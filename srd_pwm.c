/*
  Stephen Duncanson, Bloomy Controls
  RP2040 program to mimic spi bus of a bs1200 cell.
  Written fall 2022, updated spring 2023 to include new ADC.
  DAC : DAC8565
  Startup: 0x012000 to disable the default 2.5V reference.
  Then command with: 0x1#DATA
  # = 0x0, 0x2, 0x4, 0x6 = channel to be written to: A B C D
  DATA bits are 16 bit unsigned set point for the DAC.
  Vout == 2*Vref_L + (Vref_H - Vref_L) * (decimal_setpoint/65536)
  Where Vref_L == 0 V and Vref_H == 4.096V.
  ADC : ADS8328
  Startup: 0xE7FD00
  Then: 0x1000000 and 0x000000 to read from channels 0 and 1 respectively.
  Operation:
  Send startup commands to dac, adc
  Set dac channels a and b
  readback channels using adc channels 0 and 1
  repeatn
*/

#include <ctype.h>
#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "hardware/clocks.h"
#include "hardware/irq.h"
#include "hardware/spi.h"
#include "pico/stdlib.h"

#define SPI_PORT spi0
// not const in c, prefer define
const uint gpio_cs_dac = 17;
const uint gpio_cs_adc = 20;
const uint sck_gpio = 18;
const uint mosi_gpio = 19;
const uint miso_gpio = 16;
static spi_inst_t* spi = spi0;

static float vref = 3.3;//4.096;

static float v_chan0 = 0.0f;
static float v_chan1 = 0.0f;

#define INPUT_BUFFER_LEN (16U)
#define INPUT_BUFFER_LAST_IDX (INPUT_BUFFER_LEN - 1)
static char input_buffer[INPUT_BUFFER_LEN] = {0};
static unsigned int buffer_idx = 0;  // index to insert a char at

const uint8_t set_channel_mask = 0x10;
const uint8_t mask_channel_a = 0x00;
const uint8_t mask_channel_b = 0x02;
const uint8_t mask_channel_c = 0x04;
const uint8_t mask_channel_d = 0x06;

static uint8_t spi_buffer[3];
static uint8_t spi_recv_buffer[3] = {0};

static inline void cs_select(int gpio_cs_pin) {
  //asm volatile("nop \n nop \n nop");
  gpio_put(gpio_cs_pin, 0);
  //asm volatile("nop \n nop \n nop");
}

static inline void cs_deselect(int gpio_cs_pin) {
  //asm volatile("nop \n nop \n nop");
  gpio_put(gpio_cs_pin, 1);
  //asm volatile("nop \n nop \n nop");
}

static void inline SendByte(uint8_t data, int gpio_cs_pin) {
  cs_select(gpio_cs_pin);
  spi_write_blocking(SPI_PORT, &data, 1);
  cs_deselect(gpio_cs_pin);
}

static void inline SendBuffer(int gpio_cs_pin) {
  cs_select(gpio_cs_pin);  // bring cs low
  spi_write_blocking(spi, spi_buffer, 3);
  cs_deselect(gpio_cs_pin);
}

static void PrintChannelVoltage(void) {
  uint8_t temp = spi_recv_buffer[0];
  spi_recv_buffer[0] = spi_recv_buffer[1];
  spi_recv_buffer[1] = temp;
  printf("%f\n",*(uint16_t*)spi_recv_buffer * (vref / 65536.0));
}

static float ChannelBufferToVoltage(void) {
  uint8_t temp = spi_recv_buffer[0];
  spi_recv_buffer[0] = spi_recv_buffer[1];
  spi_recv_buffer[1] = temp;
  return *(uint16_t*)spi_recv_buffer * (vref / 65536.0);
}

/* Did the user hit enter after us_delay?  This function causes side effects:
   incrementing buffer_idx when a char is inserted Decrementing buffer_idx when
   backspace is pressed printing a char to the screen when it is pressed adding
   a char to global array input_buffer if a valid character is entered. */
static bool UserHitEnter(unsigned int us_delay) {
  int char_from_pc = getchar_timeout_us(us_delay);

  switch (char_from_pc) {
    case PICO_ERROR_TIMEOUT:
      break;  // common case, no char after us_delay.
    case '\r':
      printf("\n");
      return true;  // yes, the user has hit enter
    case 127:
    case '\b':
      printf("%c", char_from_pc);
      if (buffer_idx > 0) {
        input_buffer[--buffer_idx] = '\0';
      }
      break;  // backspace, del a char in buffer.
    default:
      if (isprint(char_from_pc) &&
          buffer_idx < INPUT_BUFFER_LAST_IDX) {  // valid char w/ space to place
        printf("%c", char_from_pc);
        input_buffer[buffer_idx++] = char_from_pc;
      }
      break;
  }
  return false;
}

// calculate the data bits to send to the DAC for voltage V when we
// have reference voltages of Vref_H and Vref_L
static void BitsForVoltage(float v, float Vref_H, float Vref_L) {
  uint16_t new_bits = 0;
  if (v >= Vref_H) {
    new_bits = 0xFFFF;
  } else if (v <= Vref_L) {
    new_bits = 0x0000;
  } else {
    new_bits = ((v - (2 * Vref_L)) * 65536.0f) / (Vref_H - Vref_L);
  }
  spi_buffer[1] = (uint8_t)(new_bits >> 8); /* MSByte */
  spi_buffer[2] = (uint8_t)new_bits;        /* LSByte */
}

// command is of the form n1 n2 where n1 is chan1 n2 is chan2
static void ExecuteCommand(void) {
  char selected_channel;
  char* read_from = input_buffer;
  char* read_to = NULL;
  uint16_t new_data_bits = 0x0000;
  float new_voltage_a = 0.0f;
  float new_voltage_b = 0.0f;

  // read two space delimited floats
  new_voltage_a = strtof(input_buffer, &read_to);
  new_voltage_b = strtof(read_to, NULL);

  // build the proper bits for dac channel a
  BitsForVoltage(new_voltage_a, vref, 0.0f);
  spi_buffer[0] = (set_channel_mask | mask_channel_a);
  SendBuffer(gpio_cs_dac);
  // now send the second to channel b
  BitsForVoltage(new_voltage_b, vref, 0.0f);
  spi_buffer[0] = (set_channel_mask | mask_channel_b);
  SendBuffer(gpio_cs_dac);
}

static void InputBufferClean(void) {
  memset(&input_buffer, 0, sizeof(input_buffer));
  buffer_idx = 0;
}

void InitSPI(void) {
  // set up the SPI interface.
  // spi0 and ask for 1Mhz baud, it might be different.
  spi_init(spi, 1000 * 1000);

  spi_set_format(spi0, /* Spi instance*/
                 8,    /* bits per transfer */
                 0,    /* Polarity (CPOL) */
                 1,    /* Phase (CPHA) 0 = rising edge*/
                 SPI_MSB_FIRST);

  gpio_set_function(sck_gpio, GPIO_FUNC_SPI);
  gpio_set_function(mosi_gpio, GPIO_FUNC_SPI);
  gpio_set_function(miso_gpio, GPIO_FUNC_SPI);

  // Initialize CS to idle high dac
  gpio_init(gpio_cs_dac);
  gpio_set_dir(gpio_cs_dac, GPIO_OUT);
  gpio_put(gpio_cs_dac, 1);
  // CS idle high adc
  gpio_init(gpio_cs_adc);
  gpio_set_dir(gpio_cs_adc, GPIO_OUT);
  gpio_put(gpio_cs_adc, 1);
}

static void ReadADC(void) {
  // read channel 0
  spi_buffer[0] = 0x00;
  spi_buffer[1] = 0x00;
  cs_select(gpio_cs_adc);
  spi_write_read_blocking(spi, spi_buffer, spi_recv_buffer, 2);
  cs_deselect(gpio_cs_adc);
  v_chan0 = ChannelBufferToVoltage();

  // read channel 1
  spi_buffer[0] = 0x10;
  spi_buffer[1] = 0x00;
  cs_select(gpio_cs_adc);
  spi_write_read_blocking(spi, spi_buffer, spi_recv_buffer, 2);
  cs_deselect(gpio_cs_adc);
  v_chan1 = ChannelBufferToVoltage();
}

static void SelectChannel1(void) {
  spi_buffer[0] = 0x10;
  spi_buffer[1] = 0x00;

  cs_select(gpio_cs_adc);
  spi_write_read_blocking(spi, spi_buffer, spi_recv_buffer, 2);
  cs_deselect(gpio_cs_adc);

  printf("1:");
  PrintChannelVoltage();
}

static void SelectChannel0(void) {
  spi_buffer[0] = 0x00;
  spi_buffer[1] = 0x00;

  cs_select(gpio_cs_adc);
  spi_write_read_blocking(spi, spi_buffer, spi_recv_buffer, 2);
  cs_deselect(gpio_cs_adc);
  v_chan0 = ChannelBufferToVoltage();

  // read channel 1
  spi_buffer[0] = 0x10;
  spi_buffer[1] = 0x00;

  cs_select(gpio_cs_adc);
  spi_write_read_blocking(spi, spi_buffer, spi_recv_buffer, 2);
  cs_deselect(gpio_cs_adc);
  v_chan1 = ChannelBufferToVoltage();
}

int main() {
  stdio_init_all();
  InitSPI();

  bool waiting_for_user = true;
  while (waiting_for_user) {
    if (UserHitEnter(200)) {
      printf("Sending startup command to dac.\n");
      spi_buffer[2] = 0x00;
      spi_buffer[1] = 0x20;
      spi_buffer[0] = 0x01;
      SendBuffer(gpio_cs_dac);
      printf("Sending startup command to adc.\n");
      spi_buffer[0] = 0xE7;
      spi_buffer[1] = 0xFD;
      SendBuffer(gpio_cs_adc);
      waiting_for_user = false;
    }
  }

  // set channels 1 and 2 on dac and then readback with adc.
  while (true) {
    if (UserHitEnter(20)) {
      ExecuteCommand();
      InputBufferClean();
      sleep_us(1);
      ReadADC();
      ReadADC();
      printf("0: %f\t1: %f\n", v_chan0, v_chan1);
    }
  }
  return 0;
}

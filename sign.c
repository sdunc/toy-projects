#include <stdio.h>

int main() {
  unsigned int j = 0x0000FFFF;
  printf("j before sign extension: %X\n",j);
  j = (signed int) (j << 16) >> 16;
  printf("j after sign extension: %X\n",j);
  unsigned int i = 0x00000FFF;
  printf("i before sign extension: %X\n",i);
  i = (signed int) (i << 16) >> 16;
  printf("i after sign extension: %X\n",i);
  unsigned int k = 0x00000FFF;
  printf("k before sign extension: %X\n",k);
  k = (signed int) k;
  printf("k after sign extension: %X\n",k);

  return 0;
}


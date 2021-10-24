#include <stdio.h>

int main(void) {
  int rc = 0;
  printf("int:char\n");
  for (int i=32; i<128; i++) {
    printf("%d : %c ",i,(char)i);
    rc++;
    if (rc%8==0)
      printf("\n");
  }
  return 0;
}

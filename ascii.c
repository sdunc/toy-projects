#include <stdio.h>

int main(int argc, char* argv[]) {
  if (argc > 1)
    printf("char [%c] =  int [%d]\n",*argv[1],(int)*argv[1]);
  else {
    char c;
    printf("Enter a character to get ASCII value: ");
    scanf("%c",&c);
    printf("char [%c] = int [%d]\n",c,(int)c);
  }
  return 0;
}

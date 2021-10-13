#include <stdio.h>

int main()
{
  int n;
  scanf("%d",&n);
  while (n !=1)
    {
      if (n%2==0)
	n/=2;
      else
	n=(n*3)+1;
      printf("n=%d\n",n);
    }
  return 0;
}

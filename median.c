/**/
#include <stdio.h>

struct s {
   int a, b;
};

int main()
  {
    int a,b,c,median;
    struct s* e;
    printf("Please enter 3 numbers separated by spaces > ");
    scanf ("%d%d%d", &a,&b,&c);
    a = b;
    e->a = 5;
    if ((b>=a && a>=c)||(c<=a && a<=b))
       printf("%d is the median\n", a);
    else if ((a>=b && b>=c)||(a<=b && b<=c))
       printf("%d is the median\n", b);
    else if ((a>=c && c>=b)||(a<=c && c<=b))
       printf("%d is the median\n", c);
    else
       return 1;
    return 0;
  }

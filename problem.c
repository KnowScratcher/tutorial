#include <stdio.h>
#include <stdlib.h>

int main()
{
    int a, b;
    scanf("%d",&a);
    scanf("%d",&b);
    printf("%6d\n",a);
    printf(" %s %d\n","x",b);
    printf("------\n");
    printf("%6d\n",a*((b/1)%10));
    printf("%5d\n",a*((b/10)%10));
    printf("%4d\n",a*((b/100)%10));
    printf("------\n");
    printf("%6d\n",a*b);
    return 0;
}

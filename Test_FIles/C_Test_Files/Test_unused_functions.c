#include<stdalign.h>
#include<stdio.h>
int sum(int a, int b)
{
    return a+b;
}
int fact(int n)
{
    if(n==0)
        return 1;
    else
        return n*fact(n-1);
}
int main()
{
    int a=5,b=6;
    printf("Sum of %d and %d is %d",a,b,sum(a,b));
    return 0;
}
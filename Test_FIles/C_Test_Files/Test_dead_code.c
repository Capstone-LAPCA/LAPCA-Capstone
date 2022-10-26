#include<stdio.h>
int testfun(int a, int b)
{
    int c;
    if(a>b)
    {
        c = a;
    }
    else if(a<b)
    {
        c = b;
        return c;
    }
    return c; 
    a = 10; 
    return 10;
}
int main()
{
    testfun(5,6);
}

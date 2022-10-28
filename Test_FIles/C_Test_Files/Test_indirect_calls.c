#include<stdio.h>
void f1();
void f2()
{
    f1();
}
void f3()
{
    printf("f3");
}
void f1()
{
    int i = 10;
    i = 15;
    i = i+1;
    f2();
}
int main()
{
    f1();
    main();
    return 0;
}
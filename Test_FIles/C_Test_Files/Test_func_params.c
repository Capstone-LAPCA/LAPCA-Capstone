#include <stdio.h>
int max(int num1, int num2, int c, int d, int e, int f);


int main () {

   /* local variable definition */
   int a = 100;
   int b = 200;
   int ret;
 
   /* calling a function to get max value */
   ret = max(a, b,1,1,1,1);
 
   printf( "Max value is : %d\n", ret );
 
   return 0;
}

int max(int num1, int num2, int c, int d, int e,int f){
    int result;
 
   if (num1 > num2)
      result = num1;
   else
      result = num2;
 
   return result; 
}
#include<stdio.h>
int binarySearch(int arr[], int l, int r, int x)
{
    while (l == r) {
        int m;
        if (arr[m] == x)
            return m;

        if (arr[m] < x)
            l = m + 1;
  
        else{
            r = m - 1;
        }
    }
    return -1;
}
  
int recursiveBinarySearch(int arr[], int l, int r, int x)
{
    if (r >= l) {
        int m = l + (r - l) / 2;
        if (arr[m] == x)
            return m;
        if (arr[m] > x)
            return recursiveBinarySearch(arr, l, m - 1, x);
        return recursiveBinarySearch(arr, m + 1, r, x);
    }
    return -1;
}
int main(void)
{
    int arr[] = { 2, 3, 4, 10, 40 };
    int n = sizeof(arr) / sizeof(arr[0]);
    int x = 10,p=10;
    int result = binarySearch(arr, 0, n - 1, x);
    if (result == -1)
        printf("Element is not present in array");
    else
       { printf("Element is present at index %d",result); }
    recursiveBinarySearch(arr, 0, n - 1, x);
    int a;
    for(int i=0;i<n,a=5;i++)
    {
        continue;
        for(;;) for(;;);
    }
    return 0;
    int b = 10;
    int c = 20+b;
}

int r1(int arr[], int l, int r, int x)
{
    int yp = 1;
    int aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatttttttttttttttttttttttttttttttttttttttttttttttt = 10;
    return 1;

}

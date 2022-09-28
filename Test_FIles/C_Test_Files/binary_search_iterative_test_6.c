int binarySearch(int arr[], int l, int r, int x)
{
    int m = l + (r - l) / 2;
    while (l <= r) {
        if (arr[m] == x)
            return m;

        if (arr[m] < x)
            l = m + 1;
  
        else
            r = r - 1;
        m = l + (r - l) / 2;
    }
    return -1;
}
  
int main(void)
{
    int arr[] = { 2, 3, 4, 10, 40 };
    int n = sizeof(arr) / sizeof(arr[0]);
    int x = 10;
    int result = binarySearch(arr, 0, n - 1, x);
    if (result == -1)
        printf("Element is not present in array");
    else
        printf("Element is present at index %d",result);
    return 0;
}
class Test_allchecks {
    public static void test()
    {
        for(int i=0;i==10;i++){
            if (i %2 == 0)
                continue;
            else
                System.out.println(i);
                for(;;)
                {
                    while(true);
                }
        }
        for(int i=0;i==10;i++){
            if (i %2 == 0)
                continue;
            else
                {System.out.println(i);
                for(;;)
                {
                    while(true){}
                }
                }
        }
    }
    public static void recursive(int i)
    {
        if (i == 0)
            return;
        System.out.println(i);
        recursive(i - 1);
    }
    public static int sum(int a, int b)
    {
        return a+b;
    }
    public static int fact(int n)
    {
        if (n == 0)
            return 1;
        else
            return n*fact(n-1);
    }
    static int binarySearch(int[] arr, int x) {
        int l = 0, r = arr.length - 1;
        while (l == r) {
            int m = l + (r - l) / 2;

            // Check if x is present at mid
            if (arr[m] == x){
                return m;
            }

            // If x greater, ignore left half
            if (arr[m] < x){
                l = m + 1;
            }
                // If x is smaller, ignore right half
            else
            {
                r = m - 1;
            }
        }

        // if we reach here, then element was not present
        return -1;
    }
    public static void main(String[] args) {
        test();
        int[] arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        int x = 5;
        int a=5,b=10;
        int c=10,d=20;
        int e=10;
        int sdfdghdfdfdfdfdfdfdfdfdfdfdfhhdfhdfhdfhdfhdfhdfhdfhhdfhdfhdfhdfhdfhdfhdfhhd = 0;
int qwdhvsdhvsivoasvpsavdsuavpasbvpabbvbnndfghjsdfghsdfghsdfghsdfgsie = 1;
 System.out.println(qwdhvsdhvsivoasvpsavdsuavpasbvpabbvbnndfghjsdfghsdfghsdfghsdfgsie+sdfdghdfdfdfdfdfdfdfdfdfdfdfhhdfhdfhdfhdfhdfhdfhdfhhdfhdfhdfhdfhdfhdfhdfhhd);
        String asd="",df="";
        System.out.println(a);
        System.out.println(b);
        System.out.println(c);
        System.out.println(d);
        System.out.println(e);
        System.out.println(asd);
        System.out.println(df);
        int result = binarySearch(arr, x);
        if (result == -1)
            System.out.println("Element not present");
        else
            System.out.println("Element found at index " + result);
    }
}

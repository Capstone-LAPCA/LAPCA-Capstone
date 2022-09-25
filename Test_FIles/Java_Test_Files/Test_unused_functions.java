public class Test_unused_functions {
    public static void test()
    {
        for(int i=0;i<10;i++){
            if (i %2 == 0)
                continue;
            else
                System.out.println(i);
        }
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
    int x = fact(5);
    public static void main(String[] args) {
        test();
    }
}
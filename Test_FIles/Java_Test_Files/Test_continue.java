public class Test_continue {
    public static void test()
    {
        for(int i=0;i<10;i++){
            if (i %2 == 0)
                continue;
            else
                System.out.println(i);
        }
    }
    public static void main(String[] args) {
        test();
    }
}
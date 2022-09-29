public class Test_recursion {
    public static void recursive(int i)
    {
        if (i == 0)
            return;
        System.out.println(i);
        recursive(i - 1);
    }
    public static void main(String[] args) {
        recursive(5);
    }
}

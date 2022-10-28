public class Test_indirect_recursion {
    static void f1()
    {
        f2();
    }
    static void f2()
    {
        f1();
    }
}

void recursive(int i)
{
    if (i == 0)
        return;
    recursive(i - 1);
}
void main()
{
    recursive(10);
    return;
}
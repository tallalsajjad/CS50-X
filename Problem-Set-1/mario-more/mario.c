#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Positive Number? ");
    }
    while (n < 1 || n > 8);
    for (int row = 1; row <= n; row++)
    {
        for (int i = 1; i <= n - row; i++)
        {
            printf(" ");
        }
        for (int j = 1; j <= row; j++)
        {
            printf("#");
        }
        for (int l = 1; l <= 2; l++)
        {
            printf(" ");
        }
        for (int k = 1; k <= row; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}

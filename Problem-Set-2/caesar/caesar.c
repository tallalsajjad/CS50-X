#include <cs50.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool only_digit(int num, string key);
char rotate(char c, int n);
int main(int argc, string argv[])
{
    if (only_digit(argc, argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else if (only_digit(argc, argv[1]) == true)
    {
        int key = atoi(argv[1]);
        string user_words = get_string("plaintext: ");
        int len = strlen(user_words);
        char ciphertext[len + 1];
        for (int i = 0; i < len; i++)
        {
            char cipher = rotate(user_words[i], key);
            ciphertext[i] = cipher;
        }
        ciphertext[len] = '\0';
        printf("ciphertext: %s\n", ciphertext);
        return 0;
    }
}

bool only_digit(int num, string key)
{
    if (num != 2)
    {
        return false;
    }

    int len = strlen(key);
    for (int i = 0; i < len; i++)
    {
        if (!isdigit(key[i]))
        {
            return false;
        }
    }
    return true;
}

char rotate(char c, int n)
{
    if (isalpha(c))
    {
        int p;
        if (isupper(c))
        {
            p = c - 65;
            return (p + n) % 26 + 65;
        }
        else if (islower(c))
        {
            p = c - 97;
            return (p + n) % 26 + 97;
        }
    }
    return c;
}

#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

string cipher(string key, string plaintext);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Please input 2 arguments\n");
        return 1;
    }
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 letters\n");
        return 1;
    }
    for (int i = 0; i <= strlen(argv[1]) - 1; i++)
    {
        if (isalpha(argv[1][i]) == false)
        {
            printf("Key must only have alphabet\n");
            return 1;
        }

        for (int j = i + 1; j <= strlen(argv[1]); j++)
        {
            if (toupper(argv[1][i]) == toupper(argv[1][j]))
            {
                printf("Key must contain unique letters\n");
                return 1;
            }
        }
    }
    string key = argv[1];
    for (int k = 0; k <= strlen(key); k++)
    {
        key[k] = toupper(key[k]);
    }
    string plaintext = get_string("plaintext: ");
    string ciphertext = cipher(key, plaintext);
    printf("ciphertext: %s\n", ciphertext);

    return 0;
}

string cipher(string key, string plaintext)
{
    int len = strlen(plaintext);
    for (int i = 0; i <= len; i++)
    {
        if (plaintext[i] >= 65 && plaintext[i] <= 90)
        {
            plaintext[i] = key[(plaintext[i] - 65)];
        }
        else if (plaintext[i] >= 97 && plaintext[i] <= 122)
        {
            plaintext[i] = tolower(key[(plaintext[i] - 97)]);
        }
    }

    return plaintext;
}

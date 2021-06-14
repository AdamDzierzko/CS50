#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    int key = 0;                // key given as argv[1]
    string plaintext;
    string ciphertext;

    if (argc != 2)              // check number of arguments
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int i = 0; i < strlen(argv[1]); i++)   // check if key has correct form
    {
        if (isalpha(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    key = atoi(argv[1]);                    // sting argv[1] into int
    key = key % 26;                         // final key
    plaintext = get_string("plaintext: ");  // get palaintext
    printf("ciphertext: ");                 // begin of printing ciphertext

    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (plaintext[i] >= 'a' && plaintext[i] <= 'z')     // if lowercase
        {
            if (plaintext[i] + key > 'z')                   // when char + key is bigger then z start from begin of alphabeth.
            {
                printf("%c", plaintext[i] + key - 26);
            }
            else
            {
                printf("%c", plaintext[i] + key);
            }
        }
        else if (plaintext[i] >= 'A' && plaintext[i] <= 'Z') // if uppercase
        {
            if (plaintext[i] + key > 'Z')               // when char + key is bigger then z start from begin of alphabeth.
            {
                printf("%c", plaintext[i] + key - 26);
            }
            else
            {
                printf("%c", plaintext[i] + key);
            }
        }
        else                                        // other
        {
            printf("%c", plaintext[i]);
        }
    };
    printf("\n");
}
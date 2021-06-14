#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

bool chceck_key(string key);
void encrypting(string plaintext, string key);

int main(int argc, string argv[])
{
    bool correct_key = 1;
    if (argc != 2)          // check number of args
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    correct_key = chceck_key(argv[1]);

    if (correct_key == 0)       // when key is wrong
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];       // get key

    for (int i = 0; i < 26; i++)    // take key into lowercase
    {
        key[i] = tolower(key[i]);
    }

    string plaintext = get_string("plaintext:  \n");    // ger plaintext
    
    encrypting(plaintext, key);                 // encrypting
}
    
bool chceck_key(string key)         // check proper key
{
    if (strlen(key) != 26)          // check lenght of key
    {
        return 0;
    }
    else
    {
        string a = key;
        int b = 0;
        for (int i = 0; i < 26; i++)    
        {
            char c = tolower(key[i]);   // check if key has only letter
            if (c < 'a' || c > 'z')
            {
                return 0;
            }
        }
        for (int i = 0; i < 26; i++)    // check if key has duplicated letters
        {
            b = 0;
            for (int j = 0; j < 26; j++)
            {
                if (key[i] == a[j])
                {
                    b++;
                }
            }
            if (b > 1)
            {
                return 0;
            }
        }
    }
    return 1;
}

void encrypting(string plaintext, string key)
{
    char alfabet[26];               // make alphabet char array
    for (int i = 0; i < 26; i++)
    {
        alfabet[i] = 'a' + i;
    }
    
    char ciphertext[strlen(plaintext)];
    printf("ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++)     // code
    {
        if (isupper(plaintext[i]))          // if letter in plaintext is uppercase
        {
            char a = plaintext[i];
            a = tolower(plaintext[i]);
            for (int j = 0; j < 26; j++)
            {
                if (a == alfabet[j])
                {
                    ciphertext[i] = toupper(key[j]); //put letter for key and up it
                }
            }
        }
        else                                // for sign(,.) or lowercase letters 
        {
            for (int j = 0; j < 26; j++)
            {
                if (plaintext[i] == alfabet[j])
                {
                    ciphertext[i] = key[j];     //put letter for key
                }
                if (plaintext[i] < 'a' ||  plaintext[i] > 'z') // when there is sign not letter
                {
                    ciphertext[i] =  plaintext[i];
                }
            }
        }
        printf("%c", ciphertext[i]);
    }
    printf("\n");
}
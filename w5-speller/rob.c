#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <cs50.h>

int main(void)
{

    string g_word = "b";
    int l = g_word[0];
    l = l - 97;
    printf("%i", l);

    return 0;
}
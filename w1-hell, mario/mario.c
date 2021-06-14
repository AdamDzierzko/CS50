#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int Height;
    do 
    {
        Height = get_int("Height: ");       // pick Height
    } 
    while (Height < 1 || Height > 8);       // check Height 

    for (int i = 1; i < Height + 1; i++)    // loop for row
    {
        int a = Height - i;                 // number of space columns in row

        for (int j = 0; j < a; j++)         // loop for space columns in row 
        {
            printf(" ");
        }

        for (int b = 0; b < i ; b++)        // loop for first part of # in row
        {
            printf("#");        
            if (b == i - 1)
            {
                printf("  ");               // empty space between parts of #
            }                
        }

        for (int b = 0; b < i ; b++)        // loop for second part of # in row
        {
            printf("#");
        }

        printf("\n");                       // new line
    }
}

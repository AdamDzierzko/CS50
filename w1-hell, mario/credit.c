#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    long credit = 0, cr = 0, c = 1;     // credit card number, temporaty variable to count digits, variable to separate digits by divide
    int digit = 0, a;                   // single actual digit in algoritm, even / odd number of digits in creditcard
    int sum = 0, fcd = 0, nod = 1;      // final sum made by algorithm, first two credit card digits, orginal number of digits
    bool legal;                         // legal creditcard 0/1 ?

    credit = get_long("Number: ");      // pick creditcard number
    cr = credit;                        

    while (cr / 10 >= 1)                // count digts in credit card
    {
        nod++;                            
        cr = cr / 10;
        c = c * 10;                     // liczba cyfr * 10
    };

    a = (nod % 2 == 0) ? 1 : 0;         // even / odd number of digits in creditcard

    for (int i = 1; i <= nod; i++)                   // main algorithm
    {
        digit = credit / c;         // pick first digit, the biggest 
                                    
        if (i == 1)                 // pick first digit in creditcard number,
        {
            fcd = digit * 10;
        };
        if (i == 2)                 // pick second digits in creditcard number,
        {
            fcd = fcd + digit;
        };

        if (i % 2 == a)                // even digit from end of creditcard number
        {
            digit = digit * 2;         // even digit multiply by 2         
            if (digit >= 10)           // if digit is equal or bigger then 10 
            {
                digit = (digit % 10) + 1; 
            }
            
            sum = sum + digit;          // sum of even 
        } 
        else                            // odd digit from end of creditcard number
        {
            sum = sum + digit;          // sum of odd
        }

        credit = credit % c;            // remove first digit in creditcard number

        c = c / 10;
    };

    legal = (sum % 10 == 0) ? 1 : 0;                // legal by algorithm?
    printf("l=%i", sum);

    if (legal == 1 && (fcd == 34 || fcd == 37) && (nod == 15)) //  AMEX ?
    {      
        printf("AMEX\n");
    }
    else if (legal == 1 && (fcd >= 51 && fcd <= 55) && (nod == 16))    // MASTERCARD ? 
    {  
        printf("MASTERCARD\n");
    }
    else if (legal == 1 && (fcd >= 40 && fcd <= 49) && (nod == 13 || nod == 16)) // VISA ?
    {
        printf("VISA\n");
    } 
    else                                //so creditcard is ILLEGAL!!!
    {
        printf("INVALID\n"); 
    }
}

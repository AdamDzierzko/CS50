#include<stdio.h>
#include<cs50.h>
#include<math.h>

int main(void)
{
    float  dollars = 15;            // change in dollars
    int cents = 0, coins = 0;       // change in cents, number of coins

    do                              // pick change in dollars, chcek propety
    {
        dollars = get_float("Change owned: ");
    }
    while (dollars < 0);

    cents = round(dollars * 100);   // change round to cents

    while (cents - 25 >= 0)         // count of 25c
    {
        coins++;
        cents = cents - 25;
    };
    while (cents - 10 >= 0)         // count of 10c
    {
        coins++;
        cents = cents - 10;
    };
    while (cents - 5 >= 0)          // count of 5c
    {
        coins++;
        cents = cents - 5;
    };
    while (cents - 1 >= 0)          // count of 1c
    {
        coins++;
        cents = cents - 1;
    };

    printf("%i\n", coins);          // print min number of coins
}

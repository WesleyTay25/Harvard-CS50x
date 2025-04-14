#include <cs50.h>
#include <stdio.h>

int countdigits(long credit);
int get_first(long credit, int digits);
bool luhn(long credit);

int main()
{
    long credit;
    printf("Enter credit card number: ");
    scanf("%ld", &credit);

    int size = countdigits(credit);

    if (size < 13 || size > 16)
    {
        printf("INVALID\n");
        return 0;
    }
    if (luhn(credit) == false)
    {
        printf("INVALID\n");
        return 0;
    }

    int firstd = get_first(credit, 1);
    int first2d = get_first(credit, 2);

    if (size == 15 && (first2d == 34 || first2d == 37))
    {
        printf("AMEX\n");
    }
    else if ((size == 13 || size == 16) && firstd == 4)
    {
        printf("VISA\n");
    }
    else if (size == 16 && (first2d >= 51 && first2d <= 55))
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}
bool luhn(long credit)
{
    int sum = 0;
    bool alternate = false;

    while (credit > 0)
    {
        int digit = credit % 10;

        if (alternate)
        {
            digit *= 2;
            if (digit > 9)
            {
                digit = (digit % 10) + (digit / 10);
            }
        }

        sum += digit;
        alternate = !alternate;
        credit /= 10;
    }
    return (sum % 10 == 0);
}

int countdigits(long credit)
{
    int count = 0;

    while (credit > 0)
    {
        count++;
        credit /= 10;
    }
    return count;
}

int get_first(long credit, int digits)
{
    while (countdigits(credit) > digits)
    {
        credit /= 10;
    }
    return credit;
}

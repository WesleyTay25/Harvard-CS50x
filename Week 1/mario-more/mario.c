#include <stdio.h>

void mario(int n);

int main()
{

    int height;
    // Get height of pyramid and ensure value is in between 1 and 8 if not keep prompting
    do
    {
        printf("Enter height here: ");
        scanf("%i", &height);
    }
    while (height < 1 || height > 8);

    mario(height);

    return 0;
}
void mario(int n)
{
    for (int i = 0; i < n; i++)
    {
        // Adding Spaces
        for (int spaces = 0; spaces < n - i - 1; spaces++)
        {
            printf(" ");
        }
        // Left pyramid
        for (int k = 0; k <= i; k++)
        {
            printf("#");
        }
        // Spacing in the middle
        for (int j = 0; j < 2; j++)
        {
            printf(" ");
        }
        // Right pyramid
        for (int z = 0; z <= i; z++)
        {
            printf("#");
        }

        printf("\n");
    }
    return 0;
}

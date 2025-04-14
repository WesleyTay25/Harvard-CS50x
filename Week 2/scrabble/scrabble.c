#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int addscore(string word);

int main(void)
{
    // Prompt them to receive word input
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Pass string into function to obtain score
    int score1 = addscore(word1);
    int score2 = addscore(word2);

    // Check who wins
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }

    return 0;
}

int addscore(string word)
{
    // point system
    int points[26] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                      1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    int sum = 0;
    int len = strlen(word);

    // iterate through string
    for (int i = 0; i <= len; i++)
    {
        if (toupper(word[i]) >= 'A' && toupper(word[i]) <= 'Z') // ensure all char is uppercase
        {
            sum += points[(toupper(word[i]) - 65)]; // ascii table
        }
    }
    return sum;
}

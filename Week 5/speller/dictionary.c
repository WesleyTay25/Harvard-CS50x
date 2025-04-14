// Implements a dictionary's functionality
#include <strings.h>
#include <string.h>
#include <ctype.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>


#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1]; // plus one for the /0 value
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26 * LENGTH;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int hashnumber = hash(word);
    for (node *curr = table[hashnumber]; curr != NULL; curr = curr->next)
    {
        if(strcasecmp(curr->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int hash = 0;
    int len = strlen(word);
    for (int i = 0; i < len; i++)
    {
        hash += ((toupper(word[i]) - 'A') * i); // adding ascii values of each char multiplied by position of letter
    }
    return hash % N; // reduce output value of hash function to match with indices of table
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    // TODO
    FILE *src = fopen(dictionary, "r");
    if (src == NULL)
    {
        return false;
    }
    char word[LENGTH+1];
    while (fscanf(src, "%s", word) != EOF) // get each string from dict until EOF
    {
        node *n = malloc(sizeof(node)); // create memory for new node
        if (n == NULL)
        {
            return false;
        }

        strcpy(n->word, word); // assign the node the word
        n->next = NULL;
        int hashnumber = hash(n->word); // implement hashfunction to get index

        if (table[hashnumber] == NULL)
        {
            table[hashnumber] = n;
        }
        else
        {
            n->next = table[hashnumber];
            table[hashnumber] = n;
        }
    }
    fclose(src);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    int count = 0;
    for (int i = 0; i < N; i++)
    {
        for (node *ptr = table[i]; ptr != NULL; ptr = ptr->next)
        {
            if (ptr != NULL)
            {
                count++;
            }
        }
    }
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *ptr = table[i];
        while (ptr != NULL)
        {
            node *tmp = ptr->next;
            free(ptr);
            ptr = tmp;
        }
    }
    return true;
}

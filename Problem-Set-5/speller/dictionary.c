// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

#define prem 17576 // 26^3

int words = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Choose number of buckets in hash table
const unsigned int N = prem; // Match hash space

// Hash table
node *table[N];

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash_value = 0;
    for (int i = 0; i < 3 && word[i] != '\0'; i++)
    {
        char letter = toupper(word[i]);
        if (letter >= 'A' && letter <= 'Z')
        {
            int letter_value = letter - 'A';
            hash_value = hash_value * 26 + letter_value;
        }
    }
    return hash_value % prem;
}

// Loads dictionary into memory, returning true if successful
bool load(const char *dictionary)
{
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];

    while (fscanf(source, "%45s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            fclose(source);
            return false;
        }

        strcpy(n->word, word);

        int index = hash(word);
        n->next = table[index];
        table[index] = n;

        words++;
    }

    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return words;
}

bool check(const char *word)
{
    // TODO
    int index = hash(word);
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}

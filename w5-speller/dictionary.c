// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

void insert(node n, int h);

// Number of buckets in hash table
const unsigned int N = 26; // for each alphabet letter
unsigned int n_size = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int h = 0;
    h = hash(word);   // hash word
    if (table[h] == NULL)   // hash correct ?
    {
        return false;
    }

    node *cursor = table[h]; // cursor initialize

    while (strcasecmp(word, cursor -> word) != 0) // check
    {
        if (cursor -> next == NULL) // end of checking
        {
            return false;
        }
        cursor = cursor -> next;
    }

    // TODO
    return true;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int l =  word[0];       // read first letter
    if (l >= 65 && l <= 90)     // if uppercase
    {
        l = l + 32;
    }

    l = l - 97;     // set hash
    // TODO
    return l;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;       // error in file opening
    }

    for (int i = 0; i < N; i++)     // set table[N] of NULLS
    {
        table[i] = NULL;
    }

    char *g_word = malloc(LENGTH + 1);
    unsigned int h;

    while (fscanf(file, "%s", g_word) > 0)      // loading loop
    {

        node *n = malloc(sizeof(node));     // memory for new word
        if (n == NULL)
        {
            return false;       // correct ?
        }
        n -> next = NULL;       // next as null
        strcpy(n->word, g_word); // set word variable

        h = hash(g_word);       // hash

        if (table[h] != NULL)
        {
            n -> next = table[h];   // point at previous node
        }

        table[h] = n;   // add new node to hash table

        n_size++;       // increase number of words in dictionary
    }

    fclose(file);
    free(g_word);       // free g_word memory

    // TODO
    return true;    // false
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return n_size;      // only return
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *tmp = cursor;     // tmp = cursor adres
            cursor = cursor -> next;    // move cursor foward
            free(tmp);      // free tmp
        }
    }
    // TODO

    return true;
}

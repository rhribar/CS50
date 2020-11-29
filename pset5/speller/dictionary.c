// Implements a dictionary's functionality

#include <stdbool.h>
#include "dictionary.h"
#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 65536;
unsigned int hash_index;
unsigned int word_counter = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{

    int length = strlen(word);

    char new_word[length + 1];

    for (int i = 0; i < length + 1 ; i++)
    {
        new_word[i] = tolower(word[i]);
    }

    hash_index = hash(new_word);
    node *cursor = table[hash_index];

    while (cursor != NULL)
    {
        // must be a while loop
        // must be a separate if loop
        if (strcasecmp(word,cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

/*
SOURCE: https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/
AUTHOR: delipity
*/
// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash1 = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        hash1 = (hash1 << 2) ^ word[i];
    }
    return hash1 % N;
}

/*int hash_it(char* needs_hashing)
{
    unsigned int hash = 0;
    for (int i=0, n=strlen(needs_hashing); i<n; i++)
        hash = (hash << 2) ^ needs_hashing[i];
    return hash % HASHTABLE_SIZE;
}*/

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file_pointer = fopen(dictionary, "r");

    if (file_pointer == NULL)
    {
        printf("Unable to open %s\n.", dictionary);
        return 1;
    }

    char word[LENGTH + 1];

    while (fscanf(file_pointer, "%s", word) != EOF)
    {
        // allocate memory of size node, check if it return null loop
        node *n = calloc(1, sizeof(node));
        if (n == NULL)
        {
            return 1;
        }
        // copy string
        strcpy(n->word, word);

        // get the table index of the new word
        hash_index = hash(word);

        // set the pointer to point to the next node
        n->next = table[hash_index];

        // set the head to the new node
        table[hash_index] = n;
        word_counter++;
    }

    fclose(file_pointer);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor -> next;
            free(temp);
        }
    }
    // TODO
    return true;
}

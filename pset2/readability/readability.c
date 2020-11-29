#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string s);
int count_words(string s);
int count_sentences(string s);

int main(void)
{
    string text = get_string("Text: ");

    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);
    /*
    printf("%i letter(s)\n", letters);
    printf("%i words(s)\n", words);
    printf("%i sentence(s)\n", sentences);*/

    float L = (float) letters / (float) words * 100;
    float S = (float) sentences / (float) words * 100;

    float index = 0.0588 * (float) L - 0.296 * (float) S - 15.8;

    if (index > 1 && index < 16)
    {
        printf("Grade %.0f\n", round(index));
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }

}

//method for calculating letters
int count_letters(string s)
{
    int sum_letters = 0;

    for (int i = 0; i < strlen(s); i++)
    {
        if ((s[i] >= 65 && s[i] <= 90) || (s[i] >= 97 && s[i] <= 122))
        {
            sum_letters++;
        }
    }
    return sum_letters;
}

//method for calculating words
int count_words(string s)
{
    int sum_words = 1;

    //method for calculating words
    for (int i = 0; i < strlen(s); i++)
    {
        if (s[i] == ' ')
        {
            sum_words++;
        }
    }
    return sum_words;
}

//method for calculating sentences
int count_sentences(string s)
{
    int sum_sentc = 0;

    for (int i = 0; i < strlen(s); i++)
    {
        if (s[i] == 33 || s[i] == 46 || s[i] == 63)
        {
            sum_sentc++;
        }
    }
    return sum_sentc;
}
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);         // declaration of sentences
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    int grade;                          // final grade before round
    float letters, words, sentences;    // counted
    float L, S, index;                  // algorithm vars
    string text;                        // text to pick
    text = get_string("Text: ");

    letters = count_letters(text);      // count letters
    words = count_words(text);          // count words
    sentences = count_sentences(text);  // count sentences

    L = (letters / words) * 100;        // counting index
    S = (sentences / words) * 100;
    index = 0.0588 * L - 0.296 * S - 15.8;

    if (index < 1)                      // print result
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        grade = round(index);
        printf("Grade %i\n", grade);
    }

}

int count_letters(string text)          // count letters in text
{
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        letters = (islower(text[i]) || isupper(text[i])) ? letters + 1 : letters ;
    }
    return letters;
}

int count_words(string text)            // count words in text
{
    int words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        words = (text[i] == ' ') ? words + 1 : words;
    }
    return words;
}

int count_sentences(string text)        // count sentences in text
{
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        sentences = (text[i] == '.' || text[i] == '?' || text[i] == '!') ? sentences + 1 : sentences;
    }
    return sentences;
}
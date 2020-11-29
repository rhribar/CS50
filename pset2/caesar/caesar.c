#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

string Encrypt(string s, int key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    for (int i = 0; argv[1][i] != '\0'; i++)
    {
        if (isalpha(argv[1][i]) != 0)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int key = atoi(argv[1]) % 26;
    /*
    int key;
    if(argc == 2 && isdigit(*argv[1])) {
        printf("Success\n");
        key = atoi(argv[1]) % 26;
        if(key == 0) {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    } else {
        printf("Usage: ./caesar key\n");
        return 1;
    }*/

    string text = get_string("plaintext: ");

    string encrypted = Encrypt(text, key);

    string s = "hello, world!";

    //printf("ciphertext:%c\n", text);
}

string Encrypt(string s, int key)
{
    printf("ciphertext: ");
    for (int i = 0; i < strlen(s); i++)
    {
        int c = 0;
        //check if uppercase
        if (isupper(s[i]))
        {


            //printf("%c", s[i]);
            c = (((int)s[i] - 65 + key) % 26) + 65;

            /*
            s[i] += key;
            if(s[i] > 90) {
                s[i] = (s[i] % 90) + 64;
            }*/
            printf("%c", (char) c);
        }
        //check if lowercase
        if (islower(s[i]))
        {

            c = (((int)s[i] - 97 + key) % 26) + 97;
            /*
            s[i] += key;
            //printf("%c", s[i]);

            if(s[i] > 122) {
                s[i] = (s[i] % 122) + 96;
            }
            */
            printf("%c", (char) c);
        }
        else
        {
            printf("%c", s[i]);
        }

    }
    printf("\n");
    return s;
}
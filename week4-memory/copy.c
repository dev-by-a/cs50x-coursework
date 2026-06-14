#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    char *s = get_string("s: ");
    if (s == NULL)// if user enters a big value then get string should return null as an error
    {
        return 1;
    }

    char *t = malloc(strlen(s) + 1);// using malloc we are asking for memory
    if (t == NULL)
    {
        return 1;
    }

    strcpy(t, s); // (destination, source) copy s's bytes to t

    if (strlen(s) > 0) // if user simply entered and didnt add any value
    {
        t[0] = toupper(t[0]);
    }

    printf("s: %s\n", s);
    printf("t: %s\n", t);

    free(t); // freeing the memory back to the os

}

/* NUL - its nul terminator, /0, its a single byte of 8 bits all of which are zero
NULL - special memeory address, Ox0, where nothing is ever sppose to live
get string automatically gives back the memory once its used.*/

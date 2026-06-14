#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(void)
{
    int n = 50;
    int *p = &n;
    printf("%p\n", p); //%p is used to print out address
    printf("%i\n", *p); // *dereference operator, means go the address in p



    string s = "HI!";
    printf("%s\n", s);
    printf("%p\n", s);
    printf("%p\n", &s[0]);// array notation, syntactic sugar
    printf("%p\n", &s[1]);
    printf("%p\n", &s[2]);
    printf("%p\n", &s[3]);

    char *t = "HI!"; // go to that address print till you get to the null operator
    printf("%s\n", t);
    printf("%c\n", *t);
    printf("%c\n", *(t+1));// pointer arithmetic
    printf("%c\n", *(t+2));

}


/* Notes

Pointer is a variable that can store an address of a value in memory

 int n = 50;
 int *p = &n; --> the asterisk means that this variable p stores an address of the value n

 */



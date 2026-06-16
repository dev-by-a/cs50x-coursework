#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover card.raw\n");
        return 1;
    }

    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    uint8_t buffer[512];
    FILE *output = NULL;
    int counter = 0;
    char filename[8];

    while (fread(buffer, 512, 1, card) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
             if (output != NULL)
            {
                 fclose(output);
            }

                sprintf(filename, "%03i.jpg", counter);
                output = fopen(filename, "w");
                counter++;
        }
        // new jpeg found

        if (output != NULL)
        {
            fwrite(buffer, 512, 1, output);
        }
    }

    if (output != NULL)
    {
        fclose(output);
    }
    fclose(card);
    return 0;
}

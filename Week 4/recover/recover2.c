#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>



int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("only 1 argument\n");
        return 1;
    }

    FILE *raw = fopen(argv[1], "r");

    uint8_t buffer[512];
    int counter = 0;
    bool isgen = false;
    FILE *img = NULL;
    char filename[8];

    while (fread(buffer, 512, 1, raw) != 0)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && buffer[3] <= 239 && buffer[3] >= 224)
        {
            if (isgen != false)
            {
                fclose(img);
                isgen = false;
            }
            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                printf("File could not be opened\n");
            }
            fwrite(buffer, 512, 1, img);
            counter++;
            isgen = true;
        }
        else if (isgen == true)
        {
            fwrite(buffer, 512, 1, img);
        }
    }
    fclose(img);
    fclose(raw);
}


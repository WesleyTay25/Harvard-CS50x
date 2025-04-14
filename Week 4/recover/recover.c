#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    // only accept one argument
    if (argc != 2)
    {
        printf("Enter only one argument\n");
        return 1;
    }

    // open file
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file\n");
        return 1;
    }

    // buffer of 512 bytes
    uint8_t buffer[512];

    int counter = 0;

    FILE *img = NULL; // create a pointer to point to a image
    bool isgenerating = false;

    // iterate through every byte in memory card
    while (fread(buffer, 512, 1, input) != 0)
    {
        // check if first 4 bytes have the signature JPEG format
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && buffer[3] <= 239 && buffer[3] >= 224)
        {
            // remove existing image to write in a new one
            if (isgenerating != false)
            {
                fclose(img);
                isgenerating = false;
            }
            char *file_name = malloc(8); // allocate memory for name of new file _ _ _ . j p g \0 --> 8 bytes
            sprintf(file_name, "%03i.jpg", counter); // name each file increment by one
            img = fopen(file_name, "w"); // note: img is a pointer to the image fle
            free(file); // free up the memory as pointer of file has already been assigned
            if (img == NULL)
            {
                printf("Could not open file \n");
                return 1;
            }
            fwrite(buffer, sizeof(buffer), 1, img); // write buffer into new image file
            counter ++;
            isgenerating = true;
        }
        else if (isgenerating == true) // means that there is an existing image after the start
        {
            fwrite(buffer, sizeof(buffer), 1, img); // restore the rest of the image
        }
    }
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(input);
}


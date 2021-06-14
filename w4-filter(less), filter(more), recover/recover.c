#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{

    if (argc != 2)          // check number of files
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");       // open card data file
    if (file == NULL)
    {
        return 1;
    }

    int lenght = 512, jpg_number = 0, start_of_jpg = 0;
    char *filename = malloc(8 * sizeof(char));
    unsigned char data[512];
    FILE *img;

    while (1)
    {
        lenght = fread(data, sizeof(unsigned char), 512, file);     // read data
        if (lenght != 512)                              // is it end
        {
            free(filename);
            break;
        }

        if (data[0] == 0xff && data[1] == 0xd8 && data[2] == 0xff && (data[3] & 0xf0) == 0xe0)  // is begin of jpg ?
        {
            if (jpg_number == 0)                        // first jpg
            {
                sprintf(filename, "%03i.jpg", jpg_number);
                jpg_number++;
                img = fopen(filename, "w");
                start_of_jpg = 1;
            }
            else                                        // other jpg
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", jpg_number);
                jpg_number++;
                img = fopen(filename, "w");
            }
        }

        if (start_of_jpg == 1)              // write data
        {
            fwrite(data, sizeof(unsigned char), 512, img);
        }

    }

    return 0;           // no bugs
}


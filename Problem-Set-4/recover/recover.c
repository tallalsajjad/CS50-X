#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could'nt open file\n");
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];

    // While there's still data left to read from the memory car
    FILE *img = NULL;
    int file_count = 0;
    char filename[8]; // e.g., "001.jpg"

    // 4. Read blocks of 512 bytes
    while (fread(buffer, 1, 512, card) == 512)
    {
        // 5. Check for JPEG header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // 6. If already writing a file, close it
            if (img != NULL)
            {
                fclose(img);
            }

            // 7. Open a new file
            sprintf(filename, "%03i.jpg", file_count);
            img = fopen(filename, "w");
            file_count++;
        }

        // 8. If a JPEG file is open, write to it
        if (img != NULL)
        {
            fwrite(buffer, 1, 512, img);
        }
    }

    // 9. Clean up
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(card);
    return 0;
}

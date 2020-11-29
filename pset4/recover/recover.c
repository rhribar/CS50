#include <stdio.h>
#include <stdlib.h>

#define BUFFER_SIZE 512

int main(int argc, char *argv[])
{
    // checking for valid input 1
    if (argc != 2)
    {
        printf("You need to specify the file.");
        return 1;
    }

    // assigning an input file
    char *input_file = argv[1];
    FILE *input_pointer = fopen(input_file, "r"); // assigning a pointer to the input file

    // checking for valid input 2
    if (input_file == NULL)
    {
        printf("Unable to open: %s\n", input_file);
        return 1;
    }

    //declaration of buffer here
    unsigned char buffer[BUFFER_SIZE];

    //declaration of a new file here
    FILE *output_pointer = NULL;
    int counter = 0; // creating a counter here
    int jpg_found = 0; // an int if file has been found

    // reading through the whole buffer block
    while (fread(&buffer, BUFFER_SIZE, 1, input_pointer) == 1)
    {
        // checking for start of the jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (jpg_found == 1) // checking if we have already found the jpeg
            {
                //start of the image has been found so close the current one
                fclose(output_pointer);
            }
            else
            {
                // setting jpg_found in the loop to 1 for first file
                jpg_found = 1;
            }
            char filename[8];
            sprintf(filename, "%03i.jpg", counter); // setting correct notation 000, 001, ...
            output_pointer = fopen(filename, "w"); // opening up a new file to write into
            counter++; // increasing the counter for the next file
        }

        if (jpg_found == 1)
        {
            // copy the blocks from buffer to new file, once jpg has been found
            fwrite(&buffer, BUFFER_SIZE, 1, output_pointer);
        }
    }

    //close the files when we are done
    if (output_pointer == NULL)
    {
        fclose(output_pointer);
    }
    if (input_pointer == NULL)
    {
        fclose(input_pointer);
    }
}

/*

Open memory card
    FILE *f = fopen(card,"r");
Repeat until end of card: (for loop)
    Read 512 bytes into buffer
    If start of new JPEG (if loop for jpeg)
        If first JPEG
            ... (for loop for writing the JPEG to the file)
        Else (if not first, close current file, open new file)
            ...
    Else
        If already found JPEG
            ... Keep writing the file
Close any remaining files


*/

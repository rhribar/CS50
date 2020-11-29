#include "helpers.h"
#include <math.h>

// Convert image to grayscale

void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < width; i++) {
        for(int j = 0; j < height; j++) {
            float average = round((image[j][i].rgbtRed + image[j][i].rgbtBlue + image[j][i].rgbtGreen) / 3.0);
            image[j][i].rgbtRed = average;
            image[j][i].rgbtBlue = average;
            image[j][i].rgbtGreen = average;
        }
    }
}

int limit(int color)
{
    if (color > 255)
    {
        color = 255;
    }
    return color;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < width; i++) {
        for(int j = 0; j < height; j++) {
            int sepiaRed = limit(round(0.393 * image[j][i].rgbtRed + 0.769 * image[j][i].rgbtGreen + 0.189 * image[j][i].rgbtBlue));
            int sepiaGreen = limit(round(0.349 * image[j][i].rgbtRed + 0.686 * image[j][i].rgbtGreen + 0.168 * image[j][i].rgbtBlue));
            int sepiaBlue = limit(round(0.272 * image[j][i].rgbtRed + 0.534 * image[j][i].rgbtGreen + 0.131 * image[j][i].rgbtBlue));
            /*
            if (sepiaRed > 255) {
                sepiaRed = 255;
            } else if (sepiaGreen > 255) {
                sepiaGreen = 255;
            } else if (sepiaBlue > 255) {
                sepiaBlue = 255;
            }*/
            image[j][i].rgbtRed = sepiaRed;
            image[j][i].rgbtBlue = sepiaBlue;
            image[j][i].rgbtGreen = sepiaGreen;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int temp[3];
    for(int j = 0; j < height; j++) {
        for(int i = 0; i < width / 2; i++) {
        temp[0] = image[j][i].rgbtRed;
        temp[1] = image[j][i].rgbtBlue;
        temp[2] = image[j][i].rgbtGreen;

        int iterator = width - 1 - i;
        image[j][i].rgbtBlue = image[j][iterator].rgbtBlue;
        image[j][i].rgbtGreen = image[j][iterator].rgbtGreen;
        image[j][i].rgbtRed = image[j][iterator].rgbtRed;

        image[j][iterator].rgbtRed = temp[0];
        image[j][iterator].rgbtBlue = temp[1];
        image[j][iterator].rgbtGreen = temp[2];

        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int sumBlue;
    int sumGreen;
    int sumRed;

    float counter;
    RGBTRIPLE temp[height][width];

    for(int i = 0; i < width; i++) {
        for(int j = 0; j < height; j++) {

            sumBlue = 0;
            sumGreen = 0;
            sumRed = 0;
            counter = 0.00;


            for(int k = -1; k < 2; k++) {
                if(j + k < 0 || j + k > height - 1)     {
                    continue;
                }
                for(int h = -1; h < 2; h++) {
                    if(i + h < 0 || i + h > width - 1) {
                        continue;
                    }
                    sumBlue += image[j+k][i+h].rgbtBlue;
                    sumGreen += image[j+k][i+h].rgbtGreen;
                    sumRed += image[j+k][i+h].rgbtRed;
                    counter++;

                }
            }
            temp[j][i].rgbtBlue = round(sumBlue / counter);
            temp[j][i].rgbtGreen = round(sumGreen / counter);
            temp[j][i].rgbtRed = round(sumRed / counter);
        }
    }


    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            image[j][i].rgbtBlue = temp[j][i].rgbtBlue;
            image[j][i].rgbtGreen = temp[j][i].rgbtGreen;
            image[j][i].rgbtRed = temp[j][i].rgbtRed;
        }
    }
}

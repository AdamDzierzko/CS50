#include "helpers.h"
#include "math.h"
#include "stdio.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float b = image[i][j].rgbtBlue;
            float g = image[i][j].rgbtGreen;
            float r = image[i][j].rgbtRed;

            float a;
            a = (b + g + r) / 3;
            unsigned char d = round(a);             // round to nearest int

            image[i][j].rgbtBlue = d;
            image[i][j].rgbtGreen = d;
            image[i][j].rgbtRed = d;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float r = image[i][j].rgbtRed;
            float g = image[i][j].rgbtGreen;
            float b = image[i][j].rgbtBlue;

            float red = 0.393 * r + 0.769 * g + 0.189 * b;      // red filter
            float green = 0.349 * r + 0.686 * g + 0.168 * b;    // green filter
            float blue = 0.272 * r + 0.534 * g + 0.131 * b;     // blue filter

            if (red > 255)                      // more than 255
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }

            image[i][j].rgbtRed = round(red);
            image[i][j].rgbtGreen = round(green);
            image[i][j].rgbtBlue = round(blue);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE im1[height][width];           // temp image to put new pixels

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            im1[i][width - j - 1] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)        // move temp image to orginal
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = im1[i][j];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int n = 0;                              // number - how pixels are counted
    float red = 0;
    float green = 0;
    float blue = 0;
    RGBTRIPLE temp[height][width];           // temp image

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            n = 0;
            red = 0;
            green = 0;
            blue = 0;
            for (int a = -1; a < 2; a++)
            {
                for (int b = -1; b < 2; b++)
                {
                    int c = i + a;
                    int d = j + b;

                    if ((c > -1 && c < height) && (d > -1 && d < width))
                    {
                        red = red + image[c][d].rgbtRed;            
                        green = green + image[c][d].rgbtGreen;
                        blue  = blue + image[c][d].rgbtBlue;
                        n++;
                    }
                }

            }
            temp[i][j].rgbtRed = round(red / n);             // temp image
            temp[i][j].rgbtGreen = round(green / n);
            temp[i][j].rgbtBlue = round(blue / n);
        }
    }   
    for (int i = 0; i < height; i++)            // temp image into orginal
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;

}

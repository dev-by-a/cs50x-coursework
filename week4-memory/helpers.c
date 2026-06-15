#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for  (int j = 0; j < width; j++)
        {
            int avg = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);

            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {

        for (int j = 0; j < width; j++)
        {
            int sumR = 0, sumG = 0, sumB = 0, count = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    if (i + di >= 0 && i + di < height && j + dj >= 0 && j + dj < width)
                    {
                        sumR += copy[i + di][j + dj].rgbtRed;
                        sumG += copy[i + di][j + dj].rgbtGreen;
                        sumB += copy[i + di][j + dj].rgbtBlue;
                        count++;
                    }
                }
            }

            image[i][j].rgbtRed = round((float) sumR / count);
            image[i][j].rgbtGreen = round((float) sumG / count);
            image[i][j].rgbtBlue = round((float) sumB / count);
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gxR = 0, gyR = 0;
            int gxG = 0, gyG = 0;
            int gxB = 0, gyB = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    if (i +di >= 0 && i + di < height && j + dj >= 0 && j + dj < width)
                    {
                        gxR += Gx[di + 1][dj + 1] * copy[i + di][j + dj].rgbtRed;
                        gyR += Gy[di + 1][dj + 1] * copy[i + di][j + dj].rgbtRed;
                        gxG += Gx[di + 1][dj + 1] * copy[i + di][j + dj].rgbtGreen;
                        gyG += Gy[di + 1][dj + 1] * copy[i + di][j + dj].rgbtGreen;
                        gxB += Gx[di + 1][dj + 1] * copy[i + di][j + dj].rgbtBlue;
                        gyB += Gy[di + 1][dj + 1] * copy[i + di][j + dj].rgbtBlue;
                    }
                }
            }

            int red = round(sqrt(gxR * gxR + gyR * gyR));
            int green = round(sqrt(gxG * gxG + gyG * gyG));
            int blue = round(sqrt(gxB * gxB + gyB * gyB));

            image[i][j].rgbtRed = (red > 255) ? 255 : red;
            image[i][j].rgbtGreen = (green >255) ? 255 : green;
            image[i][j].rgbtBlue = (blue >255) ? 255 : blue;
            
        }
    }
}

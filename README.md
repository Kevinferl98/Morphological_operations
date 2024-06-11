# Morphological operations

Morphological operation rapresent a suite of techniques in image processing. They are fundamentally grounded in two concepts: reflection and translation. 

These operations employ structuring elements. A structuring element is a matrix that defines the neighborhood used to process each pixel in the image. The center pixel of the structuring element, called the origin, identifies the pixel in the image being processed.

The array of morphological operations includes dilation, erosion, opning, and closing. When these operations are combined with different structuring elements, they can transform an image in various ways.

## About this project

This project involves the development of a web application that enables users to upload an image, select the desired morphological operation, and specify the shape and size of the structuring element to be used. The application then processes the image using the selected operation and structuring element, and returns the processed image as output.

The web application has been developed using Flask. The morphological operations have been manually implemented in Python. 

## How to run it

In order to execute this project using Docker, it a prerequisite to have Docker installed on your system.

The project can be run simply by executing the following command:

```
docker-compose up -d
```
Executing this command will initiate and run the container for the web application.

Then, you can access the web application by navigating to the following URL: http://localhost:5000

# Morphological operations

Morphological operations represent a suite of techniques in image processing that allow particular structures of an image to emerge or be attenuated.

Morphological operations work by sliding a structuring element over the image. A structuring element is a matrix that defines the region of pixels to be used to process each pixel of the image. The central pixel of the structuring element identifies the pixel of the image beign processed.

The array of morphological operations includes dilation, erosion, opening, and closing. When these operations are combined with different structuring elements, they can transform an image in various ways.

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

## How to use it

After uploading an image, you will have the opportunity to choose the desired operation, as well as the shape and size of the structuring element.

Once these selections have been made, you can proceed by submitting the request. As a result, you will receive the image processed based on the choices made.
<p align="center">
<img src="Images/Demo.gif" alt="Demo" width="80%"/>
</p>

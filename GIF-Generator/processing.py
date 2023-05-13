


import cv2
import numpy as np

def stucki_dithering(img):
    # Define the kernel for Stucki's algorithm
    kernel = np.array([
        [0, 0, 0, 8, 4],
        [2, 4, 8, 4, 2],
        [1, 2, 4, 2, 1]
    ]) / 42.0

    # Create an empty array for the dithered image
    dithered = np.zeros_like(img)

    # Loop over the rows and columns of the image
    for y in range(img.shape[0]-2):
        for x in range(img.shape[1]-2):
            # Get the current pixel value
            pixel = img[y, x]

            # Calculate the error
            error = pixel - dithered[y, x]

            # Set the current pixel value based on the error
            if error > 0:
                dithered[y, x] = 255
            else:
                dithered[y, x] = 0

            # Distribute the error to the neighboring pixels using the kernel
            if x < img.shape[1] - 1:
                dithered[y, x + 1] += error * kernel[0, 4]
            if x < img.shape[1] - 2:
                dithered[y, x + 2] += error * kernel[0, 3]
            if y < img.shape[0] - 1:
                if x > 0:
                    dithered[y + 1, x - 1] += error * kernel[2, 0]
                if x > 1:
                    dithered[y + 1, x - 2] += error * kernel[2, 1]
                dithered[y + 1, x] += error * kernel[2, 2]
                if x < img.shape[1] - 2:
                    dithered[y + 1, x + 1] += error * kernel[2, 3]
                if x < img.shape[1] - 3:
                    dithered[y + 1, x + 2] += error * kernel[2, 4]
            if y < img.shape[0] - 2:
                dithered[y + 2, x] += error * kernel[1, 2]
                if x > 0:
                    dithered[y + 2, x - 1] += error * kernel[1, 0]
                    dithered[y + 2, x - 2] += error * kernel[1, 1]
                if x < img.shape[1] - 1:
                    dithered[y + 2, x + 1] += error * kernel[1, 3]
                    dithered[y + 2, x + 2] += error * kernel[1, 4]

    return dithered

#Assumes BGR
def dither(img, method):
	method = method.lower()
	methodFunc = None
	match method:
		case 'stucki':
			pass
			methodFunc = stucki_dithering
	print("starting blue")
	blue = methodFunc(img[:,:,0])
	print("finished blue")
	green = methodFunc(img[:,:,1])
	red = methodFunc(img[:,:,2])
	return cv2.merge((blue,green,red))
	
			
	
import os
import cv2
import argparse



def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA, preserve_aspect_ratio = True):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    if(not preserve_aspect_ratio):
        # resize the image
        resized = cv2.resize(image, (width, height), interpolation = inter)
        return resized

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resize images')
    parser.add_argument('input', type=str, help='path to the input')
    parser.add_argument('-x', '--width', type=int, default=480, help='width of the output images')
    parser.add_argument('-y', '--height', type=int, default=None, help='height of the output images')
    parser.add_argument('-a', '--aspect', type=bool, default=True, help='maintain aspect ratio')
    args = parser.parse_args()

        # Check if the directory exists
    if not os.path.exists('../output'):
        print("Output directory does not exist.")
        # Create the directory
        os.mkdir('../output')
        print("Output directory has been created.")

    # Check if input is a directory
    if os.path.isdir(args.input):
        # Get each image
        for imageFile in os.listdir(args.input):
            # Get the path to the image
            image_path = os.path.join(args.input, imageFile)
            # Open the image
            image = cv2.imread(image_path)
            # Resize the image
            image = image_resize(image, width=args.width, height=args.height, preserve_aspect_ratio=args.aspect)
            # Save the image
            cv2.imwrite(f'../output/{image}_resized', image)
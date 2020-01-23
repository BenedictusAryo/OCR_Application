# Import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image for OCR")
ap.add_argument("-p", "--preprocess", type=str,
                default="thresh", help="type of preprocessing to be done")
args = vars(ap.parse_args())

# load the example image and convert it to grayscale
image = cv2.imread(args["image"])
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Check to see if we should apply thresholding to preprocess image
if args["preprocess"] == "thresh":
    gray_img = cv2.threshold(gray_img, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# Make a check to see if median blurring should be done to remove noise
elif args["preprocess"] == "blur":
    gray_img = cv2.medianBlur(gray_img, 3)

# Write the grayscale image to disk as temporary file
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray_img)

# Load the image as a PIL/Pillow image,
# apply OCR then delete the temporary file
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(text)

# Show the output images
cv2.imshow("Image", image)
cv2.imshow("Output", gray_img)
cv2.waitKey(0)

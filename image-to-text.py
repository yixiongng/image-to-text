import cv2
import imutils
import pytesseract
from pytesseract import Output
import csv
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True,
	help="path of the images stored")

args = vars(ap.parse_args())

# reading image using opencv
image = cv2.imread(args["path"])

#converting image into gray scale image
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# converting it to binary image by Thresholding
# this step is require if you have colored image because if you skip this part
# then tesseract won't able to detect text correctly and this will give incorrect result

threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)[1]

### uncomment it if you want to show the image
# # display image
# resizedimage = imutils.resize(threshold_img, width=700)
# cv2.imshow('threshold image', resizedimage)

# # Maintain output window until user presses a key
# cv2.waitKey(0)

# # Destroying present windows on screen
# cv2.destroyAllWindows()
### uncomment until here

#configuring parameters for tesseract
custom_config = r'--oem 3 --psm 6'

# now feeding image to tesseract

details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='eng')

total_boxes = len(details['text'])

### uncomment it if you want to show the image
# for sequence_number in range(total_boxes):

# 	if int(float(details['conf'][sequence_number])) > 30:
# 		(x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
# 		threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# # display image
# resizedimage = imutils.resize(threshold_img, width=700)
# cv2.imshow('captured text', resizedimage)

# # Maintain output window until user presses a key
# cv2.waitKey(0)

# # Destroying present windows on screen
# cv2.destroyAllWindows()
### uncomment until here

parse_text = []
word_list = []
last_word = ''

for word in details['text']:

    if word!='':
        word_list.append(word)
        last_word = word

    if (last_word!='' and word == '') or (word==details['text'][-1]):
        parse_text.append(word_list)
        word_list = []

with open('result_text.txt',  'w', newline="") as file:
    csv.writer(file, delimiter=" ").writerows(parse_text)
import os

import datetime

import cv2
import pytesseract
from PIL import Image
from flask import *

from werkzeug.utils import secure_filename


app=Flask(__name__)


@app.route('/readtext',methods=['post'])
def readtext():
    print(request.files)
    image = request.files['file']
    print(image)
    img = secure_filename(image.filename)

    image.save("sample.jpg")
    text=main("sample.jpg")
    print(text,"===========================================")
    return text
def main(path):
    # Get File Name from Command Line
    # path = input("Enter the file path : ").strip()

    # Load the required image
    print("path===",path)
    image = cv2.imread(path)
    # print(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Store grayscale image as a temporary file to apply OCR
    filename = "{}.png".format("temp")
    cv2.imwrite(filename, gray)

    # Load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\Tesseract-OCR\tesseract.exe'
    # filename="ss.png"
    text = pytesseract.image_to_string(Image.open(filename))

    print("OCR Text is " + text.strip())
    # val=text.strip().split('D')
    # atte=val[0].split(',')
    # print(atte[0],atte[1])
    # # print(val[1])
    if len(text)>120:
        text=text[0:120]
    print("===================================")
    print(text)
    return  text.strip()




if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)
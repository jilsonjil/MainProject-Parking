
import numpy as np
import cv2
from src.dbconnection import *
import time
from flask import *
import pymysql
# con=pymysql.connect(host='localhost',user='root',port=3306,passwd='',db='ocr')
# cmd=con.cursor()
from src.ocr_main import main
import os
import re
f=1
sdThresh = 35
font = cv2.FONT_HERSHEY_SIMPLEX

#TODO: Face Detection 1
regex="^[A-Z|a-z]{2}\s?[0-9]{1,2}\s?[A-Z|a-z]{0,3}\s?[0-9]{4}$"
sltno='654'
def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist
cv2.namedWindow('frame')
cv2.namedWindow('dist')
#capture video stream from camera source. 0 refers to first camera, 1 referes to 2nd and so on.
cap = cv2.VideoCapture(0)
_, frame1 = cap.read()
# _, frame2 = cap.read()
facecount = 0
while(True):
    stDev=0
    try:
        _, frame3 = cap.read()
        rows, cols, _ = np.shape(frame3)
        cv2.imshow('dist', frame3)
        dist = distMap(frame1, frame3)

        # apply Gaussian smoothing
        mod = cv2.GaussianBlur(dist, (9,9), 0)
        # apply thresholding
        _, thresh = cv2.threshold(mod, 100, 255, 0)
        # calculate st dev test
        _, stDev = cv2.meanStdDev(mod)
        cv2.imshow('dist', frame3)
        cv2.putText(frame1, "Standard Deviation - {}".format(round(stDev[0][0],0)), (70, 70), font, 1, (255, 0, 255), 1, cv2.LINE_AA)
        a = stDev
        #print(a[0][0])

    except Exception as e:
        #print(e,"===================")
        stDev=12
    if stDev > sdThresh:
     if f>=10:
        #print("Motion detected..",stDev);
        #TODO: Face Detection 2
        out = cv2.imwrite('num.jpg', frame3)
        wn=main("num.jpg")
        # wn = main("Capture.PNG")

        #print("word===>",wn)
        wn=wn.split("\n")

        print(wn)
        for i in wn:
            x = re.search('^[A-Z|a-z]{1,2}[0-9]{1,2}[A-Z|a-z]{0,3}[0-9]{4}$', i)
            if x is not None:

                print(i,x)
                qry="select * from vehicle where vehno=%s"
                res=selectone(qry,i)
                if res is  None:
                    qry = "insert into vehicle values(null,%s,now(),'null',%s,%s,'null')"
                    val = (11, 3, i)
                    iud(qry, val)





        # break
     else:
         f=f+1
         #print("==============================================================")
    # cv2.imshow('frame', frame1)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()





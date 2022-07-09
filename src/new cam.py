
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
        # dist = distMap(frame1, frame3)
        #
        # # apply Gaussian smoothing
        # mod = cv2.GaussianBlur(dist, (9,9), 0)
        # # apply thresholding
        # _, thresh = cv2.threshold(mod, 100, 255, 0)
        # # calculate st dev test
        # _, stDev = cv2.meanStdDev(mod)
        # cv2.imshow('dist', frame3)
        # cv2.putText(frame1, "Standard Deviation - {}".format(round(stDev[0][0],0)), (70, 70), font, 1, (255, 0, 255), 1, cv2.LINE_AA)
        # a = stDev
        # # print (a,"+++++++++++")
        # #print(a[0][0])
        stDev=10

    except Exception as e:

        stDev=12
    if stDev > 0:
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
                qry="select * from booking where date(entime)=curdate() and vehno=%s and  booking.sid in(select sid from slot where aid=2) and status!='finished'"
                res=selectone(qry,i)
                if res is  None:
                    qry="select * from vehicle where vehno=%s and status='pending'"
                    rr=selectone(qry,i)
                    if rr is None:
                        qry = "insert into vehicle values(null,%s,now(),'null',%s,%s,'pending',2)"
                        val = (0,0, i)
                        iud(qry, val)

                    else:
                        qry="update vehicle set `exit`=now(),status='finished' where id=%s"
                        iud(qry,rr[0])

                        qry = "update slot set status='free' where sid=%s"
                        iud(qry, rr[4])

                        qry="select hour(timediff(vehicle.exit,entry)) from vehicle where id=%s"
                        resdate=selectone(qry,rr[0])
                        amt=10
                        try:
                            amt=(int(resdate[0])+1)*10
                        except:
                            pass

                        qry="insert into bill values(null,%s,%s,curdate(),'pending')"
                        val=(rr[0],amt)
                        iud(qry,val)



                else:
                    if res[5]=='booked':
                        qry = "select status from slot where sid=%s "
                        ss = selectone(qry, res[4])
                        if ss[0] == "free":
                            qry="update booking set status='entered' where bookid=%s"
                            iud(qry,res[0])
                        else:
                            qry = "update booking set status='complicated' where bookid=%s"
                            iud(qry, res[0])
                        # qry="select status from slot where sid=%s "
                        # ss=selectone(qry,res[4])

                        if ss[0]=="free":
                            qry="update slot set status='allocated' where sid=%s"
                            iud(qry,res[4])


                        qry="insert into vehicle values(null,%s,now(),'null',%s,%s,'pending',2)"
                        val=(res[0],res[4],i)
                        iud(qry,val)
                    else:

                        qry = "update booking set status='finished' where bookid=%s"
                        iud(qry, res[0])
                        qry = "update vehicle set `exit`=now(),status='finished' where bookid=%s"
                        val = (res[0])
                        iud(qry, val)
                        qry = "update slot set status='free' where sid=%s"
                        iud(qry, res[4])
                        qry="select * from vehicle where bookid=%s"
                        rr=selectone(qry,res[0])

                        qry = "select hour(timediff(vehicle.exit,entry)) from vehicle where id=%s"
                        resdate = selectone(qry, rr[0])
                        amt=10
                        try:
                            amt = (int(resdate[0]) + 1) * 10
                        except:
                            pass

                        qry = "insert into bill values(null,%s,%s,curdate(),'pending')"
                        val = (rr[0], amt)
                        iud(qry, val)










        # break

                time.sleep(10)
     else:
         f=f+1
         #print("==============================================================")
    # cv2.imshow('frame', frame1)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()





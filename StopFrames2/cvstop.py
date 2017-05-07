import numpy as np
import cv2

Ydata =[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,
        1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,
        1,1,1,0,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1,
        1,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,
        1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,0,1,0,0,1,
        1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,
        0,0,0,0,0]

total = 306

readings = []

for index in range(1, total):
    img = cv2.imread('%d.png' %(index))

    ret,thresh = cv2.threshold(img,115,255,1)

    skin_ycrcb_mint = np.array((75,75,75))
    skin_ycrcb_maxt = np.array((221,215,215))
    skin_ycrcb = cv2.inRange(img, skin_ycrcb_mint, skin_ycrcb_maxt)

    _, contours, _= cv2.findContours(skin_ycrcb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    stopsign = False
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        area = cv2.contourArea(cnt)
        #print len(approx)

        if len(approx)==8 and area > 15000:
            #print "octogon detected"
            #print area
            cv2.drawContours(thresh,[cnt],0,255,-1)
            stopsign = True
            readings.append(1)
            break

    if stopsign == False:
        #print "No octogon"
        readings.append(0)

    #cv2.imshow('%d' %(index),thresh)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


acc = 0
for i in range(0,len(Ydata)):
    if Ydata[i] == readings[i]:
        acc += 1

print "Accuracy: ", float(acc)/float(len(readings))

import random
import numpy as np
import cv2
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import pickle

Xdata = []
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
    arr = cv2.imread('%d.png' %(index),0)
    newArr = np.asarray(arr).reshape(-1)
    Xdata.append(newArr)

    img = cv2.imread('%d.png' %(index))

    thresh_mint = np.array((75,75,75))
    thresh_maxt = np.array((221,215,215))
    thresh = cv2.inRange(img, thresh_mint, thresh_maxt)

    _, contours, _= cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

print "Shape detection accuracy: ", float(acc)/float(len(readings))

trainX = Xdata
trainY = Ydata

print "Polynomial kernel, C = 1.0, d =3 "
clf = SVC(kernel = 'poly', C = 1.0, degree = 3)
scores = cross_val_score(clf, trainX, trainY, cv = 5)
print "SVM Training accuracy", scores.mean()

model = clf.fit(trainX, trainY)
secondary = model.predict(trainX)
#print "Fitting of data in SVM", secondary

pickle.dump(clf, open('model.pkl', 'wb'))


updatedPrediction = []
for i in range(0,len(secondary)):
    if readings[i] == secondary[i]:
        updatedPrediction.append(readings[i])
    else:
        updatedPrediction.append(1)

acc = 0
for i in range(0,len(Ydata)):
    if Ydata[i] == updatedPrediction[i]:
        acc += 1

print "Final accuracy: ", float(acc)/float(len(Ydata))

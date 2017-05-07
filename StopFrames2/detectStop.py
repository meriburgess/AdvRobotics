import random
from PIL import Image
from scipy import misc
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

Xdata = []
# 1 = stop sign,  0 = no stop sign
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
cutoff = 220

for index in range(1, total):
    arr = misc.imread('%d.png' %(index))
    newArr = []
    for i in range(0,480):
        for j in range(0,640):
            val = (0.299 * arr[i][j][0]) + (0.587 * arr[i][j][1]) + (0.114 * arr[i][j][2])
            newArr.append(val)
    Xdata.append(newArr)

print "# of Images in set:", len(Xdata)
data = zip(Xdata, Ydata)
#random.shuffle(data)

train = data[0:cutoff]
test = data[cutoff:len(data)]
trainX, trainY = zip(*train)
testX, testY = zip(*test)
print trainY, testY

print "Polynomial kernel, C = 1.0, d =3 "
clfL = SVC(kernel = 'poly', C = 1.0, degree = 3)
scores = cross_val_score(clfL, trainX, trainY, cv = 5)
print "Training accuracy", scores.mean()

model = clfL.fit(trainX, trainY)
print "Test accuracy : ", clfL.score(testX, testY)
#print clfL.predict(testX)
#print testY
print model.predict(trainX)

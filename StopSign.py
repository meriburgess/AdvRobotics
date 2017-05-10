#! /usr/bin/env python
from __future__ import print_function
#from std_msgs.msg import String
import numpy as np
import roslib
import sys
import rospy
import cv2
#from std_msgs.msg import String
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from cv_bridge import CvBridge, CvBridgeError


im = cv2.imread('104.png')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
cv2.drawContours(im, contours, -1, (0,255,0), 3)
cv2.drawContours(im, contours, 3, (0,255,0), 3)
cnt = contours[4]
cv2.drawContours(im, [cnt], 0, (0,255,0), 3)

readings = []

class stop_sign:
      def __init__(self):
            self.image_pub = rospy.Publisher("stop_sign/image",Image)
            self.stop = rospy.Publisher("stop_sign/bool_to_stop",Bool)
            self.bridge = CvBridge()
            self.image_sub = rospy.Subscriber("camera/image_raw",Image,self.callback)
            self.numDetected = 0
            self.stopped = False
            self.counter = 0

      
      def callback(self,data):
            try:
                # mono8: CV_8UC1 grayscale image
                     cv_image = self.bridge.imgmsg_to_cv2(data, "mono8")
            except CvBridgeError as e:
                     print(e)


            for cnt in contours:
                  approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                  area = cv2.contourArea(cnt)
                  x,y,w,h = cv2.boundingRect(cnt)
             #print len(approx)

                  if len(approx)>=8 and (w >= 55 and h >= 65) and area > 2000:
                #print "octogon detected"
                #print area
                         cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                         cv2.drawContours(thresh,[cnt],0,255,-1)
                         stopsign = True
                         readings.append(1)
                         break
             
                  if self.numDetected > 15:
                         self.numDetected = 0
                         self.stopped = False 


             #if stopsign == False:
                #print "No octogon"
             #   readings.append(0)
                  if self.numDetected >= 5 and not self.stopped:
                          self.stopped = True
                          try:
                                 self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image_blur, "mono8"))
                                 self.stop.publish(self.stopped)
                          except CvBridgeError as e:
                                 print(e)

                  if(self.stopped):
                          self.counter += 1

                  print(self.stopped)

                  if(self.counter >= 10):
                          self.stopped = False
                          self.counter = 0
                          self.numDetected = 0

def main(args):
             s = stop_sign()
             rospy.init_node('stop_sign', anonymous=True)
             try:
                 rospy.spin()
             except KeyboardInterrupt:
                 print("Shutting down")
             cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
             
#cv2.imshow('image',im)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#!usr/bin/env python
import rospy
from sensor_msgs.msg import Range

#def callback(data):
#	print "Detected"



class Subscribe:
	def __init__(self):
		self.data = rospy.Subscriber("IR", Range, self.doStuff)
		self.prevE = 0 
		self.output = 0
		self.setPt = 0
		self.Kp = 0.5

	def doStuff(self, msg):
		#print msg.range

		#PID stuff here?
		error = self.setPt - msg.range  # msg.range == measured_value or PV
		self.output = self.Kp * error
		self.prevE = error 
		print self.output

def main():
	rospy.init_node("IR_Subscriber_Node")
	sub = Subscribe()
	rospy.spin()

if __name__ == "__main__":
	main()

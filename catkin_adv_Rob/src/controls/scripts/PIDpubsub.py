#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Range
from std_msgs.msg import Float64


class Subscribe:
	def __init__(self):
		self.IR_sub = rospy.Subscriber("IR", Range, self.doStuff)
		self.Kp = 0.5
		self.setPt = 0.36
		

	def doStuff(self, msg):
		c = msg

		#PID control loop
		error = self.setPt - c.range
		output = self.Kp * error
	
		#Now call publisher to publish PID control output		
		pub = Publish(output)
		pub.pub_msg()

class Publish:
	def __init__(self, incoming):
		self.PID_pub = rospy.Publisher("PID", Float64, queue_size=10)
		self.val = incoming

	def pub_msg(self):
		a = self.val
		self.PID_pub.publish(a) 

def main():
	rospy.init_node("PID_Node")
	sub = Subscribe()
	rospy.spin()


if __name__ == "__main__":
	main()

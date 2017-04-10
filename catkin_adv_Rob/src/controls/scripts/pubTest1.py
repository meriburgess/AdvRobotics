#!/usr/bin/env python

import rospy
import random
from sensor_msgs.msg import Range
from std_msgs.msg import Float64

# This publisher is for testing purposes! 
# Actual IR data will be published by the pololu_servo package 

class Publish:
	def __init__(self):
		self.IR_pub = rospy.Publisher("IR", Range, queue_size=10)

	def pub_msg(self):
		msg = Range()
		msg.radiation_type = 1
		msg.field_of_view = 45 
		msg.min_range = 0
		msg.max_range = 1.0
		msg.range = random.uniform(0,1)
		self.IR_pub.publish(msg) 

def main():
	rospy.init_node("IR_Publisher_node")
	rate = rospy.Rate(10)
	pub = Publish()
	while not rospy.is_shutdown():
		pub.pub_msg()
		rate.sleep()

if __name__ == '__main__':
	main()


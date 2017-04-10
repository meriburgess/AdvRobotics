#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Range

class Publish:
	def __init__(self):
		self.data = rospy.Publisher("IR", Range, queue_size=10)

	def pub_msg(self):
		# msg = range() --- values?? where do these come from actually??
		msg = Range()
		msg.radiation_type = 1
		msg.max_range = 0
		msg.min_range = 0 
		msg.field_of_view = 0
		msg.range = random.random()
		self.publish(msg) 

def main():
	rospy.init_node("IR_Publisher_node")
	rate = rospy.Rate(10)
	pub = Publish()
	while not rospy.is_shutdown():
		pub.pub_msg()
		rate.sleep()

if __name__ == '__main__':
	main()


#!/usr/bin/env python
import roslib
roslib.load_manifest('zoidberg_nav')
import rospy
import actionlib
import time

from std_msgs.msg import String, Header
from mavros_msgs.msg import State
from zoidberg_nav.msg import MoveRobotAction, MoveRobotGoal

class Command():
    """Execute basic navigation commands"""
    def __init__(self):
        """Setup a number of servers used in navigation"""

        self._ac = actionlib.SimpleActionClient('helm/move_robot',
                                                 MoveRobotAction)
        self._ac.wait_for_server()

    def change_depth(self, target_depth, timeout):
        """command a depth change
            target_depth: depth in meters, positive is down from surface
        """
        goal = MoveRobotGoal(actionID='change_depth',
                               target_depth=target_depth)
        self._ac.send_goal(goal)
        to = rospy.Duration(secs=timeout)
        res = self._ac.wait_for_result(to)
        if not res:
            rospy.loginfo("Depth change timed out")


    def change_heading(self, target_heading, timeout):
        """command a heading change
           target_heading: desired heading in Degrees, true north
        """
        goal = MoveRobotGoal(actionID='change_heading',
                               target_heading=target_heading)
        self._ac.send_goal(goal)
        to = rospy.Duration(secs=timeout)
        res = self._ac.wait_for_result(to)
        if not res:
            rospy.loginfo("Heading change timed out")

    def begin(self):
        """arm vehicle to begin moving"""
        pass

    def finished(self):
        """Shut down server"""
        self._ac.cancel_all_goals()


if __name__ == '__main__':
    try:
        rospy.init_node('navigation_client')
        co = Command()
        #co.change_depth(3, 3)
        co.change_heading(250, 100)
        #co.change_depth(1.5, 3)
        co.finished()
    except rospy.ROSInterruptException:
        rospy.loginfo("Program interrupted")

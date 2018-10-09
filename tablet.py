#!/usr/bin/python

import rospy
from naoqi_driver.naoqi_node import NaoqiNode
from distutils.version import LooseVersion
import sys
import time


class Tablet(NaoqiNode):
    def __init__(self):
        NaoqiNode.__init__(self, 'naoqi_tablet')
        self.connectNaoQi()
        rospy.loginfo("naoqi_webserver initialized")

    def connectNaoQi(self):
        rospy.loginfo("Connecting to NaoQi at %s:%d", self.pip, self.pport)
        self.systemProxy = self.get_proxy("ALSystem")
        if self.systemProxy is None:
            rospy.logerr("Could not get a proxy to ALSystem")
            exit(1)
        else:
            if LooseVersion(self.systemProxy.systemVersion()) < LooseVersion("2.4"):
                rospy.logerr("Naoqi version of your robot is " + str(self.systemProxy.systemVersion()) + ", which doesn't have a proxy to ALBackgroundMovement.")
                exit(1)
            else:
                self.tabletService = self.get_proxy("ALTabletService")
                if self.tabletService is None:
                    rospy.logerr("Could not get a proxy to ALBackgroundMovement.")
                    exit(1)
                else:
                    self.tablet()

    def tablet(self):
        print("TABLET")
        try:
            self.tabletService.enableWifi()
            time.sleep(5)
            self.tabletService.showWebview("http://146.50.60.55:5010")
        except Exception, e:
            rospy.logerr("Tablet error: ", e)


if __name__ == '__main__':
    tablet = Tablet()
    rospy.spin()

#!/usr/bin/env python

import roslib
import sys
import rospy
import cv2
import math
import numpy as np
from std_msgs.msg import *
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image,CompressedImage

from geometry_msgs.msg import Point32
from sensor_msgs.msg import LaserScan
#from pyzbar import pyzbar
import argparse
import datetime
#import imutils
import time
#import apriltag
import random
import message_filters
#import libpython_monitor_wind
#from filterpy.kalman import KalmanFilter


global flag_imageshow

flag_imageshow=1






##function to subscribe to image ros topic
def receiveimage_left(data):
    np_arr = np.fromstring(data.data, np.uint8)
    cvFrame_left = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    scale_percent = 60 # percent of original size
    width = int(cvFrame_left.shape[1] * scale_percent / 100)
    height = int(cvFrame_left.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(cvFrame_left, dim, interpolation = cv2.INTER_AREA)
    #print("here")
    global flag_imageshow
   
    #print a_time.secs
    #cvFrame = bridge.imgmsg_to_cv2(cvFrame)
    #cvFrame = cv2.flip(orig_img,-1)
    

    if(flag_imageshow==1):
        cv2.imshow('front_left',resized)
        
        #cv2.waitKey(5)
    #k = cv2.waitKey(5) & 0xff
    #if k == 27:
    #    flag_imageshow=0  #once the drone and target position are initialised and target is being detected press "esc" to close image display and increase data rate
    #    cv2.destroyAllWindows()
def receiveimage_right(data):
    np_arr = np.fromstring(data.data, np.uint8)
    cvFrame_right = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    #print("here")
    global flag_imageshow,out
    
    
    

    
    #cv2.imshow('front_right',cvFrame_right)
    out.write(cvFrame_right)
        
    #cv2.waitKey(1)
    #k = cv2.waitKey(5) & 0xff
    #if k == 27:
    #    flag_imageshow=0  #once the drone and target position are initialised and target is being detected press "esc" to close image display and increase data rate
    #    cv2.destroyAllWindows()

def receiveimage_middle(data):
    np_arr = np.fromstring(data.data, np.uint8)
    cvFrame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    #print("here")
    global flag_imageshow
    
    #print a_time.secs
    #cvFrame = bridge.imgmsg_to_cv2(cvFrame)
    #cvFrame = cv2.flip(orig_img,-1)
    cv2.imshow('front',cvFrame)
    cv2.waitKey(2)
    k = cv2.waitKey(5) & 0xff
    if k == 27:
        #flag_imageshow=0  #once the drone and target position are initialised and target is being detected press "esc" to close image display and increase data rate
        cv2.destroyAllWindows()

def receiveimage_back(data):
    np_arr = np.fromstring(data.data, np.uint8)
    cvFrame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    #print("here")
    global flag_imageshow
    
    #print a_time.secs
    #cvFrame = bridge.imgmsg_to_cv2(cvFrame)
    #cvFrame = cv2.flip(orig_img,-1)
    

    if(flag_imageshow==1):
        cv2.imshow('back',cvFrame)
        
        cv2.waitKey(2)
    k = cv2.waitKey(5) & 0xff
    if k == 27:
        
        cv2.destroyAllWindows()

    
    #print a,b,c,d,flag_tracking
    #return flag_detected,xt_image,yt_image,width,height,flag_apriltag
'''
def image_callback(imageL, imageR,imageF,imageB):
    
    np_arr = np.fromstring(imageL.data, np.uint8)
    cvFrame_left = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    np_arr = np.fromstring(imageR.data, np.uint8)
    cvFrame_right = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    np_arr = np.fromstring(imageF.data, np.uint8)
    cvFrame_front = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    np_arr = np.fromstring(imageB.data, np.uint8)
    cvFrame_back = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    scale_percent = 60 # percent of original size
    width = int(cvFrame_left.shape[1] * scale_percent / 100)
    height = int(cvFrame_left.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    cvFrame_left = cv2.resize(cvFrame_left, dim, interpolation = cv2.INTER_AREA)
    cvFrame_right = cv2.resize(cvFrame_right, dim, interpolation = cv2.INTER_AREA)
    cvFrame_back = cv2.resize(cvFrame_back, dim, interpolation = cv2.INTER_AREA)
    cvFrame_front = cv2.resize(cvFrame_front, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow('front',cvFrame_front)
    cv2.imshow('left',cvFrame_left)
    cv2.imshow('right',cvFrame_right)
    cv2.imshow('back',cvFrame_back)
    cv2.waitKey(2)
    k = cv2.waitKey(5) & 0xff
    if k == 27:
        #flag_imageshow=0  #once the drone and target position are initialised and target is being detected press "esc" to close image display and increase data rate
        cv2.destroyAllWindows()
    #rospy.loginfo("receiving frame")
    
    #imageLeft = br.imgmsg_to_cv2(imageL)
    #imageRight = br.imgmsg_to_cv2(imageR)
    
'''

def image_callback(imageL, imageR,imageF):
    
    np_arr = np.fromstring(imageL.data, np.uint8)
    cvFrame_left = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    np_arr = np.fromstring(imageR.data, np.uint8)
    cvFrame_right = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    np_arr = np.fromstring(imageF.data, np.uint8)
    cvFrame_front = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    '''
    np_arr = np.fromstring(imageB.data, np.uint8)
    cvFrame_back = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    '''
    scale_percent = 60 # percent of original size
    width = int(cvFrame_left.shape[1] * scale_percent / 100)
    height = int(cvFrame_left.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    cvFrame_left = cv2.resize(cvFrame_left, dim, interpolation = cv2.INTER_AREA)
    cvFrame_right = cv2.resize(cvFrame_right, dim, interpolation = cv2.INTER_AREA)
    #cvFrame_back = cv2.resize(cvFrame_back, dim, interpolation = cv2.INTER_AREA)
    cvFrame_front = cv2.resize(cvFrame_front, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow('front',cvFrame_front)
    cv2.imshow('left',cvFrame_left)
    cv2.imshow('right',cvFrame_right)
    #cv2.imshow('back',cvFrame_back)
    cv2.waitKey(1)
    k = cv2.waitKey(5) & 0xff
    if k == 27:
        #flag_imageshow=0  #once the drone and target position are initialised and target is being detected press "esc" to close image display and increase data rate
        cv2.destroyAllWindows()

def identifier():
    rospy.init_node('image_sub', anonymous=True)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    global out
    out = cv2.VideoWriter('right.avi', fourcc, 27.0, (640,480))
    

    #rospy.Subscriber('landing_target_info', TargetInfo, ReceiveVisionMeas)
    #rospy.Subscriber('/left/image_raw/compressed', CompressedImage, receiveimage_left,queue_size=1)
    #time.sleep(0.01)
    rospy.Subscriber('/right/image_raw/compressed', CompressedImage, receiveimage_right,queue_size=1)
    #time.sleep(0.01)
    #rospy.Subscriber('/middle/image_raw/compressed', CompressedImage, receiveimage_middle,queue_size=1)
    #time.sleep(0.01)
    #rospy.Subscriber('/back/image_raw/compressed', CompressedImage, receiveimage_back,queue_size=1)
    #time.sleep(0.01)
    
    rospy.spin()
    out.release()
def read_cameras():
    imageL = message_filters.Subscriber("/left/image_raw/compressed", CompressedImage)
    imageR = message_filters.Subscriber("/right/image_raw/compressed", CompressedImage)
    imageF = message_filters.Subscriber("/middle/image_raw/compressed", CompressedImage)
    imageB = message_filters.Subscriber("/back/image_raw/compressed", CompressedImage)

    # Synchronize images
    ts = message_filters.ApproximateTimeSynchronizer([imageL, imageR,imageF], queue_size=1, slop=0.5)
    ts.registerCallback(image_callback)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('my_node')
    try:
        read_cameras()
    except rospy.ROSInterruptException:
        pass
    
                                                                                                                                  


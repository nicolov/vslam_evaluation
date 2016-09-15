#!/usr/bin/env python

"""
Add ROS-style CameraInfo messages to an EuRoC dataset, using yaml files
from the ROS stereo calibrator:

    rosrun camera_calibration cameracalibrator.py
    --size 7x6 --square 0.06
    left:=/cam0/image_raw right:=/cam1/image_raw
"""

import os
import sys
import argparse

import rosbag
from camera_info_manager import CameraInfoManager


def parse_args():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description='Inject CameraInfo messages into euroc datasets')

    parser.add_argument('-l', type=str, default='left.yaml', help='Path to yaml file for cam0')
    parser.add_argument('-r', type=str, default='right.yaml', help='Path to yaml file for cam1')
    parser.add_argument('bagfile', type=str, help='path to the bagfile')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    left_cm = CameraInfoManager(namespace='left')
    left_cm.setURL('file://{}'.format(os.path.abspath(args.l)))
    left_cm.loadCameraInfo()
    left_msg = left_cm.getCameraInfo()

    right_cm = CameraInfoManager(namespace='right')
    right_cm.setURL('file://{}'.format(os.path.abspath(args.r)))
    right_cm.loadCameraInfo()
    right_msg = right_cm.getCameraInfo()

    in_bag = rosbag.Bag(args.bagfile)

    in_basename = os.path.splitext(
        os.path.basename(os.path.abspath(args.bagfile)))[0]
    out_filepath = os.path.join(
        os.path.dirname(os.path.abspath(args.bagfile)),
        in_basename + '_wcaminfo.bag')

    print 'Writing to', out_filepath

    with rosbag.Bag(out_filepath, 'w') as out_bag:
        for topic, msg, t in in_bag.read_messages():
            if topic == '/cam0/image_raw':
                left_msg.header = msg.header
                out_bag.write('/cam/left/camera_info', left_msg, t)
                out_bag.write('/cam/left/image_raw', msg, t)
            elif topic == '/cam1/image_raw':
                right_msg.header = msg.header
                out_bag.write('/cam/right/camera_info', right_msg, t)
                out_bag.write('/cam/right/image_raw', msg, t)
            else:
                out_bag.write(topic, msg, t)


if __name__ == "__main__":
    main()
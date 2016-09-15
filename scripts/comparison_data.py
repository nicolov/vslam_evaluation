#!/usr/bin/env python

import os, sys, inspect
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

from trajectory_toolkit.TimedData import TimedData
from trajectory_toolkit.Plotter import Plotter
from trajectory_toolkit.VIEvaluator import VIEvaluator
from trajectory_toolkit import Quaternion
from trajectory_toolkit import Utils
from trajectory_toolkit import RosDataAcquisition


def load_one_comparison(bag_file_name, odometry_topic_name):
    td_visual = TimedData()
    td_vicon = TimedData()

    eval = VIEvaluator()
    eval.bag = bag_file_name
    eval.odomTopic = odometry_topic_name
    eval.gtFile = bag_file_name
    eval.gtTopic = '/vicon/firefly_sbx/firefly_sbx'
    # Align body frames to the same inertial (not viceversa)
    eval.alignMode = 0
    # Compute analytical derivatives for visual data as well
    eval.derMode = 0

    eval.initTimedData(td_visual)
    eval.initTimedDataGT(td_vicon)
    eval.acquireData()
    eval.acquireDataGT()
    eval.getAllDerivatives()
    eval.alignTime()
    eval.alignBodyFrame()
    eval.alignInertialFrame()
    eval.getYpr()
    eval.evaluateSigmaBounds()

    return td_visual, td_vicon


def make_bag_path(filename):
    return os.path.join(os.path.expanduser('~'), 'vslam_comparison', filename)


comparisons = (
    ('ORB SLAM', make_bag_path('orb_stereo_false_traj.bag'), '/orb/odometry'),
    ('Rovio', make_bag_path('rovio_traj.bag'), '/rovio/odometry'),
    ('ORB Odom', make_bag_path('orb_stereo_true_traj.bag'), '/orb/odometry'),
    ('Viso2', make_bag_path('viso2_traj.bag'), '/stereo_odometer/odometry'),
)
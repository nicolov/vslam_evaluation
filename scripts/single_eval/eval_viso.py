#!/usr/bin/env python

import os, sys, inspect
import numpy as np

from trajectory_toolkit.TimedData import TimedData
from trajectory_toolkit.Plotter import Plotter
from trajectory_toolkit.VIEvaluator import VIEvaluator
from trajectory_toolkit import Quaternion
from trajectory_toolkit import Utils
from trajectory_toolkit import RosDataAcquisition

plotPos = True
plotVel = True
plotAtt = False
plotYpr = False
plotRor = False
plotRon = False

td_visual = TimedData()
td_vicon = TimedData()

def make_bag_path(filename):
    return os.path.join(os.path.expanduser('~'), 'vslam_comparison', filename)

rovioEvaluator = VIEvaluator()
rovioEvaluator.bag = make_bag_path('viso2_traj.bag')
rovioEvaluator.odomTopic = '/stereo_odometer/odometry'
rovioEvaluator.gtFile = make_bag_path('viso2_traj.bag')
rovioEvaluator.gtTopic = '/vicon/firefly_sbx/firefly_sbx'
rovioEvaluator.alignMode = 1

rovioEvaluator.initTimedData(td_visual)
rovioEvaluator.initTimedDataGT(td_vicon)
rovioEvaluator.acquireData()
rovioEvaluator.acquireDataGT()
rovioEvaluator.getAllDerivatives()
rovioEvaluator.alignTime()
rovioEvaluator.alignBodyFrame()
rovioEvaluator.alignInertialFrame()
rovioEvaluator.getYpr()
rovioEvaluator.evaluateSigmaBounds()
   
if plotPos: # Position plotting
    plotterPos = Plotter(-1, [3,1],'Position',['','','time[s]'],['x[m]','y[m]','z[m]'],10000)
    if rovioEvaluator.doCov:
        plotterPos.addDataToSubplotMultiple(td_visual, 'posSm', [1,2,3], ['r--','r--','r--'], ['','',''])
        plotterPos.addDataToSubplotMultiple(td_visual, 'posSp', [1,2,3], ['r--','r--','r--'], ['','',''])
    plotterPos.addDataToSubplotMultiple(td_visual, 'pos', [1,2,3], ['r','r','r'], ['','',''])
    plotterPos.addDataToSubplotMultiple(td_vicon, 'pos', [1,2,3], ['b','b','b'], ['','',''])

if plotVel: # Velocity plotting
    plotterVel = Plotter(-1, [3,1],'Robocentric Velocity',['','','time[s]'],['$v_x$[m/s]','$v_y$[m/s]','$v_z$[m/s]'],10000)
    plotterVel.addDataToSubplotMultiple(td_visual, 'vel', [1,2,3], ['r','r','r'], ['','',''])
    plotterVel.addDataToSubplotMultiple(td_vicon, 'vel', [1,2,3], ['b','b','b'], ['','',''])
    
if plotAtt: # Attitude plotting
    plotterAtt = Plotter(-1, [4,1],'Attitude Quaternion',['','','','time[s]'],['w[1]','x[1]','y[1]','z[1]'],10000)
    plotterAtt.addDataToSubplotMultiple(td_visual, 'att', [1,2,3,4], ['r','r','r','r'], ['','','',''])
    plotterAtt.addDataToSubplotMultiple(td_vicon, 'att', [1,2,3,4], ['b','b','b','b'], ['','','',''])

if plotYpr: # Yaw-pitch-roll plotting
    plotterYpr = Plotter(-1, [3,1],'Yaw-Pitch-Roll Decomposition',['','','time[s]'],['roll[rad]','pitch[rad]','yaw[rad]'],10000)
    if rovioEvaluator.doCov:
        plotterYpr.addDataToSubplotMultiple(td_visual, 'yprSm', [1,2,3], ['r--','r--','r--'], ['','',''])
        plotterYpr.addDataToSubplotMultiple(td_visual, 'yprSp', [1,2,3], ['r--','r--','r--'], ['','',''])
    plotterYpr.addDataToSubplotMultiple(td_visual, 'ypr', [1,2,3], ['r','r','r'], ['','',''])
    plotterYpr.addDataToSubplotMultiple(td_vicon, 'ypr', [1,2,3], ['b','b','b'], ['','',''])
    
if plotRor: # Rotational rate plotting
    plotterRor = Plotter(-1, [3,1],'Rotational Rate',['','','time[s]'],['$\omega_x$[rad/s]','$\omega_y$[rad/s]','$\omega_z$[rad/s]'],10000)
    plotterRor.addDataToSubplotMultiple(td_visual, 'ror', [1,2,3], ['r','r','r'], ['','',''])
    plotterRor.addDataToSubplotMultiple(td_vicon, 'ror', [1,2,3], ['b','b','b'], ['','',''])

if plotRon: # Plotting rotational rate norm
    plotterRon = Plotter(-1, [1,1],'Norm of Rotational Rate',['time [s]'],['Rotational Rate Norm [rad/s]'],10000)
    plotterRon.addDataToSubplot(td_visual, 'ron', 1, 'r', 'rovio rotational rate norm')
    plotterRon.addDataToSubplot(td_vicon, 'ron', 1, 'b', 'vicon rotational rate norm')

raw_input("Press Enter to continue...")
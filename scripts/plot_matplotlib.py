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


plotterPos = Plotter(-1, [1,1],'',['time[s]'],['x[m]'],10000)
plotterPos.legendLoc = 'center'

for i, (label, bag_file_name, odometry_topic_name) in enumerate(comparisons):
    td_visual, td_vicon = load_one_comparison(bag_file_name, odometry_topic_name)
    #plotterPos.addDataToSubplotMultiple(td_visual, 'pos', [1, 3], 2*[''], 2*[label])
    plotterPos.addDataToSubplot(td_visual, 1, 1, '', label)
    #plotterPos.addDataToSubplot(td_visual, 3, 3, '', label)

    if i == 0:
        # Only plot ground truth once
        plotterPos.addDataToSubplot(td_vicon, 1, 1, '', 'Truth')
        #plotterPos.addDataToSubplot(td_vicon, 3, 3, '', 'Truth')

if True:
    plotterPos.setFigureSize(9, 5)
    plt.tight_layout()
    plt.savefig('comparison.pdf', bbox_inches = 'tight')
    plt.savefig('comparison.png', bbox_inches = 'tight')

raw_input()
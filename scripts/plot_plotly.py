#!/usr/bin/env python

import os, sys, inspect
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import rospkg
from IPython import embed

from comparison_data import *

def position_comparison():
    plot_layout = go.Layout(
        title='X position comparison',
        xaxis={'title': 'Time [s]'},
        yaxis={'title': 'X position [m]'}
    )

    plot_data = []

    for i, (label, bag_file_name, odometry_topic_name) in enumerate(comparisons):
        td_visual, td_vicon = load_one_comparison(bag_file_name, odometry_topic_name)

        plot_data.append(
            go.Scatter(x=td_visual.col(0)[::4],
                y=td_visual.col(1)[::4],
                mode='lines+markers',
                name=label,
                marker={'maxdisplayed': 150}))

        if i == 0:
            # Only plot ground truth once
            plot_data.append(
                go.Scatter(x=td_vicon.col(0)[::20],
                    y=td_vicon.col(1)[::20],
                    mode='lines+markers',
                    name='Truth',
                    marker={'maxdisplayed': 150}))

    fig = go.Figure(data=plot_data, layout=plot_layout)
    url = py.plot(fig, filename='vslam_eval_x_pos')


def running_times():
    rospack = rospkg.RosPack()
    data_path = os.path.join(rospack.get_path('vslam_evaluation'), 'out')
    df = pd.read_csv(os.path.join(data_path, 'runtimes.txt'),
        header=None,
        index_col=0)

    bars = []

    for col_idx in df:
        this_stack = df[col_idx].dropna()
        bars.append(
            go.Bar(
                x=this_stack.index,
                y=this_stack.values,
                name='Thread {}'.format(col_idx)))

    layout = go.Layout(
        barmode='stack',
        yaxis={'title': 'Running time [s]'})

    fig = go.Figure(data=bars, layout=layout)

    url = py.plot(fig, filename='vslam_eval_run_times')


if __name__ == "__main__":
    # position_comparison()
    running_times()

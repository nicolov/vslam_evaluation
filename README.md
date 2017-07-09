# Visual SLAM evaluation code

<img src="https://github.com/nicolov/vslam_evaluation/raw/master/example_plot.png" width="500" style="text-align: center"/>

Code for the evaluation of open-source visual-odometry/SLAM systems I wrote about [in my blog](http://nicolovaligi.com/open-source-visual-slam-evaluation.html). You'll need to install the packages separately, as this repo only contains the configurations and ROS launch file needed to reproduce my results.

- *viso2*: [repo](https://github.com/srv/viso2)
- *rovio*: [repo](https://github.com/ethz-asl/rovio)
- *ORB-SLAM2*: [repo](https://github.com/raulmur/ORB_SLAM2)

Remember that all of these packages greatly benefit from compiler optimization, and need the appropriate `CMake` flags when building:

```
catkin build package --cmake-args -DCMAKE_BUILD_TYPE=Release
```

## Running

First, download the `V1_01_easy.bag` from the [dataset page](http://projects.asl.ethz.ch/datasets/doku.php?id=kmavvisualinertialdatasets) into your home folder. Each of the launch files will record its output into a new bag in the `out` folder:

```
roslaunch vslam_evaluation orbslam.launch
roslaunch vslam_evaluation rovio.launch
roslaunch vslam_evaluation viso2.launch
```

You can then run the plotting code (both Matplotlib and Plotly).

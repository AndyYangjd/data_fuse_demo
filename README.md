# data_fuse_demo
create a demo about data-fuse using nuScenes dataset

注：此项目已暂停更新，使用Cpp重构此项目，并为了push, pull速度，托管在Gitee: https://gitee.com/andyangj/setSail.git ，其中 feature为最新的分支

## language, Ide, 3rd-Dependency
lan:
- Python:3.8: extract info
- Cpp: support c++11
- julia: 1.5.1, test the algorithm and visualize

Ide:
- vscode
- vs2019 community
- pycharm

Python-Dep:
- matplotlib
- json
- nuscenes-devkit
- torch.etc(what yolov5 needs)
- PyQt5
- numpy
- pyqtgraph
- xlrd3

Cpp-Dep:
- Eigne3

Julia-Dep:
- LinearAlgeora
- DataFrames
- XLSX
- Plots
- PyPlot

## visualization
Source code store in src/visualization_simulator
- run: runing gui.py will open this program
- data-file: open data/radar_points.xlsx

## src/file-role
- extract_one_scene.py: extract can-front and radar-front file-path in the first scene
- convert_radarPcd_to_ascii.py: convert the file-format of Radar-pcd from binary to ascii, so we can parse the info about points, such as Position, relative-Velocity..
- geometry_transform.cpp: get the Transform-matrix of cam and radar
- vertify_line.jl: vertify the uv-points in the horitional line 
- coord_trans.cpp: supply a function to transfrom pos between sensor and car
- detect.py: based on yolov5 sound code detect.py and make it print BBOX coordinate,you can replace detect.py and general.py in yolov5 sound code to detect your image/video
- general.py: based on yolov5 general.py sound code has a little change.

## data/file-role
- calibration_parameter.xlsx: the calibration parameter of front camera and radar.
- extracted_data.json: the out-put of extrac_one-scene.py
- tranform_matrix.csv: the out-put of geometry_transform.cpp
- result_json: the out-put of detect.py ,image detection coordinate
- image_detection_result: image detection results

## Contributors
- Andy.Yang: process the data of radar
- Cheng Shuhui: process the data of images

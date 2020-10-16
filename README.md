# data_fuse_demo
create a demo about data-fuse using nuScenes dataset

# language, Ide, 3rd-Dependency
lan:
- Python:3.8: extract info
- Cpp: support c++11
- julia: 1.5.1

Ide:
- vscode
- vs2019 community

Python-Dep:
- matplotlib
- json
- nuscenes-devkit

Cpp-Dep:
- Eigne3

Julia-Dep:
- LinearAlgeora

## src/file-role
- extract_one_scene.py: extract can-front and radar-front file-path in the first scene
- convert_radarPcd_to_ascii.py: convert the file-format of Radar-pcd from binary to ascii, so we can parse the info about points, such as Position, relative-Velocity..
- geometry_transform.cpp: get the Transform-matrix of cam and radar
- vertify_line.jl: vertify the uv-points in the horitional line 
- coord_trans.cpp: supply a function to transfrom pos between sensor and car

## data/file-role
- calibration_parameter.xlsx: the calibration parameter of front camera and radar.
- extracted_data.json: the out-put of extrac_one-scene.py
- tranform_matrix.csv: the out-put of geometry_transform.cpp
# data_fuse_demo
create a demo about data-fuse using nuScenes dataset

# language, Ide, 3rd-Dependency
lan:
- Python3.8: extract info
- Cpp: version support c++11

Ide:
- vscode
- vs2019 community

Python-Dep:
- matplotlib
- json
- nuscenes-devkit

Cpp-Dep:
- Eigne3

## file-role
- extract_one_scene.py: extract can-front and radar-front file-path in the first scene
- convert_radarPcd_to_ascii.py: convert the file-format of Radar-pcd from binary to ascii, so we can parse the info about points, such as Position, relative-Velocity..
- geometry_transform.cpp: get the Transform-matrix of cam and radar
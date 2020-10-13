# convert_radarPcd_to_ascii.py
# convert the binary pcd file of radar to ascii

import os
from pathlib import Path
import subprocess


def runCmd(files_path_, des_path_):
    for file_path in files_path_:
        command = "pcl_convert_pcd_ascii_binary"
        file_name = str(file_path.name)
        abs_des_path = des_path_ + file_name

        cmd_all = command + " " + str(file_path) + " " + abs_des_path + ' 0'

        ret = subprocess.run(cmd_all,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             encoding="utf-8")
        if ret.returncode == 0:
            print(f"success: {file_name}")
        else:
            print("error:", ret)
            raise IOError(f"convert radar data {file_name} fail")


def getAllPcd(source_path_):
    source_path = Path(source_path_)
    return [file for file in source_path.iterdir()]


if __name__ == "__main__":
    current_path = os.path.abspath(__file__)
    current_parent2_path = Path(current_path).parents[1]

    rel_source_path = "/data/data_no_anno/radar/"
    abs_source_path = str(current_parent2_path) + rel_source_path

    rel_des_path = "/data/data_no_anno/radar_ascii/"
    abs_des_path = str(current_parent2_path) + rel_des_path

    path_list = getAllPcd(abs_source_path)
    runCmd(path_list, abs_des_path)
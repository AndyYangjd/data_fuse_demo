import numpy as np
import json
import os

def load_pcd_data(file_path):
	pts = []
	f = open(file_path, 'r')
	data = f.readlines()
	data = [book.strip('\n') for book in data]
	data = [book.split(' ') for book in data]
	f.close()

	points = data[9]
	fields = data[2]

	pts_num = eval(points[-1])
	for line in data[11:]:
		i = 1
		data_dict = {}
		for coord in line:
			label = fields[i]
			data_dict[str(label)] = coord
			i = i + 1
		pts.append(data_dict)

	num_list = []
	for i in range(1, 126):
		num_list.append(i)

	final_result = dict(zip(num_list, pts))

	return final_result


final_list = []
final_dict ={}
for root, dirs, files in os.walk(r"F:\\project\\data_fuse_demo\\data\data_no_anno\\radar_ascii"):
    for file in files:
        # 获取文件所属目录
        #print(root)
        # 获取文件路径
        file_path = os.path.join(root, file)
        result = load_pcd_data(file_path)
        final_dict[file] = result

file_name = 'result_json'
with open(file_name, 'w', encoding='UTF-8')as f:
    json.dump(final_dict, f, indent=4, ensure_ascii=False)

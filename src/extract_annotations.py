# extract_annotations.py
#
# extract Anno-Info from nuScenes-dataset
#

import os
import json

from nuscenes.nuscenes import NuScenes

nuscens_dataset_pth = r"F:\datasets\data\sets\nuscenes"
nusc = NuScenes(version='v1.0-mini',
                dataroot=nuscens_dataset_pth,
                verbose=True)

extracted_data = []

# get the first scene
my_scene = nusc.scene[0]
first_sample_token = my_scene['first_sample_token']

current_sample = nusc.get('sample', first_sample_token)
sample_id = 0

while not current_sample['next'] == '':
    current_sample_anno_list = current_sample['anns']

    current_anns_in_current_sample = {
        'sample_id': sample_id,
        'num_anns': len(current_sample_anno_list),
        'translation': [],
        'rotation': [],
        'size': [],
        'category': []
    }

    for anns in current_sample_anno_list:
        anns_metadata = nusc.get('sample_annotation', anns)

        anns_translation = anns_metadata['translation']
        anns_size = anns_metadata['size']
        anns_rotation = anns_metadata['rotation']

        anns_instance_token = anns_metadata['instance_token']
        anns_instance_metadata = nusc.get('instance', anns_instance_token)
        anns_category_token = anns_instance_metadata['category_token']
        anns_category_metadata = nusc.get('category', anns_category_token)
        anns_category_name = anns_category_metadata['name']

        current_anns_in_current_sample['translation'].append(anns_translation)
        current_anns_in_current_sample['size'].append(anns_size)
        current_anns_in_current_sample['rotation'].append(anns_rotation)
        current_anns_in_current_sample['category'].append(anns_category_name)

    extracted_data.append(current_anns_in_current_sample)

    current_sample_token = current_sample['next']
    current_sample = nusc.get('sample', current_sample_token)
    sample_id += 1

prj_pth = os.path.dirname(os.path.dirname(__file__))
dest_pth = os.path.join(prj_pth, "data", "radar_process")
print(dest_pth)

# with open("src/extracted_anns_data.json", "w") as f:
#     try:
#         json.dump(extracted_data, f, indent=4, separators=(',', ': '))
#     except IOError:
#         print("write json Error")
#     else:
#         print("write to json succeed")
# extract_one_scene.py
# extract can-front and radar-front file-path in the first scene

import json
import os

from pathlib import Path
import matplotlib

from nuscenes.nuscenes import NuScenes

nusc = NuScenes(version='v1.0-mini',
                dataroot=r'D:\datasets\data\sets\nuscenes',
                verbose=True)

my_scene = nusc.scene[0]

first_sample_token = my_scene['first_sample_token']

extracted_data = {
    'cam_front': {
        'timestamp': [],
        'file_name': [],
        'ego_pose': {
            'rotation': [],
            'translation': []
        },
        'calibrated_sensor': {
            'rotation': [],
            'translation': []
        },
        'camera_intrinsic': []
    },
    'radar_front': {
        'timestamp': [],
        'file_name': [],
        'ego_pose': {
            'rotation': [],
            'translation': []
        },
        'calibrated_sensor': {
            'rotation': [],
            'translation': []
        },
    }
}

#相机和雷达的sample_token相同，但是ego_pose, timestamp是不同的
sensors = ['CAM_FRONT', 'RADAR_FRONT']
for sensor_channel in sensors:
    current_sample = nusc.get('sample', first_sample_token)

    while not current_sample['next'] == '':
        front_data = nusc.get('sample_data',
                              current_sample['data'][sensor_channel])

        timestamp = front_data['timestamp']

        file_name = front_data['filename']

        ego_pose_token = front_data['ego_pose_token']
        ego_pose = nusc.get('ego_pose', ego_pose_token)
        ego_rotation_quat4f = ego_pose['rotation']
        ego_translation_3f = ego_pose['translation']

        calibrated_sensor_token = front_data['calibrated_sensor_token']
        calibrated_sensor = nusc.get('calibrated_sensor',
                                     calibrated_sensor_token)
        calibrated_sensor_translation_3f = calibrated_sensor['translation']
        calibrated_sensor_rotation_quat4f = calibrated_sensor['rotation']

        sensor_modality = front_data['sensor_modality']

        if sensor_modality == 'camera':
            calibrated_sensor_cam_intri = calibrated_sensor['camera_intrinsic']

            extracted_data['cam_front']['timestamp'].append(timestamp)
            extracted_data['cam_front']['file_name'].append(file_name)
            extracted_data['cam_front']['ego_pose']['rotation'].append(
                ego_rotation_quat4f)
            extracted_data['cam_front']['ego_pose']['translation'].append(
                ego_translation_3f)
            extracted_data['cam_front']['calibrated_sensor'][
                'rotation'].append(calibrated_sensor_rotation_quat4f)
            extracted_data['cam_front']['calibrated_sensor'][
                'translation'].append(calibrated_sensor_translation_3f)
            extracted_data['cam_front']['camera_intrinsic'].append(
                calibrated_sensor_cam_intri)

        elif sensor_modality == 'radar':
            extracted_data['radar_front']['timestamp'].append(timestamp)
            extracted_data['radar_front']['file_name'].append(file_name)
            extracted_data['radar_front']['ego_pose']['rotation'].append(
                ego_rotation_quat4f)
            extracted_data['radar_front']['ego_pose']['translation'].append(
                ego_translation_3f)
            extracted_data['radar_front']['calibrated_sensor'][
                'rotation'].append(calibrated_sensor_rotation_quat4f)
            extracted_data['radar_front']['calibrated_sensor'][
                'translation'].append(calibrated_sensor_translation_3f)
        else:
            raise IndexError("the modality of sensor must be camera or radar")

        current_sample_token = current_sample['next']
        current_sample = nusc.get('sample', current_sample_token)

extracted_data_json = json.dumps(extracted_data, )

prj_pth = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
dest_pth = os.path.join(prj_pth, "data", "extracted_sensor_data.json")

with open(dest_pth, "w") as f:
    try:
        json.dump(extracted_data, f, indent=4, separators=(',', ': '))
    except IOError:
        print("write json Error")
    else:
        print("write to json succeed")
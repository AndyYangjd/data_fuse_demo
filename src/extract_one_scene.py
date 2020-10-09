# extract_one_scene.py
# extract can-front and radar-front file-path in the first scene

import matplotlib

from nuscenes.nuscenes import NuScenes

nusc = NuScenes(version='v1.0-mini',
                dataroot='D:\\Library\\Thesis\\datasets\\data\\sets\\nuscenes',
                verbose=True)

my_scene = nusc.scene[0]

first_sample_token = my_scene['first_sample_token']

current_sample = nusc.get('sample', first_sample_token)
cam_file_paths = []
radar_file_paths = []

while not current_sample['next'] == '':
    sensors = ['CAM_FRONT', 'RADAR_FRONT']

    #相机和雷达的sample_token相同，但是ego_pose, timestamp是不同的
    for id_sensor, name_sensor in enumerate(sensors):
        front_data = nusc.get('sample_data',
                              current_sample['data'][sensors[id_sensor]])

        ego_pose_token = front_data['ego_pose_token']
        ego_pose = nusc.get('ego_pose', ego_pose_token)
        ego_rotation_quat4f = ego_pose['rotation']
        ego_translation_3f = ego_pose['translation']

        calibrated_sensor_token = front_data['calibrated_sensor_token']
        calibrated_sensor = nusc.get('calibrated_sensor',
                                     calibrated_sensor_token)
        calibrated_sensor_translation_3f = calibrated_sensor['translation']
        calibrated_sensor_rotation_quat4f = calibrated_sensor['rotation']

        sensor_token = calibrated_sensor['sensor_token']
        sensor = nusc.get('sensor', sensor_token)
        sensor_modality = sensor['modality']

        if sensor_modality == 'camera':
            calibrated_sensor_cam_intri = calibrated_sensor['camera_intrinsic']
            cam_file_paths.append(front_data['filename'])
        elif sensor_modality == 'radar':
            radar_file_paths.append(front_data['filename'])
        else:
            print("Error: the modality of sensor must be camera or radar")

    current_sample_token = current_sample['next']
    current_sample = nusc.get('sample', current_sample_token)

print(f"Cam-Path:{len(cam_file_paths)}")
for i in cam_file_paths:
    print(i)

print(f"Radar-Path:{len(radar_file_paths)}")
for i in radar_file_paths:
    print(i)
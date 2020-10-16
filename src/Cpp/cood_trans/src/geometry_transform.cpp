#include <iostream>
#include "coord_trans.hpp"

int main(void)
{
	Vector3d cam_trans_m(
		1.70079118954,
		0.0159456324149,
		1.51095763913);
	Quaterniond cam_rotation_quat(
		0.4998015430569128,
		-0.5030316162024876,
		0.4997798114386805,
		-0.49737083824542755
	);
	Matrix3d cam_intri_m;
	cam_intri_m <<
		1266.417203046554,
		0.0,
		816.2670197447984,
		0.0,
		1266.417203046554,
		491.50706579294757,
		0.0,
		0.0,
		1.0;
	
	Vector3d radar_trans_m(
		3.412,
		0.0,
		0.5);
	Quaterniond radar_rotation_quat(
		0.9999984769132877,
		0.0,
		0.0,
		0.0017453283658983088
	);

	Isometry3d cam2car_T_mat = Isometry3d::Identity();
	cam2car_T_mat.rotate(cam_rotation_quat);
	cam2car_T_mat.pretranslate(cam_trans_m);

	Isometry3d radar2car_T_mat = Isometry3d::Identity();
	radar2car_T_mat.rotate(radar_rotation_quat);
	radar2car_T_mat.pretranslate(radar_trans_m);

	array<Isometry3d, 2> T_sensor2car_list{ cam2car_T_mat, radar2car_T_mat };

	Isometry3d car2cam_T_mat = cam2car_T_mat.inverse();
	Isometry3d car2radar_T_mat = radar2car_T_mat.inverse();

	array<Isometry3d, 2> T_car2sensor_list{ car2cam_T_mat, car2radar_T_mat };

	string file_name = "tranform_matrix.csv";
	ofstream outfile;

	bool st_write_csv_bool;
	st_write_csv_bool=writeToCSV(outfile, file_name, T_sensor2car_list);

	if(!st_write_csv_bool)
		cout << "write data fail:" << file_name;

	Quaterniond ego_pose_rotation_quat(
		0.5721129977125774,
		-0.0014962022442161157,
		0.011922678049447764,
		-0.8200867813684729
	);
	Vector3d ego_pose_translation_m(
		411.25243634487725,
		1180.7511754315697,
		0.0
	);

	Isometry3d car2world_T_mat = Isometry3d::Identity();
	car2world_T_mat.rotate(ego_pose_rotation_quat);
	car2world_T_mat.pretranslate(ego_pose_translation_m);

	Isometry3d world2car_T_mat = car2world_T_mat.inverse();

	Vector3d posWorld_anns_center{ 399.863, 1143.574, 0.738 };
	Vector3d posCar_anns_center;
	posCar_anns_center = transCoord(
		posWorld_anns_center, 
		world2car_T_mat
);
	cout << posCar_anns_center;

	return 0;
}
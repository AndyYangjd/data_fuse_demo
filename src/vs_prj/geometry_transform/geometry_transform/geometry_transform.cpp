#include <iostream>
#include "include/coord_trans.hpp"

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

	Vector3d pos_car1{ 5, 0.5, 0.5 };
	Vector3d pos_cam1;
	pos_cam1 = transCoord(pos_car1, T_car2sensor_list[0], cam_intri_m);
	cout << pos_cam1;

	return 0;
}
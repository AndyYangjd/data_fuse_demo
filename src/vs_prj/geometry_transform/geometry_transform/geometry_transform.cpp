#include <iostream>
#include <Eigen/Core>
#include <Eigen/Geometry>
#include <iostream>
#include <fstream>
#include <string>
#include <array>

using namespace std;
using namespace Eigen;

bool writeToCSV(
	ofstream & outfile_, 
	const string & file_name_, 
	const array<Isometry3d, 2> & T_list_)
{
	bool st_return{ true };
	outfile_.open(file_name_, ios::out);

	for (auto T : T_list_)
	{
		const int num_rows = T.matrix().rows();
		const int num_cols = T.matrix().cols();

		for (int row = 0; row < num_rows; row++)
		{
			for (int col = 0; col < num_cols; col++)
			{
				outfile_ << T(row, col);
				outfile_ << ",";
			}
			outfile_ << endl;
		}
		outfile_ << endl;
	}
	outfile_.close();

	return st_return;
}

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

	Matrix3d cam_rotation_mat =
		cam_rotation_quat.toRotationMatrix();
	Matrix3d radar_rotation_mat =
		radar_rotation_quat.toRotationMatrix();

	Isometry3d cam_T_mat = Isometry3d::Identity();
	cam_T_mat.rotate(cam_rotation_quat);
	cam_T_mat.pretranslate(cam_trans_m);

	Isometry3d radar_T_mat = Isometry3d::Identity();
	radar_T_mat.rotate(radar_rotation_quat);
	radar_T_mat.pretranslate(radar_trans_m);

	cout << "Cam:" << endl;
	cout << cam_T_mat.matrix() << endl;
	
	cout << "radar:" << endl;
	cout << radar_T_mat.matrix() << endl;
	
	string file_name = "tranform_matrix.csv";
	ofstream outfile;

	array<Isometry3d, 2> T_list{cam_T_mat, radar_T_mat};
	cout << cam_T_mat.matrix() << endl;

	bool st_write_csv_bool;
	st_write_csv_bool=writeToCSV(outfile, file_name, T_list);

	if(!st_write_csv_bool)
		cout << "write data fail:" << file_name;

	return 0;
}

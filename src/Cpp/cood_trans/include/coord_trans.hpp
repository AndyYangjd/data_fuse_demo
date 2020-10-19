#pragma once

#include <iostream>
#include <Eigen/Core>
#include <Eigen/Geometry>
#include <fstream>
#include <string>
#include <array>

using namespace std;
using namespace Eigen;

bool writeToCSV(
	ofstream & outfile_,
	const string & file_name_,
	const array<Isometry3d, 2> & T_list_
);


Vector3d transCoord(
	const Vector3d & pos_,
	const Isometry3d & T_,
	const Matrix3d & Mat_intri_=Matrix3d::Zero()
);

array<Vector3d, 4> getHorPlanePosAnns(const Vector3d& anns_size_);

#include "coord_trans.hpp"

bool writeToCSV(
	ofstream & outfile_,
	const string & file_name_,
	const array<Isometry3d, 2> & T_list_
)
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

Vector3d transCoord(
	const Vector3d & pos_,
	const Isometry3d & T_,
	const Matrix3d & Mat_intri_
)
{
	Vector3d return_pos;
	
	if (Mat_intri_.isZero())

		return_pos = T_ * pos_;
	else
		return_pos = Mat_intri_ * T_ * pos_;

	return return_pos;
}

array<Vector3d, 4> getHorPlanePosAnns(const Vector3d & anns_size_)
{
	float x, y, z;
	x = anns_size_[0];
	y = anns_size_[1];
	z = anns_size_[2];

	Vector3d pos1{ x /2, y/2, -z/2};
	Vector3d pos2{ -x /2, y/2, -z/2 };
	Vector3d pos3{ x/2, -y / 2, -z/2 };
	Vector3d pos4{ -x/2, -y / 2, -z/2 };

	array<Vector3d, 4> pos_list{
		pos1, pos2, pos3, pos4
	};

	return pos_list;
}

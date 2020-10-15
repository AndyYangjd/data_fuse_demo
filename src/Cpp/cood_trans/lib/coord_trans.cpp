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
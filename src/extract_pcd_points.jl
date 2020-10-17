#= extract_pcd_points.jl
extract the radar-points in pcd file(ascii) =#

using XLSX;

prj_path = dirname(dirname(@__FILE__))
data_path = prj_path * raw"\data\data_no_anno\radar_ascii";

xls_file_path = prj_path * raw"\data\radar_points.xlsx";
XLSX.openxlsx(xls_file_path, mode="w") do xf
    for file_id in 1:38
        file_path = data_path * "\\$file_id.pcd"
        f = open(file_path, "r");
        n = countlines(f)

        # skip the first 12 lines
        seekstart(f)
        for i = 1:12
            readline(f)
        end

        data = Array{Float64}(undef, n - 12, 18)
        for i = 13:n
            row_id = i - 12;
            str_list = split(readline(f), " ")

            x = parse(Float64, str_list[1]);
            data[row_id, 1] = x;

            y = parse(Float64, str_list[2]);
            data[row_id, 2] = y;

            z = parse(Float64, str_list[3]);
            data[row_id, 3] = z;

            dyn_prop = parse(Float64, str_list[4]);
            data[row_id, 4] = dyn_prop;

            id = parse(Float64, str_list[5]);
            data[row_id, 5] = id;

            rcs = parse(Float64, str_list[6]);
            data[row_id, 6] = rcs;

            vx = parse(Float64, str_list[7]);
            data[row_id, 7] = vx;

            vy = parse(Float64, str_list[8]);
            data[row_id, 8] = vy;

            vx_comp = parse(Float64, str_list[9]);
            data[row_id, 9] = vx_comp;

            vy_comp = parse(Float64, str_list[10]);
            data[row_id, 10] = vy_comp;

            is_quality_valid = parse(Float64, str_list[11]);
            data[row_id, 11] = is_quality_valid;

            ambig_state = parse(Float64, str_list[12]);
            data[row_id, 12] = ambig_state;

            x_rms = parse(Float64, str_list[13]);
            data[row_id, 13] = x_rms;

            y_rms = parse(Float64, str_list[14]);
            data[row_id, 14] = y_rms;

            invalid_state = parse(Float64, str_list[15]);
            data[row_id, 15] = invalid_state;

            pdh0 = parse(Float64, str_list[16]);
            data[row_id, 16] = pdh0;

            vx_rms = parse(Float64, str_list[17]);
            data[row_id, 17] = vx_rms;

            vy_rms = parse(Float64, str_list[18]);
            data[row_id, 18] = vy_rms;
        end

        if file_id == 1
            sheet = xf[file_id];
            XLSX.rename!(sheet, "$file_id.pcd");
        else
            XLSX.addsheet!(xf, "$file_id.pcd")
        end
        sheet = xf["$file_id.pcd"]
        
        sheet["A1", dim=2] = [
            "x";
            "y ";
            "z ";
            "dyn_prop ";
            "id ";
            "rcs ";
            "vx ";
            "vy ";
            "vx_comp";
            "vy_comp ";
            "is_quality_valid";
            "ambig_state";
            "x_rms";
            "y_rms ";
            "invalid_state";
            "pdh0";
            "vx_rms";
            "vy_rms";
        ];
        sheet["A2:R$(n - 11)"] = data;
    end
end



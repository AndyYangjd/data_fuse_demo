#= extract_object_from_radar.jl
extract the object_list from raw-data of radar =#

using DataFrames, XLSX;
include("visualize_radar_points.jl")
using .visualize

prj_path = dirname(dirname(@__FILE__));
xls_file_path = prj_path * raw"\data\radar_process\radar_points.xlsx";

#= 
for id_sample in 1:38
    sh_name = "$id_sample.pcd"
    df=DataFrame(XLSX.readtable(
        xls_file_path,
        sh_name));
    println(df)
end =#

data, col_names = XLSX.readtable(xls_file_path, "1.pcd", header=true);

df = DataFrame(data, col_names);

x = convert(Array{Float64,1}, df.x);
y = convert(Array{Float64,1}, df.y);
vx_comp = convert(Array{Float64,1}, df.vx_comp);
vy_comp = convert(Array{Float64,1}, df.vy_comp);
v_comp = @. abs(vx_comp + im * vy_comp)

# set the v_comp-threshold(10km/s)
v_comp_threshold = 10 / 3.6;
id_v_comp = findall(x -> x >= v_comp_threshold, v_comp);

println(names(df))
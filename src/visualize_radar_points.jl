#= visualize_radar_points.jl
visualize the vel_comp of every point in radar =#

module visualize

using PyCall
@pyimport matplotlib.py

export visualizeVelCmp

function visualizeVelCmp(data)
    x = data[:,1];
    y = data[:,2];
    vx_comp = data[:,3];
    vy_comp = data[:,4];

    rotated_x, rotated_y = rotateRight90deg(x, y);
    plt = scatter(
        rotated_x,
        rotated_y,
        framestyle=:origin,
        xticks=-maximum(rotated_x):5:maximum(rotated_x),
        yticks=-maximum(rotated_y):5:maximum(rotated_y),
        xlabel="Y",
        ylabel="X",
        legend=false
        );
    
    for id_raw in 1:length(rotated_x)
        current_vx_comp = vx_comp[id_raw];
        current_vy_comp = vy_comp[id_raw];

        current_rotated_vx_comp, current_rotated_vy_comp = rotateRight90deg(
            current_vx_comp, current_vy_comp);

        plt_vel_x = [
            rotated_x[id_raw];
            rotated_x[id_raw]+current_rotated_vx_comp];
        plt_vel_y = [
            rotated_y[id_raw];
            rotated_y[id_raw]+current_rotated_vy_comp];
        plot!(
            plt,
            plt_vel_x,
            plt_vel_y
        )
    end
    gui()
end

function rotateRight90deg(original_x, original_y)
    return_x = -original_y;
    return_y = original_x;

    return return_x, return_y;
end


end
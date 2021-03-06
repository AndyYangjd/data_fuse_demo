# Role
- This file is analysized from nuscenes-devkit
- Link:https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/utils/data_classes.py#L254
- The filed means the real info of every column in pcd_ascii files.

## Field Interpretation

### 1->x
front pos in radar-Coord-Sys

- Unit: m


### 2->y
left pos in radar-Coord-Sys

- Unit: m

### 3->z
up pos in radar-Coord-Sys

- Unit: m

### 4->dyn_prop
Dynamic property of cluster to indicate if is moving or not.

- 0: moving
- 1: stationary
- 2: oncoming
- 3: stationary candidate
- 4: unknown
- 5: crossing stationary
- 6: crossing moving
- 7: stopped

### 5->id
the index of all radar points in pcd files

### 6->rcs
the RCS(radar Cross-Section) of points

### 7->vx
the velocity in the current radar frame.
In other words, relative velocity.

- Unit: m/s

### 8->vy
the velocity in the current radar frame.
In other words, relative velocity to radar.

- Unit: m/s

### 9->vx_comp
the velocities in m/s compensated by the ego motion. 
It is the measured velocity minus the ego motion.
In other words, relative to world-Coord-Sys.
 
We recommend using the compensated velocities.

- Unit: m/s

### 10->vy_comp
the velocities in m/s compensated by the ego motion. 
It is the measured velocity minus the ego motion.
In other words, relative to world-Coord-Sys.

We recommend using the compensated velocities.

- Unit: m/s

### 11->is_quality_valid

### 12->ambig_state
State of Doppler (radial velocity) ambiguity solution.

- 0: invalid
- 1: ambiguous
- 2: staggered ramp
- 3: unambiguous
- 4: stationary candidates

### 13->x_rms

### 14->y_rms

### 15->invalid_state
state of Cluster validity state.

(Invalid states)
- 0x01:invalid due to low RCS
- 0x02:invalid due to near-field artefact
- 0x03:invalid far range cluster because not confirmed in near range
- 0x05:reserved
- 0x06:invalid cluster due to high mirror probability
- 0x07:Invalid cluster because outside sensor field - of view
- 0x0d:reserved
- 0x0e:invalid cluster because it is a harmonics

(Valid states)
- 0x00:valid
- 0x04:valid cluster with low RCS
- 0x08:valid cluster with azimuth correction due to elevation
- 0x09:valid cluster with high child probability
- 0x0a:valid cluster with high probability of being a 50 deg artefact
- 0x0b:valid cluster but no local maximum
- 0x0c:valid cluster with high artefact probability
- 0x0f:valid cluster with above 95m in near range
- 0x10:valid cluster with high multi-target probability
- 0x11:valid cluster with suspicious angle

### 16-> pdh0:
False alarm probability of cluster (i.e. probability of being an artefact caused by multipath or similar).

- 0: invalid
- 1: <25%
- 2: 50%
- 3: 75%
- 4: 90%
- 5: 99%
- 6: 99.9%
- 7: <=100%

### 17->vx_rms
Standard deviation of longitudinal relative velocity

### 18->vy_rms
Standard deviation of lateral relative velocity
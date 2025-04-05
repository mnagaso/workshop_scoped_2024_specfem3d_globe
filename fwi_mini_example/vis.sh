# convert the output data into visualization format
SPECDIR=~/workspace/MINES/specfem3d_globe

# run the executable for post processing (e.g. for alpha kernel)
$SPECDIR/bin/xcombine_vol_data_vtu all alpha_kernel DATABASES_MPI/ DATABASES_MPI/ OUTPUT_FILES/ 1 1

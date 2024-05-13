# container image
imagefile=specfem3d_globe_centos7_mpi.sif

# load apptainer
module load tacc-apptainer

# get current directory
pwd = $(pwd)

# change directory to simulation folder
cd $pwd/simulation

# run the executable for post processing
apptainer run ../specfem3d_globe_centos7_mpi.sif xcombine_vol_data_vtu all alpha_kernel DATABASES_MPI/ DATABASES_MPI/ OUTPUT_FILES/ 1 1

# module load
module load gcc/9 impi qt5/5.14.2 swr/21.2.5 oneapi_rk paraview

# create snapshot
pvpython ../create_slice.py OUTPUT_FILES OUTPUT_FILES/reg_1_alpha_kernel.vtu -1

cd $pwd
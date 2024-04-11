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

cd $pwd
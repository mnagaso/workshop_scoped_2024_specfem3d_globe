# container image
imagefile=specfem3d_globe_centos7_mpi.sif

# load apptainer
module load tacc-apptainer

#
# adjoint simulation adjoint simulation
#

# change directory to simulation folder
cd ./simulation

# change simulation type
apptainer run ../$imagefile /home/scoped/specfem3d_globe/utils/change_simulation_type.pl -b

# run solver
ibrun apptainer run ../$imagefile xspecfem3D

cd ..

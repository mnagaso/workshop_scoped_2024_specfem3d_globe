
# container image
imagefile=specfem3d_globe_centos7_mpi.sif

# load apptainer
module load tacc-apptainer

# get current directory
pwd = $(pwd)

#
# forward simulation
#

# change directory to simulation folder
cd $pwd/simulation

# copy the model files from container to host
apptainer exec ../$imagefile cp -r /home/scoped/specfem3d_globe/DATA/{crust2.0,s20rts,s40rts,topo_bathy} ./DATA/

# change simulation type
apptainer run ../$imagefile /home/scoped/specfem3d_globe/utils/change_simulation_type.pl -F

# run mesher
ibrun apptainer run ../$imagefile xmeshfem3D

# run solver
ibrun apptainer run ../$imagefile xspecfem3D

#
# adjoint simulation adjoint simulation
#

# change simulation type
apptainer run ../$imagefile /home/scoped/specfem3d_globe/utils/change_simulation_type.pl -b

# run solver
ibrun apptainer run ../$imagefile xspecfem3D

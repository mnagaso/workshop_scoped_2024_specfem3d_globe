#
# adjoint simulation adjoint simulation
#

# change simulation type
apptainer run specfem3d_globe_centos7.sif /home/scoped/specfem3d_globe/utils/change_simulation_type.pl -b

# run solver 
ibrun apptainer run specfem3d_globe_centos7.sif xspecfem3D

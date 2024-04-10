
#
#
# forward simulation
#

# copy the model files from container to host
apptainer exec specfem3d_globe_centos7.sif cp -r /home/scoped/specfem3d_globe/DATA/{crust2.0,s20rts,s40rts,topo_bathy} ./DATA/

# change simulation type
apptainer run specfem3d_globe_centos7.sif /home/scoped/specfem3d_globe/utils/change_simulation_type.pl -F

# run mesher
ibrun apptainer run specfem3d_globe_centos7.sif xmeshfem3D

# run solver
ibrun apptainer run specfem3d_globe_centos7.sif xspecfem3D



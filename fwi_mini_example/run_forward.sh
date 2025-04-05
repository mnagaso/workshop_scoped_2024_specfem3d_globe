# run forward simulation

# before running this script, you need to have Specfem3D Globe and compile it.
# if not,
# git clone --recursive --branch devel https://github.com/SPECFEM/specfem3d_globe.git
# cd specfem3d_globe
# then configure/make it (below is the example to compile with/without GPU support)
# ./configure FC=gfortran CC=gcc MPIFC=mpif90 --with-cuda=cuda12 MPI_INC="/usr/include/openmpi-x86_64" CUDA_LIB="/usr/local/cuda/lib64/"
# or without GPU
# ./configure FC=gfortran CC=gcc MPIFC=mpif90
# make all -j4

# if you try with ADIOS2, the compile flag '--with-adios2 ADIOS_CONFIG=/path/to/adios2-config' is needed

# Path to the Specfem3D Globe directory
# It needs to be adjusted to the location of the Specfem3D Globe installation
# on your system.
SPECDIR=~/workspace/MINES/specfem3d_globe

# get number of processors from DATA/Par_file
NPROC_XI=$(grep NPROC_XI DATA/Par_file | awk '{print $3}')
NPROC_ETA=$(grep NPROC_ETA DATA/Par_file | awk '{print $3}')

# total number of processors
NPROC=$((NPROC_XI * NPROC_ETA))

# copy the model files from the specfem3d_globe directory
cp -r $SPECDIR/DATA/{crust2.0,s20rts,s40rts,topo_bathy} DATA/

# change the simulation setup for a forward simulation
$SPECDIR/utils/change_simulation_type.pl -F

# run mesher
echo "Running mesher"
mpirun -np $NPROC $SPECDIR/bin/xmeshfem3D

echo "Running solver"
mpirun -np $NPROC $SPECDIR/bin/xspecfem3D


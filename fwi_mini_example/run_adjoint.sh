# run adjoint simulation

# This mini example setup is skipping the step for calculating the adjoint source,
# which need to be done before running the adjoint simulation.

# The adjoint source is usually calculated from the difference between the observed
# and synthetic data, and the adjoint simulation is run to calculate the gradient
# of the objective function with respect to the model parameters.

# In stead, this script uses the pre-computed adjoint source contained in the SEM directory.
# the detail of the adjoint source calculation is described in :
# https://github.com/mnagaso/workshop_scoped_2024_specfem3d_globe/blob/main/data_process_and_kernel_comp_on_local.ipynb

# Path to the Specfem3D Globe directory
# It needs to be adjusted to the location of the Specfem3D Globe installation
# on your system.
SPECDIR=~/workspace/MINES/specfem3d_globe

# get number of processors from DATA/Par_file
NPROC_XI=$(grep NPROC_XI DATA/Par_file | awk '{print $3}')
NPROC_ETA=$(grep NPROC_ETA DATA/Par_file | awk '{print $3}')

# total number of processors
NPROC=$((NPROC_XI * NPROC_ETA))

# change the simulation setup for an adjoint simulation
$SPECDIR/utils/change_simulation_type.pl -b

# run the adjoint simulation
echo "Running adjoint simulation"
mpirun -np $NPROC $SPECDIR/bin/xspecfem3D
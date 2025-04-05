# SPECFEM3D_GLOBE Full Waveform Inversion Mini Example

This directory contains a mini example for Full Waveform Inversion (FWI) using SPECFEM3D_GLOBE. This example is part of the MINES workshop on seismic imaging and inversion.

## Directory Structure

- `DATA/`: Contains parameter files for the simulation
  - `Par_file`: Main parameter file for SPECFEM3D_GLOBE configuration
  - Other configuration files
- `DATABASES_MPI/`: Directory for output databases and simulation snapshots
- `OUTPUT_FILES/`: Contains output files from the simulation
- `run_forward.sh`: Script to run the forward simulation
- `run_adjoint.sh`: Script to run the adjoint simulation
- `vis.sh`: Script to reformat the output files for visualization

## Prerequisites

Before running this example, you need to have SPECFEM3D_GLOBE installed and compiled:

```bash
# Clone the repository
git clone --recursive --branch devel https://github.com/SPECFEM/specfem3d_globe.git
cd specfem3d_globe

# Configure and compile with GPU support (adjust the CUDA version by your device's sm version)
./configure FC=gfortran CC=gcc MPIFC=mpif90 --with-cuda=cuda12 MPI_INC="/usr/include/openmpi-x86_64" CUDA_LIB="/usr/local/cuda/lib64/"

# OR without GPU support
./configure FC=gfortran CC=gcc MPIFC=mpif90

# For ADIOS2 support, add:
# --with-adios2 ADIOS_CONFIG=/path/to/adios2-config

# Compile
make all -j4
```

## Running the FWI Workflow

1. Modify the `SPECDIR` path in the scripts to point to your SPECFEM3D_GLOBE installation:
   ```bash
   SPECDIR=/path/to/specfem3d_globe
   ```

2. Run the forward simulation:
   ```bash
   ./run_forward.sh
   ```

3. After the forward simulation completes, run the adjoint simulation:
   ```bash
   ./run_adjoint.sh
   ```

4. Finally, run the visualization script to reformat the output files:
   ```bash
   ./vis.sh
   ```

## Simulation Configuration

The simulation is configured for a regional domain centered at:
- Latitude: 37.4881°
- Longitude: 137.1197°
- Angular width: 90° in both Xi and Eta directions

The mesh consists of 96×96 elements at the surface, distributed across a 4×4 MPI processes grid.

## Model Configuration

The simulation uses the `s40rts` global tomographic model with:
- Oceans, ellipticity, topography, gravity, rotation, and attenuation all enabled

## Output Files

The simulation produces several outputs including:
- Seismograms in SAC binary format
- Databases in the `DATABASES_MPI` directory
- Kernel files when running in kernel mode

## Reference

For more information about SPECFEM3D_GLOBE, visit:
[https://github.com/SPECFEM/specfem3d_globe](https://github.com/SPECFEM/specfem3d_globe)
<a href="https://seisscoped.org/"><img src="https://seisscoped.org/images/scoped_logo.jpg" alt="scoped" width="50" /></a>

# The jupyter notebook and data for the 2024 SCOPED workshop, SPECFEM3D_GLOBE session

![kernel](img/kernel.png)

This repository contains the jupyter notebook and data for the 2024 SCOPED workshop. Below is a brief description of the files in this repository:

- `data_processing_and_kernel_comp.ipynb`: A jupyter notebook that demonstrates how to process the data and run a kernel computation.
- `data`: the data for the demo, which will be downloaded in the notebook.
- `quakeml`: the QuakeML files, which will be created after running the notebook.
- `simulation`: a directory where we run forward/adjoint simulations with Specfem3D_globe. The essential files will be created here after running the notebook.
- `img`: images used in the notebook and README.md.
- `shakemov_syn`: the synthetic waveform data downloaded from the ShakeMovie website.
- `finite_fault`: the CMTSOLUTION files for the finite fault model.
- `job.jupyter`: a job script for running the jupyter notebook on Frontera.
- `job.dcv`: a job script for running the visualization job on Frontera.
- `create_slice.py`: paraview python script for creating slices.
- `AVS_boundaries_elliptical.inp`: an AVS input file for plotting the coastlies.
- `paraview_red_to_blue_colormap.json`: a paraview colormap file for plotting kernel.
- `plot_kernel_slices_frontera.pvsm`: a paraview state file for plotting kernel slices.

## 0. About this example
Some parts of this example are designed to run on the Frontera supercomputer at TACC. 
If you don't have access to Frontera, you can still run the notebook on your local machine to do a data processing and calculation adjoint source. For running this on your local machine, please follow the section [here](#run-the-notebook-on-your-local-machine) section.


## 1. Log in to Frontera
This example is designed to run on the Frontera supercomputer at TACC. To log in to Frontera, you need to have an account at TACC and authentication setup. If you don't have an account, please follow the instruction to setup it [here](https://seisscoped.org/HPS-book/chapters/HPC/intro.html).

## 2. Run Jupyter notebook on Frontera

- go to SCRATCH directory:
```bash
cd $SCRATCH
```
- Clone this repository:
```bash
git clone https://github.com/mnagaso/workshop_scoped_2024_specfem3d_globe.git
```
- Submit the job:
```bash
cd workshop_scoped_2024
sbatch job.jupyter
```
- Check the job status:
```bash
squeue -u $USER
        JOBID   PARTITION   NAME      USER    ST       TIME  NODES NODELIST(REASON)
        6247768 development tap_jupy  mnagaso PD       0:00      1 (None)
```
- You will find the starting of the job by becoming `R` from `PD` for example:
```bash
squeue -u $USER
        JOBID   PARTITION   NAME      USER     ST      TIME  NODES NODELIST(REASON)
        6247768 development tap_jupy  mnagaso  R       0:00      1 c201-022
```

It takes about 1 mintue or so to finishing a initial setup. Then, you can access the jupyter notebook server by openning the link indicated at the last of the `jupyter.out` file. 

This link is something like:
```
tail jupyter.out

TACC: created reverse ports on Frontera logins
TACC: Your jupyter notebook server is now running at https://frontera.tacc.utexas.edu:60188/?token=ee7153b2ec3569dabea24b66de63247efed8cf2e8f203036cc2f490c58321fc7
```

## 3. Run the visualization job on Frontera

Stop current job for jupyter notebook by running the command below on the terminal:
``` bash
scancel -u $USER
```

Then, start a new job for the visualization by running the command below on the terminal:
``` bash
sbatch ./job.dcv
```

After the job is started, you will have the url for opening the visualization job environment, at the end of the output file `dcvserver.out`, e.g.
```
TACC: Your DCV session is now running!
TACC: To connect to your DCV session, please point a modern web browser to:
TACC:          https://frontera.tacc.utexas.edu:60036
```


## Run the notebook on your local machine

If you don't have access to Frontera, you can still run the notebook on your local machine. Here is a brief instruction on how to run the notebook on your local machine:

Prepare the prerequisites:
```bash
pip install --user obspy cartopy jupyterlab
```
```bash
pip uninstall -y urllib3
pip install --user 'urllib3<2.0'
```
then launch the jupyter notebook:
```bash
jupyter-lab
or
jupyter-notebook
or
jupyter lab
or
jupyter notebook
```

then modify a line in the data_process_and_kernel_comp.ipynb (7th cell) for loading pre-calculated synthetic data as below:
``` python

# read and plot the raw data

...

# load the synthetic waveform data with 3D model (with SPECFEM3D_GLOBE)
# use the result from the forward simulation
#st_syn = obspy.read("./simulation/OUTPUT_FILES/*sac") # in sac format

# use the precalculated synthetics with 3D model
st_syn = obspy.read("./data/C202401010710A/waveforms_syn/*sac") # in sac format

...
```
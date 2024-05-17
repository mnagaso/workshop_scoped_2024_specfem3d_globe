# module load for paraview
module load gcc/9 impi qt5/5.14.2 swr/21.2.5 oneapi_rk paraview

#
# Create a slice image using pvpython script
#
## change directory to simulation folder
##cd ./simulation
## create snapshot
##swr -p 1 pvpython ../create_slice.py OUTPUT_FILES OUTPUT_FILES/reg_1_alpha_kernel.vtu -1
##cd ..


#
# Create a slice image using paraview state file
#
# load paraview state file
swr -p 1 paraview ./paraview_state.pvsm
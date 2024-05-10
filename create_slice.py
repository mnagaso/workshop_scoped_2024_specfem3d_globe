# paraview script which creates a slice between two points (source and station)

from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import os
import numpy as np

if __name__ == '__main__':

    # get arguments
    import sys
    if len(sys.argv) != 4:
        print("Usage: create_slice.py OUTPUT_FILES OUTPUT_FILES/reg_1_alpha_kl.vtk (id rec)")
        sys.exit(1)

    # get arguments
    output_dir = sys.argv[1]
    fpath_data = sys.argv[2]
    id_rec = int(sys.argv[3])

    fsrc = output_dir+"/source.vtk"
    frec = output_dir+"/receiver.vtk"
    fdata = fpath_data

    reader_src = OpenDataFile(fsrc)
    reader_rec = OpenDataFile(frec)
    reader_data = OpenDataFile(fdata)
    reader_src.UpdatePipeline()
    reader_rec.UpdatePipeline()
    #reader_data.UpdatePipeline()

    renderView = GetActiveViewOrCreate('RenderView')

    output_src = reader_src.GetClientSideObject().GetOutput()
    output_rec = reader_rec.GetClientSideObject().GetOutput()
    output_data = reader_data.GetClientSideObject().GetOutput()


    # calculate the center of ouput_data by all corners
    center = output_data.GetCenter()
    print("center: ", center)
    # plot sphere at center
    #sphere = Sphere()
    #sphere.Center = center
    #sphere.Radius = 0.2
    #Show(sphere)


    # show src
    for i in range(output_src.GetNumberOfPoints()):
        p = output_src.GetPoint(i)
        print("source: ", p)
        # indicate source as a sphere
        sphere = Sphere()
        sphere.Center = p
        sphere.Radius = 0.02
        Show(sphere)

    # show rec
    for i in range(output_rec.GetNumberOfPoints()):
        p = output_rec.GetPoint(i)
        print("receiver: ", p)
        # indicate receiver as a sphere
        sphere = Sphere()
        sphere.Center = p
        sphere.Radius = 0.01
        Show(sphere)



    # create slice for each receiver
    for i in range(output_rec.GetNumberOfPoints()):

        if i != id_rec and id_rec != -1:
            continue

        p = output_rec.GetPoint(i)
        print("receiver: ", p)
        # create slice
        slice = Slice(reader_data)
        slice.SliceType = 'Plane'
        slice.SliceOffsetValues = [0.0]
        slice.SliceType.Origin = output_src.GetPoint(0)
        # calculate normal vector of plane which passes through source and receiver and center
        v_src_rec = np.array(p) - np.array(output_src.GetPoint(0))
        v_src_center = center - np.array(p)
        v_norm = np.cross(v_src_rec, v_src_center)

        slice.SliceType.Normal = v_norm

        #slice.UpdatePipeline()

        slice1Display = Show(slice, renderView, 'GeometryRepresentation')
        slice1Display.Representation = 'Surface'
        slice1Display.SetScalarBarVisibility(renderView, True)
        #Show(slice)

        arrayInfo = slice.PointData["alpha_kl"]
        print(arrayInfo)
        range = arrayInfo.GetComponentRange(0)
        print(range)

        cmap = GetColorTransferFunction('alpha_kl')
        #cmap.RescaleTransferFunction(range[0]/10, range[1]/10)
        factor=50000
        cmap.RGBPoints = [range[0]/factor, 0.23, 0.299, 0.754,
                          0.0, 0.865, 0.865, 0.865,
                          range[1]/factor, 0.706, 0.016, 0.150]
        omap = GetOpacityTransferFunction('alpha_kl')
        #omap.RescaleTransferFunction(range[0]/10, range[1]/10)



    layout = GetLayout()
    layout.SetSize(600, 500)
    # change the center of rotation to mass center of the data
    renderView.CenterOfRotation = slice.SliceType.Origin
    # reset view to fit data
    renderView.ResetCamera()

    Render()
    Interact()


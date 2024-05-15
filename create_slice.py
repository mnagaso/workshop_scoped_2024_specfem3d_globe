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

        slice1Display = Show(slice, renderView, 'GeometryRepresentation')
        slice1Display.Representation = 'Surface'
        slice1Display.SetScalarBarVisibility(renderView, True)

        # set scalar coloring
        ColorBy(slice1Display, ('POINTS', 'alpha_kernel'))
        # rescale color and/or opacity maps used to include current data range
        slice1Display.RescaleTransferFunctionToDataRange(True, False)
        # show color bar/color legend
        slice1Display.SetScalarBarVisibility(renderView, True)

    # get color transfer function/color map for 'alpha_kernel'
    alpha_kernelLUT = GetColorTransferFunction('alpha_kernel')
    # get opacity transfer function/opacity map for 'alpha_kernel'
    alpha_kernelPWF = GetOpacityTransferFunction('alpha_kernel')
    # get 2D transfer function for 'alpha_kernel'
    alpha_kernelTF2D = GetTransferFunction2D('alpha_kernel')
    # vrange for alpha_kernel
    vmin = -5e-7
    vmax = 5e-7
    # Rescale transfer function
    alpha_kernelLUT.RescaleTransferFunction(vmin, vmax)
    # Rescale transfer function
    alpha_kernelPWF.RescaleTransferFunction(vmin, vmax)
    # Rescale 2D transfer function
    alpha_kernelTF2D.RescaleTransferFunction(vmin, vmax, 0.0, 1.0)
    # get color legend/bar for alpha_kernelLUT in view renderView1
    alpha_kernelLUTColorBar = GetScalarBar(alpha_kernelLUT, renderView)
    # change scalar bar placement
    alpha_kernelLUTColorBar.Orientation = 'Horizontal'
    alpha_kernelLUTColorBar.WindowLocation = 'Any Location'
    alpha_kernelLUTColorBar.Position = [0.3448222424794894, 0.11209242618741988]
    alpha_kernelLUTColorBar.ScalarBarLength = 0.33000000000000046

    # use custom colormap
    ImportPresets(filename='../paraview_red_to_blue_colormap.json')
    alpha_kernelLUT.ApplyPreset('RedYellowWhiteCyanBlue', True)
    alpha_kernelPWF.ApplyPreset('RedYellowWhiteCyanBlue', True)

    # invert the transfer function (not necessary for this custom plot)
    #alpha_kernelLUT.InvertTransferFunction()
    #alpha_kernelPWF.InvertTransferFunction()

    # coast lines
    fname_coastline = "../AVS_boundaries_elliptical.inp"
    # create a new 'AVS UCD Reader'
    aVS_boundaries_ellipticalinp = AVSUCDReader(registrationName='AVS_boundaries_elliptical.inp', FileNames=[fname_coastline])
    # set active source
    SetActiveSource(aVS_boundaries_ellipticalinp)
    # show data in view
    aVS_boundaries_ellipticalinpDisplay = Show(aVS_boundaries_ellipticalinp, renderView, 'UnstructuredGridRepresentation')
    # trace defaults for the display properties.
    aVS_boundaries_ellipticalinpDisplay.Representation = 'Surface'
    # show color bar/color legend
    aVS_boundaries_ellipticalinpDisplay.SetScalarBarVisibility(renderView, True)
    # update the view to ensure updated data information
    renderView.Update()
    # get color transfer function/color map for 'Zcoord'
    zcoordLUT = GetColorTransferFunction('Zcoord')
    # turn off scalar coloring
    ColorBy(aVS_boundaries_ellipticalinpDisplay, None)
    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(zcoordLUT, renderView)
    # change solid color
    aVS_boundaries_ellipticalinpDisplay.AmbientColor = [1.0, 1.0, 1.0]
    aVS_boundaries_ellipticalinpDisplay.DiffuseColor = [1.0, 1.0, 1.0]


    layout = GetLayout()
    layout.SetSize(1103, 838)

    # view from south
    #renderView.CameraPosition = [-0.5887903997623548, 2.803681072719318, -1.018517693499023]
    #renderView.CameraFocalPoint = [-0.342757061123847, 0.3219155967235563, 0.42726002633571647]
    #renderView.CameraViewUp = [-0.5706063130402489, 0.37041409881175547, 0.7329405370970339]
    #renderView.CameraParallelScale = 1.0923619938785378
    # view from north
    renderView.CameraPosition = [-0.7655962333546708, -1.5952796160732157, 2.2850851066908113]
    renderView.CameraFocalPoint = [-0.5001205052249119, 0.4860835075378399, 0.49414500594139166]
    renderView.CameraViewUp = [-0.572003823461119, 0.5757051546753071, 0.5842732244644981]
    renderView.CameraParallelScale = 0.8639217207980154

    Render()
    # save screenshot
    SaveScreenshot(output_dir+"/slice_"+str(id_rec)+".png", layout, SaveAllViews=1)
    # interactive render
    Interact()




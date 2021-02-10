from osgeo import gdal
import matplotlib.pyplot as plt
import gdal_merge as gm
import subprocess


demList = ["Test_Files\\Original_DEMs\\gt30e020n40.tif", "Test_Files\\Original_DEMs\\gt30e020s10.tif",
           "Test_Files\\Original_DEMs\\gt30w020n40.tif", "Test_Files\\Original_DEMs\\gt30w020s10.tif"]

merge_cmd = "'' -o mergedDEM.tif"
gm.main(merge_cmd.split() + demList)

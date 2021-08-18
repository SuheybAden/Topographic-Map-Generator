from osgeo import gdal, ogr
# from osgeo.utils.gdal_merge import main as merge_main

import numpy as np
import os
import json
# import open3d as o3d


# Constant variables
merged_filename = "merged_DEM.tif"
clipped_filename = "clipped_DEM.tif"
temp_filename = "temp.tif"
resized_filename = "resized_DEM.tif"
cutline_filename = "shapefiles/World_Countries__Generalized_.shp"
resize = False
res = 10
vertical_exageration = .01
no_data_value = -9999

demList = ["Test_Files\\Original_DEMs\\gt30e020n40.tif", "Test_Files\\Original_DEMs\\gt30e020s10.tif",
           "Test_Files\\Original_DEMs\\gt30w020n40.tif", "Test_Files\\Original_DEMs\\gt30w020s10.tif"]

class MeshGenerator():

	def downloadDEM(self):
		pass

	def mergeDEM(self, dem_list):
		# Merge DEM files
		try:
			merge_cmd = "'' -o " + merged_filename
			# merge_main(merge_cmd.split() + dem_list)
		except:
			print("Couldn't merge DEM files")

	# Generates the shapefile that will be used for clipping
	# The field paramater determines what field
	def generateShp(self, field: str, fieldVal: str):
		# Split shapefile to country of interest
		driver = ogr.GetDriverByName("ESRI Shapefile")
		ds = driver.Open(cutline_filename)
		if ds is None:
			print("Can't open shapefile")
			return
		layer = ds.GetLayer()
		spatialRef = layer.GetSpatialRef()

		for feature in layer:
			if feature.GetField(field).lower() == fieldVal.lower():
				dirName = "country_shp/"
				filename = fieldVal + ".shp"

				if not os.path.isdir(dirName):
					os.mkdir(dirName)

				# if not os.path.isfile(dirName + filename):
				outds = driver.CreateDataSource(dirName + filename)
				outlayer = outds.CreateLayer(filename, srs=spatialRef, geom_type=ogr.wkbPolygon)
				
				outDfn = outlayer.GetLayerDefn()
				print(outDfn)
				outFeat = ogr.Feature(outDfn)
				
				lngeom = feature.GetGeometryRef()
				outFeat.SetGeometry(lngeom)
				outlayer.CreateFeature(outFeat)

				return feature.ExportToJson(as_object=True)


	def getFieldNames(self, layer):
		schema = []
		ldefn = layer.GetLayerDefn()
		for n in range(ldefn.GetFieldCount()):
			fdefn = ldefn.GetFieldDefn(n)
			schema.append(fdefn.name)
		print(schema)

	def resizeDEM(self, source_dem, x_res, y_res):
		return gdal.Warp(resized_filename, source_dem, xRes=x_res, yRes=y_res)


	def clipDEM(self, source_dem, downscale):
		# Clip based on shapefile
		clipped_dem = gdal.Warp(temp_filename, source_dem,
							cutlineDSName=cutline_filename, cropToCutline=True, dstNodata=-9999)

		# Resize elevation file
		if downscale:
			gt = clipped_dem.GetGeoTransform()
			new_x = res * gt[1]
			new_y = res * gt[5]
			clipped_dem = self.resizeDEM(clipped_dem, new_x, new_y)

		return clipped_dem


	def dem_to_mesh(self, source_dem):
		dem = gdal.Open(source_dem, gdal.GA_ReadOnly)
		if not dem:
			print("Failed to open DEM")
			return

		# gt = dem.GetGeoTransform()
		# radius = 5.8 * max(gt[1], gt[5])

		band = dem.GetRasterBand(1)
		array = band.ReadAsArray()
		print(array.shape)

		v = []
		n = []
		for x in range(array.shape[0]):
			for y in range(array.shape[1]):
				if array[x][y] != no_data_value:
					v.append([x, y, array[x][y] * vertical_exageration])
					n.append([0, 0, 1])

		vertices = np.array(v)
		normals = np.array(n)
		v = []

		# pcd = o3d.geometry.PointCloud()
		# pcd.points = o3d.utility.Vector3dVector(vertices)
		# pcd.normals = o3d.utility.Vector3dVector(normals)

		print("Successfully generated point cloud")

		# distances = pcd.compute_nearest_neighbor_distance()
		# avg_dist = np.mean(distances)
		# radius = 4 * avg_dist

		# Need normals
		# bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
		# 	pcd, o3d.utility.DoubleVector([radius, radius * 2]))

		# poisson_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
		# 	pcd, depth=8, width=0, scale=1.1, linear_fit=False)[0]
		# bbox = pcd.get_axis_aligned_bounding_box()
		# p_mesh_crop = poisson_mesh.crop(bbox)

		# dec_bpa = bpa_mesh.simplify_quadric_decimation(100000)
		# dec_bpa.remove_degenerate_triangles()
		# dec_bpa.remove_duplicated_triangles()
		# dec_bpa.remove_duplicated_vertices()
		# dec_bpa.remove_non_manifold_edges()
		# # dec_poisson = poisson_mesh.simplify_quadric_decimation(100000)
		# o3d.visualization.draw_geometries([dec_bpa])
		# # o3d.io.write_triangle_mesh("bpa_mesh.ply", dec_bpa)


if __name__ == "__main__":
	mesh_generator = MeshGenerator()
	# mesh_generator.merge_dem(demList)
	# dem = gdal.Open("Africa.tif", gdal.GA_ReadOnly)
	# mesh_generator.clip_dem(merged_filename, True)
	# mesh_generator.dem_to_mesh("Africa_resized.tif")
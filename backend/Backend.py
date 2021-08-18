from osgeo import ogr
from .MeshGenerator import MeshGenerator
from PyQt5.QtCore import QObject, QVariant, pyqtSignal, pyqtSlot
import requests
from zipfile import ZipFile
import os
import json

class Backend(QObject):
	updated = pyqtSignal()

	def __init__(self) -> None:
		super().__init__()
		self.datasetTags = ["National Elevation Dataset (NED) 1 arc-second",
							"Digital Elevation Model (DEM) 1 meter",
							"National Elevation Dataset (NED) 1/3 arc-second",
							"National Elevation Dataset (NED) 1/9 arc-second",
							"Small-scale Datasets"]
	
	@pyqtSlot(QVariant)
	def generateMesh(self, param):
		print("Starting...")
		print("Getting Coordinates...")
		
		meshGenerator = MeshGenerator()
		
		if param.property("selectionMode").toString() == "Rect" :
			minX = param.property("topLeftRectLat").toNumber()
			minY = param.property("topLeftRectLong").toNumber()
			maxX = param.property("bottomRightRectLat").toNumber()
			maxY = param.property("bottomRightRectLong").toNumber()
			self.downloadByRect(minX, minY, maxX, maxY)

		elif param.property("selectionMode").toString() == "Country" :
			countryCode = param.property("targetCountryCode").toString()
			country_shp = self.downloadByCountry(meshGenerator, countryCode)


	def downloadByRect(self, minX:int, minY: int, maxX:int, maxY:int):
		# Converts bounding box to string that USGS server can accept
		bbox=','.join([str(minX), str(minY), str(maxX), str(maxY)])
		print(bbox)
		payload = dict(bbox=bbox, datasets="National Elevation Dataset (NED)")
		links = self.getDownloadLinks(payload)
		# print(links)
		# self.downloadAndExtractFiles(links)

	def downloadByCountry(self, generator:MeshGenerator, countryCode:str):
		# Gets country's shapefile and bounding box
		shp = generator.generateShp("ISO", str(countryCode))
		coordinates = shp["geometry"]["coordinates"][0][0]
		x_coordinates, y_coordinates = zip(*coordinates)
		
		# Downloads files within bounding box
		self.downloadByRect(min(x_coordinates), min(y_coordinates),
								max(x_coordinates), max(y_coordinates))

		return shp

	def getDownloadLinks(self, payload):
		r = requests.get("https://tnmaccess.nationalmap.gov/api/v1/products?",
							params=payload)
		print(r.url)

		links = []
		if r.status_code == 200:
			for item in r.json()["items"]:
				links.append(item["downloadURL"])
		return links
		

	def downloadAndExtractFiles(self, links):
		for link in links:
			# Name of the directory that stores the DEM files
			dirname = "Elevation_Files/"
			# Creates filename from the end of the download link
			filename = link.rsplit('/', 1)[-1]

			# Downloads from each link one at a time
			if not os.path.isfile(dirname + filename):
				r = requests.get(link)
				# Saves the zip files contents
				with open(dirname + filename, 'wb') as f:
					f.write(r.content)
				with ZipFile(dirname + filename, "r") as data_zip:
					data_zip.extractall(dirname)


if __name__ == "__main__":
	meshGenerator = MeshGenerator()
	coord = meshGenerator.generateShp("Country", "Egypt")
	print(coord)

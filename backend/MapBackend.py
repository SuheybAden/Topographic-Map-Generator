from .DownloadManager import DownloadManager
from osgeo import ogr
from .MeshGenerator import MeshGenerator
from PyQt5.QtCore import QObject, QVariant, pyqtSignal, pyqtSlot

class MapBackend(QObject):
	def __init__(self) -> None:
		super().__init__()
		self.datasetTags = ["National Elevation Dataset (NED) 1 arc-second",
							"Digital Elevation Model (DEM) 1 meter",
							"National Elevation Dataset (NED) 1/3 arc-second",
							"National Elevation Dataset (NED) 1/9 arc-second",
							"Small-scale Datasets"]

		self.downloadManager = DownloadManager()
		self.meshGenerator = MeshGenerator()
	
	# Signals
	updated = pyqtSignal()

	@pyqtSlot(QVariant)
	def generateMesh(self, param):
		print("Starting...")
		print("Getting Coordinates...")
		
		print(param.property("apiKey").toString())

		# if param.property("selectionMode").toString() == "Rect" :
		# 	# Convert QVariants to proper python data types
		# 	minX = param.property("topLeftRectLat").toNumber()
		# 	minY = param.property("topLeftRectLong").toNumber()
		# 	maxX = param.property("bottomRightRectLat").toNumber()
		# 	maxY = param.property("bottomRightRectLong").toNumber()

		# 	# Downloads files within bounding box
		# 	self.downloadManager.downloadDatasets(minX, minY, maxX, maxY)

		# elif param.property("selectionMode").toString() == "Country" :
		# 	# Convert QVariants to proper python data types
		# 	countryCode = param.property("targetCountryCode").toString()

		# 	# Gets country's shapefile and bounding box
		# 	shp = meshGenerator.generateShp("ISO", str(countryCode))
		# 	coordinates = shp["geometry"]["coordinates"][0][0]
		# 	x_coordinates, y_coordinates = zip(*coordinates)
			
		# 	# Downloads files within bounding box
		# 	self.downloadManager.downloadDatasets(min(x_coordinates), min(y_coordinates),
		# 						max(x_coordinates), max(y_coordinates))


if __name__ == "__main__":
	meshGenerator = MeshGenerator()
	coord = meshGenerator.generateShp("Country", "Egypt")
	print(coord)

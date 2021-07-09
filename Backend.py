from PyQt5.QtCore import QObject, QVariant, pyqtSignal, pyqtSlot
import requests
# import MeshGenerator

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
    def generate_mesh(self, param):
        print("Downloading topography files...")
        if param.property("selectionMode").toString() == "Rect" :
            minx = param.property("topLeftRectLat").toNumber()
            miny = param.property("topLeftRectLong").toNumber()
            maxx = param.property("bottomRightRectLat").toNumber()
            maxy = param.property("bottomRightRectLong").toNumber()
            bbox=','.join([str(minx), str(miny), str(maxx), str(maxy)])

            payload = dict(bbox=bbox,
                            max=10)
            r = requests.get("https://tnmaccess.nationalmap.gov/api/v1/products?",
                                params=payload)

        elif param.property("selectionMode").toString() == "Circle" :
            pass
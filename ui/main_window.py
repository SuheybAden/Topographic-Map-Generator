from PyQt5 import QtCore, QtWidgets, QtGui, uic
import os
from .generate_mesh import merge_dem, get_shp, clip_dem


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.load_ui()

	def load_ui(self):
		cwd = os.getcwd()
		filename = os.path.splitext(os.path.basename(__file__))[0]
		uic.loadUi(cwd + "\\ui_files\\" + filename + ".ui", self)
		self.connect_all()

	def connect_all(self):
		self.projection_combo.currentTextChanged.connect(
			self.projectionChanged_Handler)
		self.inputFile_btn.clicked.connect(self.inputFileClicked_Handler)
		self.outputFile_btn.clicked.connect(self.outputFileClicked_Handler)

	def projectionChanged_Handler(self):
		pass

	def inputFileClicked_Handler(self):
		pass

	def outputFileClicked_Handler(self):
		pass

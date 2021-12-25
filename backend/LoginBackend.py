from .MapBackend import MapBackend
from .DownloadManager import DownloadManager
from PyQt5.QtCore import QObject, QVariant, pyqtSignal, pyqtSlot

class LoginBackend(QObject):
	def __init__(self) -> None:
		super().__init__()

		self.downloadManager = DownloadManager()

	# Signals to send data with
	signalLogin = pyqtSignal(bool, str, QObject)
	signalBackend = pyqtSignal(QObject, QObject)

	@pyqtSlot(QVariant)
	def login(self, param):
		print("Logging in...")

		# Converts QVariants to proper python data types
		username = param.property("username").toString()
		password = param.property("password").toString()

		username = "Suheyb21"
		password = "C5YJR3txZpue2Xq"

		if self.downloadManager.login(username, password):
			print("Successfully logged into USGS")
			self.signalLogin.emit(True, self.downloadManager.apiKey, MapBackend())

		else:
			print("Failed to login")
			self.signalLogin.emit(False, None, None)

	# Slot that generates a backend
	@pyqtSlot(QObject)
	def createMapBackend(self, win):
		self.signalBackend.emit(win, MapBackend())
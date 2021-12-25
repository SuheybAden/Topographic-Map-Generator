from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
import sys
from backend.LoginBackend import LoginBackend
from backend.MapBackend import MapBackend

def main():
	app = QApplication(sys.argv)
	
	engine = QQmlApplicationEngine()
	engine.quit.connect(app.quit)
	engine.load("qml/" + 'LoginWindow.qml')

	if not engine.rootObjects():
		sys.exit(-1)

	backend = LoginBackend()
	engine.rootObjects()[0].setProperty('backend', backend)

	sys.exit(app.exec())

if __name__ == "__main__":
	main()
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
import sys
from backend.Backend import Backend

def main():
	app = QApplication(sys.argv)
	
	engine = QQmlApplicationEngine()
	engine.quit.connect(app.quit)
	engine.load("qml/" + 'LoginWindow.qml')

	# backend = Backend()
	# engine.rootObjects()[0].setProperty('backend', backend)

	if not engine.rootObjects():
		sys.exit(-1)

	sys.exit(app.exec())

if __name__ == "__main__":
	main()
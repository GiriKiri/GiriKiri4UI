import sys

from Controller.CentralWidgetController import CentralWidgetController

from PySide6.QtWidgets import (
  QApplication,
  QMainWindow,
)


def main() :
  application = QApplication(sys.argv)

  mainWindow = QMainWindow()

  centralWidgetController = CentralWidgetController()
  centralWidgetController.setup()
  mainWindow.setCentralWidget(centralWidgetController.centralWidget)

  mainWindow.show()
  sys.exit(application.exec())


if __name__ == '__main__' :
  main()

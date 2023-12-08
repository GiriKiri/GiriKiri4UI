from Controller.RealsenseController import RealsenseController
from View.CentralWidget import CentralWidget

from PySide6.QtWidgets import (
  QLabel,
  QPushButton,
)

class CentralWidgetController :
  def setup(self) :
    centralWidget = CentralWidget()
    centralWidget.setup()
    self.centralWidget = centralWidget

    depthImageWidget = centralWidget.findChild(QLabel, 'realsense depth image widget')
    colorImageWidget = centralWidget.findChild(QLabel, 'realsense color image widget')
    #IR 이미지 부분
    irImageWidget = centralWidget.findChild(QLabel, 'realsense ir frame widget')

    startButton = centralWidget.findChild(QPushButton, 'realsense start button')
    stopButton = centralWidget.findChild(QPushButton, 'realsense stop button')

    self.realsenseController = RealsenseController()
    #ir 이미지 위젯 추가
    self.realsenseController.setup(depthImageWidget, colorImageWidget, irImageWidget, startButton, stopButton)

    startButton.clicked.connect(self.realsenseController.start)
    stopButton.clicked.connect(self.realsenseController.stop)
    stopButton.setEnabled(False)

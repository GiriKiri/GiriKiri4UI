from PySide6.QtWidgets import (
  QLabel,
  QPushButton,
  QWidget,
  QVBoxLayout,
)

class CentralWidget(QWidget) :
  def setup(self) :
    layout = QVBoxLayout()
    self.setLayout(layout)

    depthImageWidget = QLabel()
    depthImageWidget.setObjectName('realsense depth image widget')
    layout.addWidget(depthImageWidget)

    colorImageWidget = QLabel()
    colorImageWidget.setObjectName('realsense color image widget')
    layout.addWidget(colorImageWidget)
    
    # ir 위젯 추가
    irImageWidget = QLabel()
    irImageWidget.setObjectName('realsense ir image widget')
    layout.addWidget(irImageWidget)

    startButton = QPushButton('Start')
    startButton.setObjectName('realsense start button')
    layout.addWidget(startButton)

    stopButton = QPushButton('Stop')
    stopButton.setObjectName('realsense stop button')
    layout.addWidget(stopButton)
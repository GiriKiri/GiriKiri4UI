import numpy as np
import cv2
from PySide6 import QtCore
from PySide6 import QtGui 
from Model.Camera import Realsense
import constant


class RealsenseController :
  class RealsenseThread(QtCore.QThread) :
    def __init__(self) :
      super().__init__()
      self.shouldRun = True

    def setup(self, depthImageWidget, colorImageWidget, irImageWidget) :
      self.depthImageWidget = depthImageWidget
      self.colorImageWidget = colorImageWidget
      #IR 이미지 추가부분
      self.irImageWidget = irImageWidget

      self.realsense = Realsense()
      self.realsense.setup()

    def run(self) :
      while self.shouldRun :
        self.update()

    def update(self) :
      depthFrame, colorFrame, irFrame = self.realsense.getFrames()
      # 깊이, 이미지, ir 프레임 모두 아닌 경우
      if not depthFrame or not colorFrame or not irFrame :
        return

      self.updateDepthImage(depthFrame)
      self.updateColorImage(colorFrame)
      #irFrame 업데이트
      self.updateIRImage(irFrame)

    def updateDepthImage(self, depthFrame) :
#       self.printDepthAverage(depthFrame)
      image = np.asanyarray(depthFrame.get_data())
      image = cv2.applyColorMap(cv2.convertScaleAbs(image, alpha=0.03), cv2.COLORMAP_JET)
      qImage = QtGui.QImage(image, constant.INFRARED_WIDTH, constant.INFRARED_HEIGHT, QtGui.QImage.Format_RGB888)
      pixmap = QtGui.QPixmap.fromImage(qImage)
      pixmap = pixmap.scaled(constant.IMAGEWIDGET_WIDTH, constant.IMAGEWIDGET_HEIGHT, QtCore.Qt.KeepAspectRatio)
      self.depthImageWidget.setPixmap(pixmap)

    def printDepthAverage(self, depthFrame) :
      sum = 0
      for y in range(constant.INFRARED_HEIGHT) :
        for x in range(constant.INFRARED_WIDTH) :
          sum += depthFrame.get_distance(x, y)
      average = round(sum / (constant.INFRARED_WIDTH * constant.INFRARED_HEIGHT), 2)
      print("depth average : ", average)

    def updateColorImage(self, colorFrame) :
      image = np.asanyarray(colorFrame.get_data())
#       self.printRGBAverage(image)
      qImage = QtGui.QImage(image, constant.COLOR_WIDTH, constant.COLOR_HEIGHT, QtGui.QImage.Format_RGB888)
      pixmap = QtGui.QPixmap.fromImage(qImage)
      pixmap = pixmap.scaled(constant.IMAGEWIDGET_WIDTH, constant.IMAGEWIDGET_HEIGHT, QtCore.Qt.KeepAspectRatio)
      self.colorImageWidget.setPixmap(pixmap)

    def printRGBAverage(self, image) :
      sum = np.sum(image, axis=(0, 1))
      average = sum / (constant.COLOR_WIDTH * constant.COLOR_HEIGHT)
      print("rgb average : ", average)
      
    #ir 이미지 업데이트 함수 추가
    def updateIRImage(self, irFrame) :
      image = np.asanyarray(irFrame.get_data())
      image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
      qImage = QtGui.QImage(image, constant.IR_WIDTH, constant.IR_HEIGHT, QtGui.QImage.Format_RGB888)
      pixmap = QtGui.QPixmap.fromImage(qImage)
      pixmap = pixmap.scaled(constant.IMAGEWIDGET_WIDTH, constant.IMAGEWIDGET_HEIGHT, QtCore.Qt.KeepAspectRatio)
      self.irImageWidget.setPixmap(pixmap)
      
    # ir 이미지 평균 값 출력 함수
    # def printIRAverage(self, image) :

    def stop(self) :
      self.shouldRun = False

  def __init__(self) :
    self.realsenseThread = None

  def setup(self, depthImageWidget, colorImageWidget, irImageWidget, startButton, stopButton) :
    self.depthImageWidget = depthImageWidget
    self.colorImageWidget = colorImageWidget
    # ir 이미지 위젯 추가
    self.irImageWidget = irImageWidget

    self.startButton = startButton
    self.stopButton = stopButton

  def start(self) :
    if not self.realsenseThread :
      self.startButton.setEnabled(False)
      self.stopButton.setEnabled(True)

      self.setupRealsenseThread()
      self.realsenseThread.start()

  def setupRealsenseThread(self) :
    self.realsenseThread = self.RealsenseThread()
    # ir 이미지 위젯 추가
    self.realsenseThread.setup(self.depthImageWidget, self.colorImageWidget, self.irImageWidget)

  def stop(self) :
    self.startButton.setEnabled(True)
    self.stopButton.setEnabled(False)

    self.realsenseThread.stop()
    self.realsenseThread.wait()
    self.realsenseThread = None

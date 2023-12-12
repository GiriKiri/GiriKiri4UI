import time

import constant

class Camera :
  def __init__(self) :
    self.timeinterval = 1.0 / constant.FPS

  def setup(self) :
    pass

  def getImage(self) :
    pass

class VirtualCamera(Camera) :
  WIDTH = 2
  HEIGHT = 2

  blackImage = [
    [ [0, 0, 0], [0, 0, 0], ],
    [ [0, 0, 0], [0, 0, 0], ],
  ]

  startImage = [
    [ [255, 0, 0], [0, 255, 0], ],
    [ [0, 0, 255], [127, 127, 127], ],
  ]

  greyImage = [
    [ [127, 127, 127], [127, 127, 127], ],
    [ [127, 127, 127], [127, 127, 127], ],
  ]

  def setup(self) :
    self.image = self.greyImage

  def update(self) :
    time.sleep(self.timeinterval)
    for x in range(self.WIDTH) :
      for y in range(self.HEIGHT) :
        for rgb in range(3) :
          value = self.image[y][x][rgb]
          self.image[y][x][rgb] = (value + 10) % 256

  def getImage(self) :
    self.update()
    return self.image

class Realsense(Camera) :
  def setup(self) :
    self.setupConfig()

  def setupConfig(self) :
    # warning : if this import is executed before `QApplication()`, an thread related error message is printed
    import pyrealsense2 as rs
    self.pipeline = rs.pipeline()

    config = rs.config()
    # config.enable_stream(rs.stream.infrared, 1, constant.INFRARED_WIDTH, constant.INFRARED_HEIGHT, rs.format.y8, constant.FPS)
    config.enable_stream(rs.stream.depth, constant.INFRARED_WIDTH, constant.INFRARED_HEIGHT, rs.format.z16, constant.FPS)
    config.enable_stream(rs.stream.color, constant.COLOR_WIDTH, constant.COLOR_HEIGHT, rs.format.rgb8, constant.FPS)
    # config IR 스트림 추가
    config.enable_stream(rs.stream.infrared, constant.IR_WIDTH, constant.IR_HEIGHT, rs.format.y8, constant.FPS)
    self.pipeline.start(config)

    self.align = rs.align(rs.stream.color)

  def waitForAlignedFrames(self) :
    frames = self.pipeline.wait_for_frames()
    alignedFrames = self.align.process(frames)
    return alignedFrames

  def getFrames(self) :
    # frames = self.waitForAlignedFrames()
    frames = self.pipeline.wait_for_frames()
    depthFrame = frames.get_depth_frame()
    # infraredFrame = frames.get_infrared_frame()
    colorFrame = frames.get_color_frame()
    #IR 이미지 프레임 추가
    irFrame = frames.get_infrared_frame()

    return ( depthFrame, colorFrame, irFrame )

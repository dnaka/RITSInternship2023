#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait

# Colorセンサーが返すカラーの値
COLOR_DICT = {
  "UNKNOWN":0,
  "BLACK":1,
  "WHITE":2,
  "RED":3,
  "BLUE":4,
  "YELLOW":5,
  "GRAY":6,
}

# pybricksのreferenceはここ: https://docs.pybricks.com/en/v2.0/ev3devices.html
class RGBColor():
  """
  RGBカラーを取り扱うクラス。定数とメソッドのみで状態は持たない。
  Colorクラスだとpybricksのクラス名とかぶるのでRGBColorにしている。
  """
  THRESHOLD = 8

  # 各色の基準値。RGBの反射値がこれらの+-THRESHOLD以内なら、その色として扱う。単位は%
  BASE_RED = [57, 7, 7]
  BASE_BLUE = [7, 12, 32]
  BASE_YELLOW = [50, 48, 5]
  BASE_BLACK = [1, 2, 0]
  BASE_GRAY = [29, 34, 43]
  BASE_GREEN = [10, 28, 6]
  BASE_WHITE = [57, 58, 75]

  def __init__(self):
    """Constructor"""
    self.colorSensor = ColorSensor(Port.S3)

  def __parse(self, base, red, green, blue):
    """ baseがBASE_WHITE かつ (BASE_WHITE - THRESHOLD) 値より明るければ、白と見なす """
    if (base[0] == self.BASE_WHITE[0] and base[1] == self.BASE_WHITE[1] and base[2] == self.BASE_WHITE[2]) and \
       ((base[0] - self.THRESHOLD) <= red) and \
       ((base[1] - self.THRESHOLD) <= green ) and \
       ((base[2] - self.THRESHOLD) <= blue):
      return True

    """ RGBの反射値lightValが、baseで指定された色かどうか調べる"""
    if ((base[0] - self.THRESHOLD) <= red   and red   <= (base[0] + self.THRESHOLD)) and \
       ((base[1] - self.THRESHOLD) <= green and green <= (base[1] + self.THRESHOLD)) and \
       ((base[2] - self.THRESHOLD) <= blue  and blue  <= (base[2] + self.THRESHOLD)):
      return True

    return False

  def getColor(self):
    """
    センサーの取得したRGB値を具体的な色に変換する
    """
    (red, green, blue) = self.colorSensor.rgb()
    if self.__parse(self.BASE_BLACK, red, green, blue):
      return COLOR_DICT["BLACK"]
    elif self.__parse(self.BASE_RED, red, green, blue):
      return COLOR_DICT["RED"]
    elif self.__parse(self.BASE_YELLOW, red, green, blue):
      return COLOR_DICT["YELLOW"]
    elif self.__parse(self.BASE_GRAY, red, green, blue):
      return COLOR_DICT["GRAY"]
    elif self.__parse(self.BASE_BLUE, red, green, blue):
      return COLOR_DICT["BLUE"]
    elif self.__parse(self.BASE_WHITE, red, green, blue):
      return COLOR_DICT["WHITE"]
    else:
      return COLOR_DICT["UNKNOWN"]
  
  def getReflection(self):
    """
    赤外線の反射値を返す
    """
    return self.colorSensor.reflection()

  def getRgb(self):
    """
    RGB値を返す
    """
    return self.colorSensor.rgb()

if __name__ == "__main__":
  ev3 = EV3Brick()
  colorSensor = ColorSensor(Port.S3)
  rgbColor = RGBColor()

  while True:
    color = rgbColor.getColor()

    ev3.screen.clear()
    if color is COLOR_DICT["UNKNOWN"]:
      ev3.screen.draw_text(0, 0, "UNKNOWN")
    elif color is COLOR_DICT["RED"]:
      ev3.screen.draw_text(0, 0, "RED")
    elif color is COLOR_DICT["BLUE"]:
      ev3.screen.draw_text(0, 0, "BLUE")
    elif color is COLOR_DICT["YELLOW"]:
      ev3.screen.draw_text(0, 0, "YELLOW")
    elif color is COLOR_DICT["BLACK"]:
      ev3.screen.draw_text(0, 0, "BLACK")
    elif color is COLOR_DICT["WHITE"]:
      ev3.screen.draw_text(0, 0, "WHITE")
    elif color is COLOR_DICT["GRAY"]:
      ev3.screen.draw_text(0, 0, "GRAY")

    wait(1000)

#!/usr/bin/env pybricks-micropython
import sys
sys.path.append("./")

# pybricksのreferenceはここ: https://docs.pybricks.com/en/v3.2.0/index.html
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch
from pybricks import ev3brick as brick
from pybricks.robotics import DriveBase
from color import RGBColor, COLOR_DICT

class LineTraceCar():
  """
  ライントレースを行うクラス
  """

  # タイヤの速度。ターンする時は片方をLOW、もう片方をHIGHにすると曲がる。単位は角度/s (deg/s)
  SPEED = [120, 30]

  def __init__(self):
    """
    Constructor
    """
    # EV3の固有デバイス初期化
    self.leftMotor = Motor(Port.C)
    self.rightMotor = Motor(Port.B)
    self.robot = DriveBase(self.leftMotor, self.rightMotor, 56, 104)
    
  
  def parking(self):
    """
    車庫入れと元の道への復帰をする
    """
    self.robot.drive_time(self.SPEED[0], 0, 180000/self.SPEED[0])
    self.robot.drive_time(0, -45, 2500)
    self.robot.drive_time(-self.SPEED[0], 0, 270000/self.SPEED[0])

    # 待機状態にする
    self.idle()

    self.robot.drive_time(self.SPEED[0], 0, 270000/self.SPEED[0])
    self.robot.drive_time(0, 45, 2500)


  def goal(self):
    """
    厨房に戻る
    """
    self.robot.drive_time(self.SPEED[0], 0, 300000/self.SPEED[0])
    self.robot.drive_time(0, -45, 2500)

    # 待機状態にする
    self.idle()


  def idle(self):
    """
    タッチセンサーが押されるまで待機状態になる
    """
    self.__run(0,0)
    while True:
      if ts_1.pressed() or ts_2.pressed():
        break

  def TraceColorLine(self, color):
    """
    色の線をトレースする
    """
    # RGBColorクラスの初期化
    rgbColor = RGBColor()

    self.__initMotor()
    isDelivery = True

    # ラインをトレースして走る
    while True:

      # 色の取得と判定
      gotColor = rgbColor.getColor()
      # 画面を初期化
      brick.display.clear()

      if gotColor is COLOR_DICT["BLACK"]:
        # 色名を画面に表示
        brick.display.text("BLACK",(60,50))
        # 右旋回
        self.__run(self.SPEED[1], self.SPEED[0])

      elif gotColor is COLOR_DICT["YELLOW"]:
        # 色名を画面に表示
        brick.display.text("YELLOW",(60,50))
        if color == "YELLOW" and isDelivery:
          isDelivery = False
          # 車庫入れ
          self.parking()
        else:
          # 右旋回
          self.__run(self.SPEED[1], self.SPEED[0])
      
      elif gotColor is COLOR_DICT["RED"]:
        # 色名を画面に表示
        brick.display.text("RED",(60,50))
        if color == "RED" and isDelivery:
          isDelivery = False
          # 車庫入れ
          self.parking()
        else:
          # 右旋回
          self.__run(self.SPEED[1], self.SPEED[0])

      elif gotColor is COLOR_DICT["BLUE"]:
        # 色名を画面に表示
        brick.display.text("BLUE",(60,50))
        if color == "BLUE" and isDelivery:
          isDelivery = False
          # 車庫入れ
          self.parking()
        else:
          # 右旋回
          self.__run(self.SPEED[1], self.SPEED[0])

      elif gotColor is COLOR_DICT["GRAY"]:
        # 色名を画面に表示
        brick.display.text("GRAY",(60,50))
        if isDelivery:
          # 右旋回
          self.__run(self.SPEED[1], self.SPEED[0])
        else:
          isDelivery = True
          # 厨房に戻る
          self.goal()

      elif gotColor is COLOR_DICT["WHITE"]:
        # 色名を画面に表示
        brick.display.text("WHITE",(60,50))
        # 左回転
        self.__run(self.SPEED[0], self.SPEED[1])

      else:
        # 白以外のその他の色も左回転
        self.__run(self.SPEED[0], self.SPEED[1])
    # end of while

    # モーターを停止
    self.leftMotor.stop()
    self.rightMotor.stop()
    print("trace MotorStop")

  def __initMotor(self):
    """
    【内部関数】モーターの初期化
    """
    self.leftMotor.brake()
    self.rightMotor.brake()

    self.leftMotor.reset_angle(0)
    self.rightMotor.reset_angle(0)

  def __run(self, l_motor_speed, r_motor_speed):
    """
    【内部関数】モーターを回す。
    @param l_motor_speed, r_motor_speed 左右モーターの角速度(deg/s)
    """
    if l_motor_speed == 0:
      # TODO: hold()でもいいかも
      self.leftMotor.stop()
    else:
      self.leftMotor.run(l_motor_speed)

    if r_motor_speed == 0:
      self.rightMotor.stop()
    else:
      self.rightMotor.run(r_motor_speed)

  def __runDecidedDistance(self, distance_cm):
    """
    【内部関数】指定した距離だけ進む
    @param distance_cm 走行距離
    """
    speed = self.__calcDegree(distance_cm)

    # 補足：wait = True の場合、該当処理の完了を待ってから次の処理に進む
    # 「左モーター wait = False」「右モーター wait = True」にすることで、処理が同時になり、直進できる
    self.leftMotor.run_angle(speed, speed, wait=False)
    self.rightMotor.run_angle(speed, speed, wait=True)

    self.leftMotor.stop()
    self.rightMotor.stop()

  def __calcDegree(self, run_distance_cm):
    """
    【内部関数】走行距離を入力すると、必要な角度を計算する
    @param run_distance_cm 走行距離
    """
    # 走行距離yは y = 5.6(cm タイヤ直径) * 3.14 * deg / 360 で計算できるので、これを変形してdegを計算する
    return run_distance_cm * 20.47


class initColor():
    def __init__(self, ts_1, ts_2):
      self.init_color = "RED"
      self.ts_1 = ts_1
      self.ts_2 = ts_2

    def selectColor(self):
      stop_color = ["BLUE", "RED", "YELLOW"]
      color_index = 0

      brick.display.clear()
      brick.display.text("please select color",(20, 50))

      wait(3000)

      pre_ts_1, pre_ts_2 = False, False

      brick.display.clear()
      brick.display.text(stop_color[color_index],(60, 50))

      while True:
        # waitを入れることで、ボタンが確実に反応するようになる
        wait(100)
        if (not self.ts_1.pressed()) and pre_ts_1:
          color_index = (color_index + 1) % 3
          brick.display.clear()
          brick.display.text(stop_color[color_index],(60, 50))

        if (not self.ts_2.pressed()) and pre_ts_2:
          brick.display.clear()
          break

        pre_ts_1 = ts_1.pressed()
        pre_ts_2 = ts_2.pressed()

      self.init_color = stop_color[color_index]

      return self.init_color


if __name__ == "__main__":
  ts_1, ts_2 = TouchSensor(Port.S1), TouchSensor(Port.S2)

  instanceInitColor = initColor(ts_1, ts_2)
  init_color = instanceInitColor.selectColor()

  print(init_color)

  car = LineTraceCar()
  # ライントレース開始
  car.TraceColorLine(init_color)
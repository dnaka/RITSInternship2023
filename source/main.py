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
from time import time

class LineTraceCar():
  """
  ライントレースを行うクラス
  """

  # タイヤの速度。ターンする時は片方をLOW、もう片方をHIGHにすると曲がる。単位は角度/s (deg/s)
  SPEED = [240, 80]

  def __init__(self):
    """
    Constructor
    """
    # EV3の固有デバイス初期化
    self.leftMotor = Motor(Port.C)
    self.rightMotor = Motor(Port.B)
    self.ultrasonicsensor = UltrasonicSensor(Port.S4)
    self.robot = DriveBase(self.leftMotor, self.rightMotor, 56, 104)
    self.ts_1 = TouchSensor(Port.S1)
    self.ts_2 = TouchSensor(Port.S2)

  def parking(self):
    """
    車庫入れと元の道への復帰をする
    """

    # 車庫入れ
    # 直進
    self.robot.drive_time(self.SPEED[0], 0, 180000/self.SPEED[0])
    # 反時計回りに角速度(45deg/s)で転回
    self.robot.drive_time(0, -45, 2200)
    # 後退
    self.robot.drive_time(-self.SPEED[0], 0, 250000/self.SPEED[0])

    # 待機状態にする
    self.idle()

    # 元の道への復帰
    # 直進
    self.robot.drive_time(self.SPEED[0], 0, 270000/self.SPEED[0])
    # 時計回りに角速度(45deg/s)で転回
    self.robot.drive_time(0, 45, 2200)
    self.robot.drive_time(self.SPEED[0], 0, 100000/self.SPEED[0])

  def returnKitchen(self):
    """
    厨房に戻ったとき緑なら
    """
    
    # 後退
    self.robot.drive_time(-self.SPEED[0], 0, 100000/self.SPEED[0])
    # 反時計回りに角速度(45deg/s)で転回
    self.robot.drive_time(0, -45, 3000)


  def idle(self):
    """
    タッチセンサーが押されるまで待機状態になる
    """
    # 停止する
    self.__run(0,0)

    # 待機状態になる
    while True:
      # タッチセンサーが押されたら処理を終了
      if self.ts_1.pressed() or self.ts_2.pressed():
        break
    # end of while

  def GetDistance(self):
    # 距離を返す
    return self.ultrasonicsensor.distance()

  def Alert(self) :
    """
    アラートを鳴らす
    """
    while True:
      if self.GetDistance() > 100:
        break
      else:
        brick.sound.beep(300, 500, 5)
        wait(500)

  def TraceColorLine(self):
    """
    色の線をトレースする
    """
    # RGBColorクラスの初期化
    rgbColor = RGBColor()

    self.__initMotor()

    isDelivery = True
    count = 0

    selected_color = self.selectColor()

    # ラインをトレースして走る
    while True:

      #  障害物との距離が10cm以下の場合
      if self.GetDistance() <= 100:
        # 停止し、停止時間の管理のためのcountを１増加させる
        #この周の処理を終了
        self.__run(0, 0)
        count += 1
        #約5秒間、ロボの前に障害物があった場合アラートを鳴らす。
        if count >= 50:
          self.Alert()
        wait(100)
        continue   
      count = 0
      
      # 色の取得と判定
      gotColor = rgbColor.getColor()

      # 配達中かどうかで分岐
      if isDelivery:
        if gotColor is COLOR_DICT["BLACK"]:
          # 右旋回
          self.__run(self.SPEED[1], self.SPEED[0])

        elif gotColor is COLOR_DICT["YELLOW"]:
          # 選んだ色が黄色の場合
          if selected_color == "YELLOW":
            # 配達中フラグをFalseにする
            isDelivery = False
            # 車庫入れ
            self.parking()

          else:
            # 右旋回
            self.__run(self.SPEED[1], self.SPEED[0])
        
        elif gotColor is COLOR_DICT["RED"]:
          # 選んだ色が赤色の場合
          if selected_color == "RED":
            # 配達中フラグをFalseにする
            isDelivery = False
            # 車庫入れ
            self.parking()

          else:
            # 右旋回
            self.__run(self.SPEED[1], self.SPEED[0])

        elif gotColor is COLOR_DICT["BLUE"]:
          # 選んだ色が青色の場合
          if selected_color == "BLUE":
            # 配達中フラグをFalseにする
            isDelivery = False
            # 車庫入れ
            self.parking()

          else:
            # 右旋回
            self.__run(self.SPEED[1], self.SPEED[0])

        elif gotColor is COLOR_DICT["GRAY"]:
          # 右旋回
          self.__run(self.SPEED[1], self.SPEED[0])

        else:
          # その他の色で左回転
          self.__run(self.SPEED[0], self.SPEED[1])
      # 厨房に戻るとき
      else:
        if gotColor is COLOR_DICT["GREEN"]:
          isDelivery = True
          # 厨房に戻る
          self.returnKitchen()
          selected_color = self.selectColor()
      
        elif gotColor is COLOR_DICT["WHITE"]:
          # 左回転
          self.__run(self.SPEED[0], self.SPEED[1])

        else:
          # その他の色で右回転
          self.__run(self.SPEED[1], self.SPEED[0])

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

  def selectColor(self):
    """
    ボタンで色を選択し、選択された色を返す
    """
    # 選べる色のリスト
    color_list = ["BLUE", "RED", "YELLOW"]
    # 現在選んでいる色のリスト番号
    color_index = 0

    brick.display.clear()
    brick.display.text("please select color",(20, 50))

    wait(3000)

    pre_ts_1, pre_ts_2 = False, False

    brick.display.clear()
    brick.display.text(color_list[color_index],(60, 50))

    # 色の選択
    while True:
      # waitを入れることで、ボタンが確実に反応するようになる
      wait(100)

      # ts_1を押すと色を変更
      if (not self.ts_1.pressed()) and pre_ts_1:
        color_index = (color_index + 1) % 3
        brick.display.clear()
        brick.display.text(color_list[color_index],(60, 50))

      # ts_2を押すとループを終了
      if (not self.ts_2.pressed()) and pre_ts_2:
        brick.display.clear()
        break

      # 100ミリ秒前にボタンが押されたか
      pre_ts_1 = self.ts_1.pressed()
      pre_ts_2 = self.ts_2.pressed()
    # end of while
      

    return color_list[color_index]


if __name__ == "__main__":

  car = LineTraceCar()

  # ライントレース開始
  car.TraceColorLine()


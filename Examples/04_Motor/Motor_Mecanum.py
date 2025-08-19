#!/usr/bin/env/python3
# File name   : Motor_Mecanum.py
# Website     : www.Adeept.com
# Author      : Adeept
# Date        : 2025/03/6
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor

MOTOR_M1_IN1 =  15      #Define the positive pole of M1
MOTOR_M1_IN2 =  14      #Define the negative pole of M1
MOTOR_M2_IN1 =  12      #Define the positive pole of M2
MOTOR_M2_IN2 =  13      #Define the negative pole of M2
MOTOR_M3_IN1 =  11      #Define the positive pole of M3
MOTOR_M3_IN2 =  10      #Define the negative pole of M3
MOTOR_M4_IN1 =  8       #Define the positive pole of M4
MOTOR_M4_IN2 =  9       #Define the negative pole of M4

def map(x,in_min,in_max,out_min,out_max):
  return (x - in_min)/(in_max - in_min) *(out_max - out_min) +out_min

i2c = busio.I2C(SCL, SDA)
pwm_motor = PCA9685(i2c, address=0x5f)
pwm_motor.frequency = 50

motor1 = motor.DCMotor(pwm_motor.channels[MOTOR_M1_IN1],pwm_motor.channels[MOTOR_M1_IN2] )
motor1.decay_mode = (motor.SLOW_DECAY)
motor2 = motor.DCMotor(pwm_motor.channels[MOTOR_M2_IN1],pwm_motor.channels[MOTOR_M2_IN2] )
motor2.decay_mode = (motor.SLOW_DECAY)
motor3 = motor.DCMotor(pwm_motor.channels[MOTOR_M3_IN1],pwm_motor.channels[MOTOR_M3_IN2] )
motor3.decay_mode = (motor.SLOW_DECAY)
motor4 = motor.DCMotor(pwm_motor.channels[MOTOR_M4_IN1],pwm_motor.channels[MOTOR_M4_IN2] )
motor4.decay_mode = (motor.SLOW_DECAY)

def Motor(channel,direction,motor_speed):
  if motor_speed > 100:
    motor_speed = 100
  elif motor_speed < 0:
    motor_speed = 0
  speed = map(motor_speed, 0, 100, 0, 1.0)
  if direction == 1:
    speed = -speed

  if channel == 1:
    motor1.throttle = speed
  elif channel == 2:
    motor2.throttle = speed
  elif channel == 3:
    motor3.throttle = speed
  elif channel == 4:
    motor4.throttle = speed

def motorStop():#Motor stops
    motor1.throttle = 0
    motor2.throttle = 0
    motor3.throttle = 0
    motor4.throttle = 0

def destroy():
  motorStop()
  pwm_motor.deinit()


if __name__ == '__main__':
  try:     
    for i in range(10):
      speed = 80
      Motor(1, 1, speed) #forward
      Motor(2, 1, speed) 
      Motor(3, 1, speed) 
      Motor(4, 1, speed) 
      print("Forward")
      time.sleep(2) 

      Motor(1,-1, speed) #backward
      Motor(2,-1, speed)
      Motor(3,-1, speed)
      Motor(4,-1, speed)
      print("Backward")
      time.sleep(2)

      Motor(1,-1, speed) #Rotate Left
      Motor(2,-1, speed)
      Motor(3,1, speed)
      Motor(4,1, speed)
      print("Turn left")
      time.sleep(2)

      Motor(1,1, speed) #Rotate Right
      Motor(2,1, speed)
      Motor(3,-1, speed)
      Motor(4,-1, speed)
      print("Turn right")
      time.sleep(2)

      Motor(1, -1, speed) #Translate Left
      Motor(2, 1, speed)
      Motor(3, -1, speed)
      Motor(4, 1, speed)
      print("Drift left")
      time.sleep(2)

      Motor(1, 1, speed) #Translate Right
      Motor(2, -1, speed)
      Motor(3, 1, speed)
      Motor(4, -1, speed)
      print("Drift right")
      time.sleep(2)

      Motor(1,1, 0) #Translate Forward and Left
      Motor(2,1, speed)
      Motor(3,1, 0)
      Motor(4,1, speed)
      print("Drift front-left")
      time.sleep(2)

      Motor(1,-1, 0) #Translate Backward and right
      Motor(2,-1, speed)
      Motor(3,-1, 0)
      Motor(4,-1, speed)
      print("Drift rear-right")
      time.sleep(2)

      Motor(1,1, speed) #Translate Forward and Right
      Motor(2,1, 0)
      Motor(3,1, speed)
      Motor(4,1, 0)
      print("Drift front-right")
      time.sleep(2)

      Motor(1,-1, speed) #Translate Backward and left
      Motor(2,-1, 0)
      Motor(3,-1, speed)
      Motor(4,-1, 0)
      print("Drift rear-left")
      time.sleep(2)
    destroy()
  except KeyboardInterrupt:
    destroy()


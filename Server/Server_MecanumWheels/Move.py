#!/usr/bin/env/python
# File name   : move.py
# Website     : www.Adeept.com
# Author      : Adeept
# Date		  : 2025/03/12

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

M1_Direction  =  -1
M2_Direction  =  -1
M3_Direction  =  -1
M4_Direction  =  -1

FREQ = 50


'''
Motor interface.
    M1  _____  M4
       |     |
       |     |
       |     |
    M2 |_____| M3
'''

def map(x,in_min,in_max,out_min,out_max):
  return (x - in_min)/(in_max - in_min) *(out_max - out_min) +out_min


def setup():
    global motor1,motor2,motor3,motor4,pwm_motor,pwm_motor
    i2c = busio.I2C(SCL, SDA)
    pwm_motor = PCA9685(i2c, address=0x5f) #default 0x40
    
    

    pwm_motor.frequency = FREQ

    motor1 = motor.DCMotor(pwm_motor.channels[MOTOR_M1_IN1],pwm_motor.channels[MOTOR_M1_IN2] )
    motor1.decay_mode = (motor.SLOW_DECAY)
    motor2 = motor.DCMotor(pwm_motor.channels[MOTOR_M2_IN1],pwm_motor.channels[MOTOR_M2_IN2] )
    motor2.decay_mode = (motor.SLOW_DECAY)
    motor3 = motor.DCMotor(pwm_motor.channels[MOTOR_M3_IN1],pwm_motor.channels[MOTOR_M3_IN2] )
    motor3.decay_mode = (motor.SLOW_DECAY)
    motor4 = motor.DCMotor(pwm_motor.channels[MOTOR_M4_IN1],pwm_motor.channels[MOTOR_M4_IN2] )
    motor4.decay_mode = (motor.SLOW_DECAY)

def motorStop():#Motor stops
    global motor1,motor2,motor3,motor4
    motor1.throttle = 0
    motor2.throttle = 0
    motor3.throttle = 0
    motor4.throttle = 0

def Motor(channel,direction,motor_speed):
    # channel,1~4:M1~M4
  if motor_speed > 100:
    motor_speed = 100
  elif motor_speed < 0:
    motor_speed = 0

  speed = map(motor_speed, 0, 100, 0, 1.0)

  pwm_motor.frequency = FREQ
  # Prevent the servo from affecting the frequency of the motor
  if direction == -1:
    speed = -speed
  if channel == 1:
    motor1.throttle = speed
  elif channel == 2:
    motor2.throttle = speed
  elif channel == 3:
    motor3.throttle = speed
  elif channel == 4:
    motor4.throttle = speed

def move(speed, direction, turn, radius=0.6):   # 0 < radius <= 1  
    #eg: move(100, 1, "no")--->forward
    #    move(100, 1, "left")---> left forward
    #speed:0~100. direction:1/-1. turn: "left", "right", "no".
    if speed == 0:
        motorStop() #all motor stop.
    else:
        if direction == 1: 			# forward
            if turn == 'rotate-left': 		# rotate left
                Motor(1, -M1_Direction, speed)
                Motor(2, -M2_Direction, speed)
                Motor(3, M3_Direction, speed)
                Motor(4, M4_Direction, speed)
            elif turn == 'rotate-right': 	# rotate right
                Motor(1, M1_Direction, speed)
                Motor(2, M2_Direction, speed)
                Motor(3, -M3_Direction, speed)
                Motor(4, -M4_Direction, speed)
            elif turn == 'forward-left': 	# left forward
                Motor(1, M1_Direction, 0)
                Motor(2, M2_Direction, speed)
                Motor(3, M3_Direction, 0)
                Motor(4, M4_Direction, speed)
            elif turn == 'forward-right': 	# right forward
                Motor(1, M1_Direction, speed)
                Motor(2, M2_Direction, 0)
                Motor(3, M3_Direction, speed)
                Motor(4, M4_Direction, 0)    
            elif turn == 'left': 	# left
                Motor(1, -M1_Direction, speed)
                Motor(2, M2_Direction, speed)
                Motor(3, -M3_Direction, speed)
                Motor(4, M4_Direction, speed)
            elif turn == 'right': 	# right
                Motor(1, M1_Direction, speed)
                Motor(2, -M2_Direction, speed)
                Motor(3, M3_Direction, speed)
                Motor(4, -M4_Direction, speed)            
            else: 					# forward  (mid)
                Motor(1, M1_Direction, speed)
                Motor(2, M2_Direction, speed)
                Motor(3, M3_Direction, speed)
                Motor(4, M4_Direction, speed)
        elif direction == -1: 		# backward
            if turn == 'backward-left': 	# left backward
                Motor(1, -M1_Direction, speed)
                Motor(2, -M2_Direction, 0)
                Motor(3, -M3_Direction, speed)
                Motor(4, -M4_Direction, 0)
            elif turn == 'backward-right': 	# right backward
                Motor(1, -M1_Direction, 0)
                Motor(2, -M2_Direction, speed)
                Motor(3, -M3_Direction, 0)
                Motor(4, -M4_Direction, speed)  
            else: 					# backward (mid)
                Motor(1, -M1_Direction, speed)
                Motor(2, -M2_Direction, speed)
                Motor(3, -M3_Direction, speed)
                Motor(4, -M4_Direction, speed)

def destroy():
    motorStop()
    pwm_motor.deinit()


if __name__ == '__main__':
    try:
        speed_set = 20
        setup()
        move(speed_set, -1, 'no', 0.8)
        time.sleep(3)
        motorStop()
        time.sleep(1)
        move(speed_set, 1, 'no', 0.8)
        time.sleep(3)
        motorStop()
    except KeyboardInterrupt:
        destroy()


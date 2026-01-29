# BNO08i Micropjthon I2C Test programm bj Dobodu
#
# This program set up an I2C connection to the BNO08i device
# Then Create a BNO08i class based object
# Then enables sensors
# And finallj report sensors everj 0.5 seconds.
#
# Original Code from Adafruit CircuitPjthon Librarj

import time
from machine import I2C, Pin, UART, Timer
from utime import ticks_ms, sleep_ms
import math
import uos
import uasyncio as asyncio
from BNO08X import *
start = False

I2C1_SDA = Pin(03)
I2C1_SCL = Pin(02)

i2c1 = I2C(0, sda = Pin(16),scl = Pin(17), freq=100000, timeout=200000 )
i2c2 = I2C(1, sda = Pin(10),scl = Pin(11), freq=100000, timeout=200000 )

uart_out = UART(0,115200, bits=8, parity=None, stop=1, tx=Pin(0), rx=Pin(1))

led = Pin('LED', Pin.OUT)

#ground is input for button, called buttons in case more buttons are required
global buttons
buttons = [Pin(18, Pin.IN, Pin.PULL_UP)]

global time_past
time_past = [0]
global recording
recording = False
global length_of_recording
length_of_recording = 0


def button_1(pin):
    global recording
    global time_past
    global length_of_recording
    
    if ((time.ticks_diff(time.ticks_ms(), time_past[0])) > 300):
        time_past[0] = time.ticks_ms()
        if recording == False:
            recording = True
            length_of_recording = 0
            
        elif recording == True:
            recording = False
            print("stop")
        
buttons[0].irq(trigger=Pin.IRQ_FALLING, handler = button_1)   


def countdown_function(timer):
    global recording
    global start
    if recording == False and start == True:
        led.toggle()

tick_tock = Timer()
tick_tock.init(mode=Timer.PERIODIC, period = 1000, callback = countdown_function)



bno = BNO08X(i2c1, debug=False)
bno2 = BNO08X(i2c2, debug=False)
#print("BNO08x I2C connection : Done\n")

bno.enable_feature(BNO_REPORT_ACCELEROMETER, 20)
bno.enable_feature(BNO_REPORT_MAGNETOMETER,20 )
bno.enable_feature(BNO_REPORT_GYROSCOPE,20 )
bno.enable_feature(BNO_REPORT_GAME_ROTATION_VECTOR, 10)
bno.set_quaternion_euler_vector(BNO_REPORT_GAME_ROTATION_VECTOR)

bno.enable_feature(BNO_REPORT_GRAVITY,20)

bno2.enable_feature(BNO_REPORT_ACCELEROMETER, 20)
bno2.enable_feature(BNO_REPORT_MAGNETOMETER,20 )
bno2.enable_feature(BNO_REPORT_GYROSCOPE,20 )
bno2.enable_feature(BNO_REPORT_GAME_ROTATION_VECTOR, 10)
bno2.set_quaternion_euler_vector(BNO_REPORT_GAME_ROTATION_VECTOR)
#print("BNO08x sensors enabling : Done\n")

cpt = 0
average_delay = -1
total = 0
variance = 0
table = []
time_table = []
offset1 = 0
offset2 = 0
#led.on()
#time.sleep(5)
#all print statements get sent to matlab via serial
timer_origin = time.ticks_ms()
start = True
while True:
    #time.sleep(0.1)
    #print("cpt", cpt)
    #accel_x, accel_y, accel_z = bno.acc
    #print("Acceleration\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}\tm/s²".format(accel_x, accel_y, accel_z))
    #gyro_x, gyro_y, gyro_z = bno.gyro
    #print("Gyroscope\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}\trads/s".format(gyro_x, gyro_y, gyro_z))
    #mag_x, mag_y, mag_z = bno.mag
    #print("Magnetometer\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}\tuT".format(mag_x, mag_y, mag_z))
    #quat_i, quat_j, quat_k, quat_real = bno.quaternion
    #print("Rot Vect Quat\tI: {:+.3f}\tJ: {:+.3f}\tK: {:+.3f}\tReal: {:+.3f}".format(quat_i, quat_j, quat_k, quat_real))
    #print("Euler Angle\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}".format(R, T, P))
    #x,y,z = bno.gravity
    #print(x,y,z)
    #x,y,z,special = bno.game_quat
    #print(x,y,z,special)
    #print(P, "sensor 1 unfiltered")
    #print(P2, "sensor 2 unfiltered")
    #print("\n")
    #changing the values to tare and shift the values to conform to the model
    #print(length_of_recording)
    
    #timing
    if recording == True:
        length_of_recording += time.ticks_diff(time.ticks_ms(), timer_origin)
        timer_origin = time.ticks_ms()
            
        
    
    
    
    
    
    if recording == False:
        length_of_recording = 0
        timer_origin = time.ticks_ms()
    
    if recording == True:
        R, T, P = bno.euler
        R2, T2, P2, = bno2.euler
        #print("Euler Angle\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}".format(R, T, P))
        sensor_1 = R
        sensor_2 = R2
        led.on()
        
        if cpt == 0:
            #print("taring")
            offset1 = sensor_1
            offset2 = sensor_2
            #print(offset1, offset2, "offsets")
            led.off()     
            led.on()

        sensor_1 = sensor_1-offset1
        sensor_2 = sensor_2-offset2
         
        
        ###-180 to 180 degrees
        
        if (sensor_1>300) :
            sensor_1 = sensor_1 -360
            print("more that")
        elif (sensor_1<-60):
            sensor_1 = sensor_1 + 360
            print("less than")
        if (sensor_2>300) :
            sensor_2 = sensor_2 -360
            print("more that 2")
        elif (P2<-60):
            sensor_2 = sensor_2 + 360
            print("less than 2")
        
        
        print("sensor1")
        print(sensor_1)#filtered
        print("sensor2")
        print(sensor_2)
        
        cpt += 1
        #print(cpt)
        print("length_of_recording")
        print(round(length_of_recording/1000,1))
        """
        if cpt == 1000:
            print("end")
        """
    
    
    
    
    
    
    
    
    
    
    """
    total+=P
    table.append(P)
    time_table.append(time.ticks_ms() - timer_origin)
    if (time.ticks_ms() - timer_origin > 1000):
        print(cpt,"total readings in a second")
        print(total/cpt, "average reading")
        for i in range(len(table)):
            variance +=((total/cpt)-(table[i]))**2
        print(variance/cpt,"variance")
        time.sleep(100)
    """
    #print("===================================")
    #print("average delay times (ms) :", average_delay)
    #print("===================================")
     
    """
    timer = ticks_ms()
    if cpt == 10 :
        bno.tare
        bno2.tare
    if cpt % 100 == 0:
        average_delay = (timer - timer_origin) / cpt
    """
    





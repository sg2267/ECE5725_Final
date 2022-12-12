# coding = uft-8
from socket import *
import RPi.GPIO as GPIO
import time
from time import sleep
from gpiozero import Servo
import json

GPIO.setmode(GPIO.BCM)
# One button for quit
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Motor A
GPIO.setup(26, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

# Motor B
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

dc = 0
p = GPIO.PWM(26,100)  # A
q = GPIO.PWM(16,100)  # B 
p.start(dc)           # A
q.start(dc)           # B

# Motor A
GPIO.output(5, GPIO.LOW)
GPIO.output(6, GPIO.LOW)
# Motor B
GPIO.output(20, GPIO.LOW)
GPIO.output(21, GPIO.LOW)

# Socket communication
udp = socket(AF_INET, SOCK_DGRAM)
udp.bind(("",8080))

start_state = False
coderun = True

# Servo
val = 0
servo = Servo(13)
servo_2 = Servo(22)

while coderun:
    #time.sleep(0.2)
    # Socket receive message
    msg,addrInfo = udp.recvfrom(1024)
    print(" message from %s ：%s"%(addrInfo[0],msg.decode("utf-8")))
    output = json.loads(msg)
    #output = msg.decode("utf-8")
    
    if (output[0] == 'forward'):
        # A: forward
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(5, GPIO.LOW)
        # B: forward
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.HIGH)
        # Run 
        p.ChangeDutyCycle(80)
        q.ChangeDutyCycle(60)
        
    elif (output[0] == 'left'):
        # A: forward (large)
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(5, GPIO.LOW)
        # B: forward (small)
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
        # Run 
        p.ChangeDutyCycle(60)
        q.ChangeDutyCycle(10)
        
    elif (output[0] == 'right'):
        # A: forward (small)
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(5, GPIO.LOW)
        # B: forward (large)
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.HIGH)
        # Run 
        p.ChangeDutyCycle(10)
        q.ChangeDutyCycle(50)
        
    else:
        # A: forward (small)
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(5, GPIO.LOW)
        # B: forward (large)
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.HIGH)
        # Run 
        p.ChangeDutyCycle(0)
        q.ChangeDutyCycle(0)
    
    if output[1] == 'down':
        val = val + 0.2
        if val > 1:
            val = 1
        else:
            servo_2.value = val
        sleep(0.1)   
    elif output[1] == 'up':
        val = val - 0.2
        if val < -1:
            val = -1
        else:
            servo_2.value = val
        sleep(0.1)              
    elif output[1] == 'left':
        val = val - 0.2
        if val < -1:
            val = -1
        else:
            servo.value = val
        sleep(0.1)       
    elif output[1] == 'right':
        val = val + 0.2
        if val > 1:
            val = 1
        else:
            servo.value = val
        sleep(0.1)  
    else:
        servo.value = val    
    
    if (not GPIO.input(27)):
        coderun = False
        udp.close()
        print("Close")
    
    
    
    
    
    
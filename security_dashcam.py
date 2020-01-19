# Visit www.youtube.com/c/Rahulkhanna24june for more projects.


import RPi.GPIO as GPIO
import picamera
import os
import glob
import smtplib
from time import sleep, strftime, time

# Importing modules for sending mail
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText 
from email.utils import formatdate  
from email import encoders

sender = ' Sender Email ID'
password = ' password '
receiver = ' Receiver Email ID'

#DIR = './Database/'
DIR = '/home/pi/Desktop/KEMET/Intruder1/'
FILE_PREFIX = 'img-'

sensorPIN = 15
# Set pins 23, 24 to be an output pin and set initial value to low (high), since relay ckt is pull-down mechanism
Green = 23
Red = 24
# Set pin 14 to be an input pin
reset_button = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensorPIN, GPIO.IN)
GPIO.setup(reset_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(Green, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(Red, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setwarnings(False)

pulse = 0
PyroRead = 0
IR_threshold = 198000

IR_sensed = 0
start_time = 0
end_time = 0

def send_mail():
    timestr = strftime("%Y-%m-%d-%H%M%S")
    # print (timestr)
    print ('Sending E-Mail')
    filename = os.path.join(DIR, FILE_PREFIX + '%s.jpg' % timestr)
    
    with picamera.PiCamera() as camera:
        #To change the direction of the camera
        camera.rotation = 270
        camera.resolution = (1024, 768)
        #camera.resolution = (3280, 2464)
        camera.start_preview()
        sleep(0.1)
        pic = camera.capture(filename)
        print ('Image Captured')
        
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Alert - Security Breach at your place'
    
    body = 'Picture is Attached. \n. \n. \n. \nThis is a automated message from thelonelyprogrammer'
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()
    print ('Mail Sent . . .')
    
def alert():
    GPIO.output(23, GPIO.HIGH) # Turn off Green
    GPIO.output(24, GPIO.LOW) # Turn on Red
    print("Alert !!!")
            
    send_mail()
    
    counter = 0
    
    while(1):
        print(counter, end = ' ')
        counter += 1
        if GPIO.input(reset_button)==0:
            GPIO.output(23, GPIO.LOW) # Turn on Green
            GPIO.output(24, GPIO.HIGH) # Turn off Red
            print("")
            print('*'*25)
            print("Manual Reset !")
            print('*'*25, end = '\n')
            break
        
        elif(counter > 100):
            GPIO.output(23, GPIO.LOW) # Turn on Green
            GPIO.output(24, GPIO.HIGH) # Turn off Red
            
            print("")
            print('*'*25)
            print("Counter timeout")
            print('*'*25, end = '\n')
            break
        
        else:
            sleep(0.1)
            
try:
    while True:
        print('*'*25)
        print('System Init')
        print('*'*25)
        #Safe Cond
        GPIO.output(23, GPIO.LOW) # Turn on Green
        GPIO.output(24, GPIO.HIGH) # Turn off Red
        
        while(IR_sensed < 2):
            start_time = time()
            GPIO.wait_for_edge(sensorPIN, GPIO.FALLING)
            GPIO.wait_for_edge(sensorPIN, GPIO.RISING)
            GPIO.wait_for_edge(sensorPIN, GPIO.FALLING)
            end_time = time()
            PyroRead = round((end_time - start_time)*1000000)
            # print(PyroRead)
            
            if(PyroRead > IR_threshold):
                IR_sensed += 1
        
        pulse = pulse + 1
        # print(pulse)
        print("Intruder Alert !!!")
        
        alert()
        
        PyroRead = 0
        IR_sensed = 0
        sleep(1)         # wait 1 second
        
except KeyboardInterrupt:
    print("clean up")
    # GPIO.cleanup([sensorPIN])
    GPIO.output(23, GPIO.HIGH) # Turn off Green
    GPIO.output(24, GPIO.HIGH) # Turn off Red
    GPIO.cleanup() # cleanup all GPIO

finally:
    print("clean up")
    # GPIO.cleanup([sensorPIN])
    GPIO.output(23, GPIO.HIGH) # Turn off Green
    GPIO.output(24, GPIO.HIGH) # Turn off Red
    GPIO.cleanup() # cleanup all GPIO
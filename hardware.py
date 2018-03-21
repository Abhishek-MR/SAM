#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
import paho.mqtt.client as mqtt
import subprocess
import urllib2
import speech_recognition as sr
import os
from time import ctime
import time
import datetime
import sys
from polly import Polly
tts = Polly('Matthew')

#globals
light=0
seeds=100
user1="Anuj"
user2="Abhishek"
user1s=300
user2s=300
waste=0
live=0

GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(26, GPIO.IN)

p=GPIO.PWM(22,50)
p.start(7.5)

#mqtt and callback
mqttc = mqtt.Client("client1", clean_session=False)
mqttc.username_pw_set("ptbelqhi", "wdJXMPWzv6Q5")
mqttc.connect("m13.cloudmqtt.com", 13476, 60)
def on_message(client, userdata, message):
     global light
     global seeds
     global user1
     global user2
     global user1s
     global user2s
     global live
     #all cases of subscibe
     #appliances
     if message.payload =="OFF":
         print "off"
         light=0
         
     if message.payload =="ON":
         print "on"
         light =1

     #home
     if "seedand" in message.payload:
         msg=message.payload.split();
         print "seed changed to "+msg[1]
         seed = int(msg[1])
         pub_seeds()

     #users
     if "userand" in message.payload:
         if "1" in message.payload:
              msg=message.payload.split();
              user1=msg[2]
              user1s=int(msg[4])
              pub_users()
         if "2" in message.payload :
              msg=message.payload.split();
              user2=msg[2]
              user2s=int(msg[4])
              pub_users()
      
     if message.payload =="y":
        live=1
     if message.payload =="n":
        live=2
    
     if message.payload =="0":
          p.ChangeDutyCycle(3.5)
     if message.payload =="1":
          p.ChangeDutyCycle(4.5)
     if message.payload =="2":
          p.ChangeDutyCycle(5.5)
     if message.payload =="3":
          p.ChangeDutyCycle(6.5)
     if message.payload =="4":
          p.ChangeDutyCycle(7.5)
     if message.payload =="5":
          p.ChangeDutyCycle(8.5)
     if message.payload =="6":
          p.ChangeDutyCycle(9.5)
     if message.payload =="7":
          p.ChangeDutyCycle(10.5)
     if message.payload =="8":
          p.ChangeDutyCycle(11.5)
     if message.payload =="9":
          p.ChangeDutyCycle(12.5)
         
mqttc.on_message= on_message





#publishing
def pub_seeds():
     global light
     global seeds
     global user1
     global user2
     global user1s
     global user2s
     pub("seedpi "+str(seeds))
    
def pub_users():
     global light
     global seeds
     global user1
     global user2
     global user1s
     global user2s
     
     pub("userpi 1 "+user1+" s "+str(user1s))
     pub("userpi 2 "+user2+" s "+str(user2s))
             
def pub(msg): 
     mqttc.publish("sensor/snd",msg,qos=1)
def livestream():
     global live
     if live == 1:
          cmd="raspivid -o - -t 99999 -w 640 -h 360 -fps 25|cvlc stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8090}' :demux=h264"
          pol = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)
     if live == 2:
          pol.kill()


#listening



i=0
j=0

marv=0
while (True) :
    global marv
    global live
    if marv==0:
         pub_seeds()
         pub_users()
         marv=marv+1
        
    mqttc.subscribe("top")
    rc = 0
        
    rc= mqttc.loop_start()

    
    #GPIO.output(22, True)
    i =GPIO.input(17)    
    if(i==1) :
        if light==0:  light=1
        elif light==1 :light=0

    if( light==1) :
        print "on"
        GPIO.output(27, True)
        if GPIO.input(26)==0 :
             waste+=1
             print "No one is present!!light is ON"
        else:
             print "light is ON !! People present"
    else :
        GPIO.output(27, False)

    if (waste==50) :
         print "WASTEAGE WARNING SENT!!"
         pub("waste")
         waste=0
         
    #time.sleep(0.3)
    rc= mqttc.loop_stop()    
    













   


#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
import urllib2
import speech_recognition as sr
import os
from time import ctime
import time
import datetime
import sys
from polly import Polly
tts = Polly('Matthew')
listensam=0
r = sr.Recognizer()
def sam_e(data) :
	print data
        if "what" in data :
                if "name" in data:
                        tts.say(" my name is sam ")    
                if "time" in data:
                        t = datetime.datetime.now().replace(microsecond=0)
                        tts.say("The time is ")
                        tts.say(t.strftime('%H:%M:%S'))
                if "date" in data:
                        t = datetime.datetime.now()
                        tts.say("The date is ")
                        tts.say(t.strftime('%m/%d/%Y')) 
	 	elif "how are you" in data:
                	tts.say("i am awesome as hell")
        else :
                tts.say("Sorry bro cant understand")
        

def listen():
        global listensam
        with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                if listensam is 0 :
                        tts.say(" Greetings user, Sam at your service, what can i do for you? ")
                        listensam=1
                else :
                        tts.say("what can i do for you? ")
                print("Say something!")
                audio = r.record(source, duration = 3)
        try:
                mytext= r.recognize_google(audio, language="en")
                print(mytext)
                return mytext
        except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                return "sorry could not understand"
        except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return "sorry could not understand"

while(1) :
        data="sorry i could not understand that"
        data=listen()
        sam_e(data)
        

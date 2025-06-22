import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
from googlesearch import search
import psutil
import sys
import os
import pywhatkit as pt
import time
import phonenumbers 
from phonenumbers import geocoder
from phonenumbers import carrier
import pyautogui
import sounddevice
from scipy.io.wavfile import write
import subprocess
import re

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning sir")
    elif hour >= 12 and hour < 16:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5  # Reduced for faster response
        r.adjust_for_ambient_noise(source, duration=0.5)  # Improve accuracy
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=7)  # Add timeouts
        except Exception as e:
            print("Listening timed out. Please try again...")
            return "None"
    try:
        query = r.recognize_google(audio, language='en-us')
        print("You said:", query)
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

def set_timer(query):
    # Extract time from query (e.g., 'set a timer for 5 minutes')
    match = re.search(r'(\d+)\s*(second|seconds|minute|minutes)', query)
    if not match:
        speak("Please specify the timer duration in seconds or minutes.")
        return
    value = int(match.group(1))
    unit = match.group(2)
    seconds = value * 60 if 'minute' in unit else value
    speak(f"Timer set for {value} {unit}.")
    time.sleep(seconds)
    speak("Time's up!")

if __name__ == '__main__':
    # Find a female voice id (default to first female, else fallback to first voice)
    female_voice_id = None
    for v in voices:
        if 'female' in v.name.lower() or 'female' in v.id.lower():
            female_voice_id = v.id
            break
    if not female_voice_id:
        female_voice_id = voices[0].id  # fallback
    male_voice_id = voices[0].id

    while True:
        query = takecommand()

        if 'liam' in query or 'liya' in query or 'lia' in query or 'can you hear me' in query:
            # Switch to female voice if 'lia' is detected, else use male
            if 'lia' in query:
                engine.setProperty('voice', female_voice_id)
            else:
                engine.setProperty('voice', male_voice_id)
            wishme()
            speak("How can I help you?")

            while True:
                query = takecommand()

                if "give me some details about" in query:
                    speak("Getting information from Wikipedia")
                    topic = query.replace("give me some details about", "")
                    results = wikipedia.summary(topic, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)

                elif 'open youtube' in query:
                    webbrowser.open("https://www.youtube.com")

                elif 'open google' in query:
                    webbrowser.open("https://www.google.com")

                elif 'open espncricinfo' in query:
                    webbrowser.open("https://www.espncricinfo.com")

                elif 'calculator' in query:
                    subprocess.call(["open", "/System/Applications/Calculator.app"])

                elif 'open whatsapp' in query:
                    webbrowser.open("https://web.whatsapp.com/")

                elif 'charge left' in query:
                    battery = psutil.sensors_battery()
                    if battery:
                        percentage = battery.percent
                        print(f"The charge left is {percentage}%")
                        speak(f"The charge left is {percentage} percent")

                elif 'open notes' in query:
                    subprocess.call(["open", "/System/Applications/Notes.app"])

                elif 'voice to text' in query:
                    result = takecommand()
                    print("You said:", result)

                elif 'play' in query and 'on youtube' in query:
                    pt.playonyt(query.replace("play", "").replace("on youtube", ""))

                elif 'google search' in query:
                    pt.search(query.replace("google search", ""))

                elif 'shutdown' in query:
                    speak("Shutting down. Bye Sir.")
                    os.system("sudo shutdown -h now")
                    sys.exit()

                elif 'record' in query:
                    speak("How long should I record in seconds?")
                    duration = int(takecommand())
                    speak("Recording...")
                    fps = 44100
                    recording = sounddevice.rec(int(duration * fps), samplerate=fps, channels=1)
                    sounddevice.wait()
                    write("output.wav", fps, recording)
                    speak("Recording saved")

                elif 'play the recording' in query:
                    subprocess.call(["afplay", "output.wav"])

                elif "set an alarm at" in query:
                    alarm_time = query.replace("set an alarm at", "").strip()
                    speak(f"Alarm set for {alarm_time}")
                    while True:
                        now = datetime.datetime.now().strftime("%H:%M")
                        if now == alarm_time:
                            for _ in range(5):
                                speak("Wake up sir")
                            break
                        time.sleep(30)

                elif 'set a timer for' in query:
                    set_timer(query)

                elif 'exit' in query or 'stop' in query:
                    speak("Goodbye sir")
                    break

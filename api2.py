import os
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
from datetime import datetime
import pyttsx3
import tkinter as tk

# Set up the Vosk model
model_path = "vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    print(f"Model not found at {model_path}")
    exit(1)

model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()
listening = False  # Flag to control listening state

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))

def process_command(command):
    command = command.lower()
    if "play music" in command:
        print("Playing music...")
        # Add code to play music
    elif "what's the time" in command:
        current_time = datetime.now().strftime("%H:%M")
        print(f"The current time is {current_time}.")
        speak(f"The current time is {current_time}.")
    elif "thank you" in command:
        print("You're welcome!")
        speak("You're welcome!")

def recognize_speech():
    global listening
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("Listening...")
        while listening:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result)['text']
                if text:
                    print("Final recognized text:", text)
                    process_command(text)

def start_listening():
    global listening
    listening = True  # Set listening to true
    recognize_speech()  # Call the function directly

def stop_listening():
    global listening
    listening = False  # Set listening to false
    print("Stopped listening.")

# Set up the GUI
root = tk.Tk()
root.title("Voice Assistant")

# Set the window size (width x height)
root.geometry("600x400")  # Example: 600 pixels wide and 400 pixels tall

start_button = tk.Button(root, text="Start Listening", command=start_listening)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Listening", command=stop_listening)
stop_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", stop_listening)  # Ensure listening stops on window close
root.mainloop()  # Keep the window open

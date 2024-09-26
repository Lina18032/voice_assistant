import os
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
from datetime import datetime
import pyttsx3

model_path = "vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    print(f"Model not found at {model_path}")
    exit(1)

model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))
    
def process_command(command):
    command = command.lower()  # Convert to lowercase for easier matching

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
    #else:
        #print("Sorry, I didn't understand the command.")
        #speak("Sorry, I didn't understand that.")


def recognize_speech():
    """Capture and recognize speech from the microphone"""
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("Listening...")

        while True:
            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result)['text']
                if text:
                    print("Final recognized text:", text)
                    process_command(text)  # Call the command processing function
            #else:
                #partial_result = recognizer.PartialResult()
                #partial_text = json.loads(partial_result)['partial']
                #print("Partial result:", partial_text)


#def microphone_test():
    #print("Starting microphone test... Speak now.")
    #with sd.InputStream(callback=lambda *args: print("Receiving audio")):
        #sd.sleep(5000)
        


if __name__ == "__main__":
    #microphone_test()
    recognize_speech()
    process_command()

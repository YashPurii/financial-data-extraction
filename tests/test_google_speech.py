# import speech_recognition as sr

# recognizer = sr.Recognizer()
# audio_path = "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/raw/test.wav"  # Use a small WAV file

# with sr.AudioFile(audio_path) as source:
#     audio = recognizer.record(source)  # Read entire file

# try:
#     print("Google Speech Recognition Output:\n", recognizer.recognize_google(audio))
# except sr.RequestError:
#     print("🔴 Could not request results from Google Speech API.")
# except sr.UnknownValueError:
#     print("🔴 Google Speech API could not understand the audio.")

import speech_recognition as sr

recognizer = sr.Recognizer()
audio_path = "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/raw/sample-short.wav"

with sr.AudioFile(audio_path) as source:
    audio = recognizer.record(source)  # Read entire file

try:
    print("\n🔹 Google Speech Recognition Output:")
    print(recognizer.recognize_google(audio))
except sr.RequestError:
    print("🔴 Could not request results from Google Speech API.")
except sr.UnknownValueError:
    print("🔴 Google Speech API could not understand the audio.")

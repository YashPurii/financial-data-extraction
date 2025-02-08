import PyPDF2
import pytesseract
from PIL import Image
import speech_recognition as sr
from pydub import AudioSegment
import os
import json
import csv

# Set Tesseract path (Windows users)
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---------------- PDF Extraction ----------------
def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    extracted_text = []
    
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            extracted_text.append(page.extract_text())

    return "\n".join(filter(None, extracted_text))  # Join non-empty text lines

# ---------------- Image OCR Extraction ----------------
def extract_text_from_image(image_path):
    """Extracts text from an image using OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error processing image: {e}"

# ---------------- Audio Transcription ----------------
# import subprocess
# import os

# def convert_mp3_to_wav(mp3_path):
#     """Automatically trims and converts an MP3 file to a 16kHz WAV file."""
    
#     # Generate new filenames
#     trimmed_mp3 = mp3_path.replace(".mp3", "-short.mp3")
#     wav_path = mp3_path.replace(".mp3", "-short.wav")

#     # Step 1: Trim the MP3 file to 30 seconds
#     trim_command = [
#         "ffmpeg", "-i", mp3_path, "-t", "30", "-acodec", "copy", trimmed_mp3, "-y"
#     ]
#     subprocess.run(trim_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

#     # Step 2: Convert trimmed MP3 to WAV with required specifications
#     convert_command = [
#         "ffmpeg", "-i", trimmed_mp3, "-ar", "16000", "-ac", "1", "-ab", "32k", wav_path, "-y"
#     ]
#     subprocess.run(convert_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

#     # Check if conversion was successful
#     if os.path.exists(wav_path):
#         return wav_path
#     else:
#         raise Exception("🔴 FFmpeg conversion failed: No WAV file generated.")



# def transcribe_audio_google(audio_path):
#     """Transcribes audio using Google Speech Recognition (free alternative)."""
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_path) as source:
#         audio = recognizer.record(source)  # Read entire audio file

#     try:
#         return recognizer.recognize_google(audio)
#     except sr.UnknownValueError:
#         return "Google Speech API could not understand the audio."
#     except sr.RequestError:
#         return "Could not request results from Google Speech API."

import subprocess
import os
import math
import speech_recognition as sr
from pydub import AudioSegment

def convert_mp3_to_wav(mp3_path):
    """Splits MP3 into 30-second chunks and converts each to WAV."""
    
    # Load audio file
    audio = AudioSegment.from_mp3(mp3_path)
    duration_sec = len(audio) / 1000  # Convert milliseconds to seconds
    num_chunks = math.ceil(duration_sec / 30)  # Number of 30-second segments

    wav_files = []

    for i in range(num_chunks):
        start_time = i * 30 * 1000  # Convert to milliseconds
        end_time = min((i + 1) * 30 * 1000, len(audio))
        chunk = audio[start_time:end_time]

        chunk_mp3 = mp3_path.replace(".mp3", f"-chunk{i}.mp3")
        chunk_wav = mp3_path.replace(".mp3", f"-chunk{i}.wav")

        chunk.export(chunk_mp3, format="mp3")

        # Convert each MP3 chunk to WAV
        convert_command = [
            "ffmpeg", "-i", chunk_mp3, "-ar", "16000", "-ac", "1", "-ab", "32k", chunk_wav, "-y"
        ]
        subprocess.run(convert_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        wav_files.append(chunk_wav)

    return wav_files  # Returns a list of chunked WAV files

def transcribe_audio_google(audio_files):
    """Transcribes multiple WAV chunks and merges the text."""
    recognizer = sr.Recognizer()
    full_transcription = ""

    for audio_path in audio_files:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)  # Read chunk

        try:
            text = recognizer.recognize_google(audio)
            full_transcription += text + " "  # Append each chunk's transcription
        except sr.UnknownValueError:
            full_transcription += "[Unrecognized audio] "
        except sr.RequestError:
            full_transcription += "[Google API Error] "

    return full_transcription.strip()  # Return full transcribed text

# ---------------- Save to JSON ----------------
def save_to_json(data, output_path):
    """Saves extracted data to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

# ---------------- Save to CSV ----------------
def save_to_csv(data, output_path):
    """Saves extracted data to a CSV file."""
    with open(output_path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Source", "Extracted Text"])  # Header

        for source, text in data.items():
            writer.writerow([source, text])

# ---------------- Main Execution ----------------
if __name__ == "__main__":
    extracted_data = {}

    # Define input file paths
    pdf_file = "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/raw/sample-invoice.pdf"
    image_file = "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/raw/Balance-Sheet.jpg"
    mp3_file = "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/raw/NPR1180246583.mp3"

    # Extract data
    extracted_data["PDF"] = extract_text_from_pdf(pdf_file)
    extracted_data["Image"] = extract_text_from_image(image_file)

    # Convert MP3 to WAV
    wav_file = convert_mp3_to_wav(mp3_file)
    extracted_data["Audio"] = transcribe_audio_google(wav_file)

    # Save extracted data to JSON and CSV
    save_to_json(extracted_data, "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/processed/extracted_data.json")
    save_to_csv(extracted_data, "C:/Users/yashp/OneDrive/Desktop/financial-data-extraction/data/processed/extracted_data.csv")

    # Print output confirmation
    print("\n✅ Data Extraction Completed!")
    print("📂 Extracted data saved to: \n- extracted_data.json\n- extracted_data.csv")

import os
import sys
venv_path = '/home/sona-inc5619/mp_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)



import pyaudio
import wave
import time
import sys
import struct
import math
from faster_whisper import WhisperModel
import ollama
import pyttsx3
import threading

engine = pyttsx3.init()

model_size = "base"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

CHUNK = 1024 # Number of samples in one frame
RATE = 16000 # Sampling rate
FORMAT = pyaudio.paInt16
CHANNELS = 1

# The volume threshold below which we consider that the user is "silent"
THRESHOLD = 100

# How many consecutive seconds should I be "silent" to stop recording
SILENCE_LIMIT = 3.0

# store the entire history of the dialog here
messages = []

def rms(data):
    """
    Calculate the approximate volume (RMS) for one byte block.
    data: byte string read from PyAudio
     """
    count = len(data) // 2 # Number of samples in int16 format
    format_str = "<" + "h" * count
    shorts = struct.unpack_from(format_str, data)

    sum_squares = 0.0
    for sample in shorts:
        sum_squares += sample * sample

    if count == 0:
        return 0

    return math.sqrt(sum_squares / count)

def record_once(filename="audio.wav"):
    """
   We record one fragment of speech (until 'silence') and save it to a WAV file.
    We return the path to the recorded file.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    print("Start of recording (speak)...")

    silence_counter = 0 # Counter of "silent" chunks
    
    
    while True:
      data = stream.read(CHUNK)
      frames.append(data)
        # Calculate the volume of the current CHUNK
      current_rms = rms(data)
      if current_rms < THRESHOLD:
# Volume below threshold => "silence"
            silence_counter += 1
      else:
         silence_counter = 0
# If the total length of silent blocks has exceeded SILENCE_LIMIT seconds, exit
      if silence_counter * (CHUNK / RATE) > SILENCE_LIMIT:
        break
        print("Recording completed.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save it to a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return filename

def transcribe(filename):
  """
     We recognize the file using faster_whisper.
    Returning the recognized text.
     """
  segments, info = model.transcribe(filename, beam_size=8)
  print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
  texts = ''
  for segment in segments:
        texts += segment.text
        return texts

def main():
    while True:
        #  Recording a fragment of speech
        audio_path = record_once("audio.wav")
#  Recognize
        user_text = transcribe(audio_path)
# If recognition suddenly returns an empty string, skip it
        if not user_text.strip():
         print("The user did not say anything or was not recognized, we continue to listen...")
         continue

        print("The user said:", user_text)

        #Add to the history as a new message from the user
        messages.append({"role": "user", "content": user_text})

        # Sending  to Ollama
        response = ollama.chat(
            model="llama3",
            messages=messages,
        )
        #  Extracting the response text
        assistant_text = response['message']['content']
        print("Assistant replied:", assistant_text)

        #  Save the assistant's response to the history
        messages.append({"role": "assistant", "content": assistant_text})

        # TTS
        engine.say(assistant_text)
engine.runAndWait()

if __name__ == "__main__":
    main()
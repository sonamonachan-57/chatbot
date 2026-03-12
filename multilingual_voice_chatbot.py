import sounddevice as sd
from scipy.io.wavfile import write
from groq import Groq
from gtts import gTTS
import re
import webrtcvad
import queue
import sys
import numpy as np






# -----------------------------
# API KEYS
# -----------------------------

GROQ_API_KEY = "API key here"

client = Groq(api_key=GROQ_API_KEY)


# -----------------------------
# Audio settings
# -----------------------------

sample_rate = 16000
duration = 10

# -----------------------------
# Conversation memory
# -----------------------------

full_transcript = [
    {
        "role": "system",
        "content": f"""
You are a assistant.
give proper reply to the user's question
Be polite, helpful, and efficient.
Reply in the user's language.

If the user speaks Malayalam, respond in natural Malayalam.
"""
    }
]



# -----------------------------
# Record Audio
# -----------------------------

def record_audio():

    print("\n🎤 Speak now...\n")

    vad = webrtcvad.Vad(2)

    frame_duration = 30
    frame_size = int(sample_rate * frame_duration / 1000)

    stream = sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype='int16',
        blocksize=frame_size
    )

    speech_frames = []
    speech_started = False

    silence_limit = 20
    silence_count = 0

    speech_confirm_frames = 5
    speech_counter = 0

    with stream:

        while True:

            frame, _ = stream.read(frame_size)

            frame_bytes = frame.tobytes()

            is_speech = vad.is_speech(frame_bytes, sample_rate)

            # wait for speech start
            if not speech_started:

                if is_speech:
                    speech_counter += 1

                    if speech_counter > speech_confirm_frames:
                        print("🎙 Speech detected, recording...")
                        speech_started = True
                        speech_frames.append(frame)

                else:
                    speech_counter = 0

            else:

                speech_frames.append(frame)

                if is_speech:
                    silence_count = 0
                else:
                    silence_count += 1

                if silence_count > silence_limit:
                    print(" Silence detected, stopping recording")
                    break

    import numpy as np

    audio_data = np.concatenate(speech_frames, axis=0)

    filename = "input.wav"

    write(filename, sample_rate, audio_data)

    return filename


# -----------------------------
# Speech → Text
# -----------------------------

def speech_to_text(audio_file):

    with open(audio_file, "rb") as file:

        transcription = client.audio.transcriptions.create(
            file=(audio_file, file.read()),
            model="whisper-large-v3",
            temperature=0,
            response_format="verbose_json",
        )

    print("Patient:", transcription.text)
    print("Detected language:", transcription.language)

    return transcription.text, transcription.language


# -----------------------------
# LLM Response
# -----------------------------

def generate_ai_response(user_text):

    full_transcript.append(
        {"role": "user", "content": user_text}
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=full_transcript,
        temperature=0.7,
        max_tokens=500
    )

    ai_text = response.choices[0].message.content

    full_transcript.append(
        {"role": "assistant", "content": ai_text}
    )

    print("\nAI Bot:", ai_text)
    
    

    return ai_text


# -----------------------------
# Text → Speech
# -----------------------------

def speak(text, lang):

    text = re.sub(r"\s+", " ", text).strip()

    lang_map = {
        "ml": "ml",
        "Malayalam": "ml",
        "en": "en",
        "English": "en",
        "hi": "hi",
        "Hindi": "hi",
        "ta": "ta",
        "Tamil": "ta"
    }

    lang = lang_map.get(lang, "en")

    print("Speaking language:", lang)

    tts = gTTS(text=text, lang=lang)

    filename = "response.mp3"
    tts.save(filename)

    os.system(f"mpg123 {filename}")


# -----------------------------
# Main Loop
# -----------------------------

def main():

    greeting = "My name is Sarah. How may I assist you?"

    print("AI Bot:", greeting)

    speak(greeting, "en")

    while True:

      audio_file = record_audio()

      if audio_file is None:
        continue

      user_text, detected_lang = speech_to_text(audio_file)

      if not user_text:
        continue

      ai_response = generate_ai_response(user_text)

      speak(ai_response, detected_lang)

# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":

    print("\nAI Bot started\n")

    main()




    




import speech_recognition as sr

# Create recognizer object
recognizer = sr.Recognizer()

# Use microphone as source
with sr.Microphone() as source:
    print("Adjusting for background noise...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Please speak now...")
    audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print("You said:", text)

    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")

    except sr.RequestError as e:
        print("Could not request results; check your internet connection.")

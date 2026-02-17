1. Speech to text using speech recognition

   A basic real-time Speech Recognition project built using Python and the SpeechRecognition library.
   This program captures audio from the microphone and converts it into text using Google's Speech Recognition API.

Features:

   Captures live audio from microphone

   Adjusts for background noise

  Converts speech to text using Google API

  Handles errors gracefully

  Beginner-friendly implementation


Technologies used:

        Python 3.x
        SpeechRecognition
        PyAudio
        Google Web Speech API

Install dependencies:

     pip install SpeechRecognition
     pip install pyaudio

How it works:
   Recognizer() initializes the speech recognizer
   Microphone() captures live audio
   adjust_for_ambient_noise() reduces background noise
   recognize_google() converts speech into text

Output:



2.Customer service robot (rule based)

A simple rule-based Customer Service Chatbot built using Python and NLTK.
The chatbot detects user intent using basic Natural Language Processing (tokenization + keyword matching) and responds accordingly.


Features:

  Uses NLP tokenization (word_tokenize)

  Handles greetings and farewells

  Supports order tracking queries

  Handles refund/return requests

  Responds to complaints

  Object-Oriented implementation


Technologies used:

       Python 3.x
       NLTK (Natural Language Toolkit)
       Rule-Based NLP Approach

Install dependencies:
       
       pip install nltk
Download required NLTK data:
         
         import nltk
         nltk.download('punkt')

How it works:

   User input is converted to lowercase

   Text is tokenized using word_tokenize()

   Tokens are matched against predefined keyword lists

  Appropriate response is returned


Output:

   

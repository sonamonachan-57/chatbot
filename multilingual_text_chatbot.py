from langdetect import detect
import ollama


# Detect language
def detect_language(text):

    try:
        lang = detect(text)
    except:
        lang = "en"

    return lang


# Generate AI response
def generate_answer(question):

    prompt = f"""
User question: {question}

Reply in the SAME language as the user.
Do not translate to English.
Give a natural conversational reply.
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response['message']['content']

    return answer


# Chat loop
def main():

    print("\n Multilingual Text Chatbot")
    print("Type 'exit' to quit\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        language = detect_language(user_input)

        print("Detected Language:", language)

        answer = generate_answer(user_input)

        print("Bot:", answer)


if __name__ == "__main__":
    main()




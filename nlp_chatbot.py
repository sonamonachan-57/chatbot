import os
import sys
venv_path = '/home/sona-inc5619/chat_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)




import nltk
from nltk.tokenize import word_tokenize

class CustomerServiceBot:
    def __init__(self):
        self.greetings = ["hello", "hi","hai","hii" "hey"]
        self.farewells = ["bye", "goodbye", "see you"]
        self.order_keywords = ["order", "track", "delivery", "shipping"]
        self.refund_keywords = ["refund", "return", "money back"]
        self.complaint_keywords = ["complaint", "problem", "issue", "bad"]

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        return tokens

    def respond(self, user_input):
        tokens = self.preprocess(user_input)

        # Greeting
        if any(word in tokens for word in self.greetings):
            return "Hello! How can I assist you today?"

        # Order tracking
        elif any(word in tokens for word in self.order_keywords):
            return "Please provide your order ID. I will help you track it."

        # Refund
        elif any(word in tokens for word in self.refund_keywords):
            return "I'm sorry to hear that. Please share your order ID to initiate a refund."

        # Complaint
        elif any(word in tokens for word in self.complaint_keywords):
            return "We apologize for the inconvenience. Could you please describe the issue in detail?"

        # Farewell
        elif any(word in tokens for word in self.farewells):
            return "Thank you for contacting us. Have a great day!"

        else:
            return "I'm sorry, I didn't understand that. Could you please rephrase?"

# Run chatbot
if __name__ == "__main__":
    bot = CustomerServiceBot()
    print("Customer Service Bot: Type 'exit' to end conversation.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Bot: Goodbye!")
            break

        response = bot.respond(user_input)
        print("Bot:", response)

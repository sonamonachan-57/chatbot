
import os
import sys
venv_path = '/home/sona-inc5619/mp_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)

import ollama
history=[]
model="llama3"
while True:
    prompt=input("you: ").strip()
    if prompt.lower()in('exit','quit'):
        print("have a nice day")
        break
    message={
        "role":"user",
        "content":prompt       
    }
    history.append(message)
    response=ollama.chat(model=model, messages=history)
    bot_message_content=response.message.content
    print(f"Bot:{bot_message_content}")
    bot_message={
        "role":"assistant",
        "content":bot_message_content
    }
    history.append(bot_message)
    
    
    #this python code converted to ros2 node
    
import os
import sys
venv_path = '/home/sona-inc5619/mp_env/lib/python3.12/site-packages'
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)

import ollama
import rclpy
from rclpy.node import Node

history = []
model = "llama3"

class ChatBot(Node):

    def __init__(self):
        super().__init__('chatbot_node')
        self.timer = self.create_timer(1.0, self.chat_loop)

    def chat_loop(self):
        prompt = input("you: ").strip()

        if prompt.lower() in ('exit', 'quit'):
            self.get_logger().info("Have a nice day")
            rclpy.shutdown()
            return

        message = {
            "role": "user",
            "content": prompt
        }

        history.append(message)

        response = ollama.chat(model=model, messages=history)
        bot_message_content = response['message']['content']

        self.get_logger().info(f"Bot: {bot_message_content}")

        bot_message = {
            "role": "assistant",
            "content": bot_message_content
        }

        history.append(bot_message)


def main(args=None):
    rclpy.init(args=args)
    node = ChatBot()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

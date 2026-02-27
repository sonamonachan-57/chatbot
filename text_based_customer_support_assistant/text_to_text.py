import ollama

#load product manual

with open("product_manual.txt","r",encoding="utf-8") as f:
    manual_text=f.read()
    manual_sections=manual_text.split("\n\n")
    
#simple retrieval function

def retrieve_answer(query):
    query=query.lower()
    for section in manual_sections:
        if any(word in section.lower() for word in query.split()):
            return section
        return None


history=[]
model="llama3"



while True:
     prompt=input("you: ").strip()
     if prompt.lower() in ('exit', 'quit'):
         print("have a nice day")
         break
    #retrieve from manual
     retrieved_section=retrieve_answer(prompt)
     if retrieved_section:
         
        advanced_prompt=f"""
                        you are a  regional customer support assistant.Answer clearly using the product information.
                         product manual info:{retrieved_section}
                      user question:{prompt}
                        """
     else:
         advanced_prompt=f"""
                         you are a customer support assistant. If the answer is not in the product manual.say:"I am transferring you to a human support agent."
                         user Question:
                         {prompt}
                         """
     #add to history
     message={
         "role":"user",
        
         "content": advanced_prompt
     }
     history.append(message)
     #ollama bot
     response=ollama.chat(model=model,messages=history)
     bot_message_content=response["message"]["content"]  
     print(f"Bot: {bot_message_content}")
     
     #store assistant reply
     
     bot_message={
         "role":"assistant",
         "content": bot_message_content
     }
     history.append(bot_message)
       
    
    

   
 
      
   

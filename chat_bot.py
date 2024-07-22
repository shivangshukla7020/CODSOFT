import random as rd  # Importing random to chose from the responses

# The data set for questions and responses
greet = ["hello","hi","hey","what's up","hey chatbot"]
greet_response = ["Hello Sir","Hey","Nice to meet you","Hey, how are you","What's up !","I'm tired but let me know your query"]
ask_name = ["what is your name", "your name ?", "what can I call you","who are you","tell me your name","name"]
ask_name_response = ["I'm shiBot your personal chatbot","I'm a chat bot named shiBot","Everyone call me shiBot","Shibot"]
bye_greet = ["ok bye", "see ya","have a good day","it was good to meet you","see you later","goodbye","bye","tata"]
bye_greet_response = ["Bye!","Good Bye !","Take Care! Bye","See you later","Enjoy your day","See you later","bubbye"]
age = ["age","what is your age","who made you","your age ?","your age ?","tell me your age"]
age_response = ["I dont't know just arrived here !","maybe a century","two eternity","I think..............","age ? Don't ask me that"]
default = ["I'm sorry, I don't understand. Can you please repeat ?","I dont know that please do (greet,name,bye,age), Only - greet,name,bye,age"]

# answer functions responds according to the questions asked (Must follow rules)
def answer(question):
  if question in greet:
    return rd.choice(greet_response)
  
  if question in ask_name:
    return rd.choice(ask_name_response)
  
  if question in bye_greet:
    return rd.choice(bye_greet_response)
  
  if question in age:
    return rd.choice(age_response)
  
  return rd.choice(default)
  

print("\n=============== Hello, This is a rule Based ChatBot ============================")
print("""The rules are : 
      - You can greet(hi,hello,bye) 
      - ask name  
      - ask age
      - type 'exit' to quit""")

# While loop for continuous chat, breaks when user types 'exit'
while(True):
  user_input = input().lower()
  if user_input == "exit":
    break
  print(answer(user_input))



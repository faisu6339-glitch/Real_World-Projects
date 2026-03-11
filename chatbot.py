import json
import random

# Load the chatbot responses from a JSON file
with open("intent.json") as file:
    data = json.load(file)

# Function to get a random response based on the user's input
def chatbot_response(user_input):
    user_input = user_input.lower()

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern in user_input:
                return random.choice(intent["responses"])
    return "I'm sorry, I don't understand. Can you please rephrase?"
print("Hello! I'm a chatbot. How can I assist you today?")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye! Have a great day!")
        break
    response = chatbot_response(user_input)
    print(f"Chatbot: {response}")
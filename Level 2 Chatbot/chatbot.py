import json
import random

# Load intents
def load_intents():
    with open("intent.json", "r") as file:
        return json.load(file)

# Save intents
def save_intents(data):
    with open("intent.json", "w") as file:
        json.dump(data, file, indent=4)

# Get response
def chatbot_response(user_input, data):
    user_input = user_input.lower()

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_input:
                return random.choice(intent["responses"])

    return None


print("Hello! I'm a chatbot. Type 'quit' to exit.")

data = load_intents()

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Chatbot: Goodbye!")
        break

    response = chatbot_response(user_input, data)

    if response:
        print("Chatbot:", response)

    else:
        print("Chatbot: I don't know the answer to that.")
        new_answer = input("Please tell me the correct answer: ")

        # Save new question & answer
        new_intent = {
            "tag": user_input,
            "patterns": [user_input],
            "responses": [new_answer]
        }

        data["intents"].append(new_intent)
        save_intents(data)

        print("Chatbot: Thanks! I learned something new.")
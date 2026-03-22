import json
import random
import difflib
from textblob import TextBlob


def load_intents():
    with open("intent.json", "r") as file:
        return json.load(file)


def save_intents(data):
    with open("intent.json", "w") as file:
        json.dump(data, file, indent=4)


def correct_spelling(text):
    blob = TextBlob(text)
    return str(blob.correct())


def find_best_match(user_input, patterns):
    match = difflib.get_close_matches(user_input, patterns, n=1, cutoff=0.6)
    return match[0] if match else None


def chatbot_response(user_input, data):

    user_input = correct_spelling(user_input.lower())

    all_patterns = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            all_patterns.append(pattern.lower())

    best_match = find_best_match(user_input, all_patterns)

    if best_match:
        for intent in data["intents"]:
            if best_match in [p.lower() for p in intent["patterns"]]:
                return random.choice(intent["responses"])

    return None


print("Hello! I'm an AI chatbot. Type 'quit' to exit.")

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
        print("Chatbot: I don't understand this question.")
        new_answer = input("Please teach me the correct answer: ")

        new_intent = {
            "tag": user_input.lower(),
            "patterns": [user_input.lower()],
            "responses": [new_answer]
        }

        data["intents"].append(new_intent)

        save_intents(data)

        # IMPORTANT: reload updated data
        data = load_intents()

        print("Chatbot: Thanks! I learned something new.")
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Load knowledge with UTF-8 (FIXES YOUR ERROR 🔥)
with open("knowledge.json", encoding="utf-8") as f:
    knowledge = json.load(f)["data"]

# 🔥 Build pattern list
all_patterns = []
answers = []

for item in knowledge:
    for pattern in item["patterns"]:
        all_patterns.append(pattern.lower())
        answers.append(item["answer"])

# ✅ Handle empty case
if not all_patterns:
    all_patterns = ["hello"]
    answers = ["Hello!"]

# 🔥 Train vectorizer once
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_patterns)


# 🔍 FIND BEST MATCH
def find_best_match(user_input):
    user_input = user_input.lower()

    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, X)

    best_score = similarity.max()
    best_index = similarity.argmax()

    return answers[best_index], best_score


# 🤖 CHAT RESPONSE
def chatbot_response(user_input):
    answer, score = find_best_match(user_input)

    if score > 0.5:
        return answer
    else:
        return None


# 🧠 SELF-LEARNING (IMPROVED 🔥)
def learn(user_input, answer):
    global knowledge, all_patterns, answers, X

    user_input = user_input.lower()

    # ✅ Duplicate check
    existing_answer, score = find_best_match(user_input)

    if score > 0.85:
        return "⚠️ I already know something similar!"

    # ✅ Add new knowledge
    new_entry = {
        "patterns": [user_input],
        "answer": answer
    }

    knowledge.append(new_entry)

    # ✅ Save safely with UTF-8 + emoji support
    with open("knowledge.json", "w", encoding="utf-8") as f:
        json.dump({"data": knowledge}, f, indent=4, ensure_ascii=False)

    # 🔄 Update runtime memory (NO RESTART 🔥)
    all_patterns.append(user_input)
    answers.append(answer)

    X = vectorizer.fit_transform(all_patterns)

    return "✅ Learned successfully!"
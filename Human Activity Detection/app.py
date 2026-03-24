import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load models
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
pca = joblib.load('pca.pkl')
le = joblib.load('label_encoder.pkl')

st.set_page_config(page_title="HAR App", layout="centered")

st.title("🏃 Human Activity Recognition App")

# =====================================
# 🔹 SECTION 1: CSV UPLOAD (FIXED)
# =====================================

st.subheader("📂 Upload CSV for Accurate Prediction")

file = st.file_uploader("Upload CSV file", type=["csv"])

if file:
    data = pd.read_csv(file)

    # 🔥 REMOVE NON-NUMERIC COLUMNS (IMPORTANT FIX)
    data = data.drop(columns=['Activity', 'subject'], errors='ignore')

    # Keep only numeric columns (extra safety)
    data = data.select_dtypes(include=['float64', 'int64'])

    # Check shape
    if data.shape[1] != scaler.n_features_in_:
        st.error(f"❌ Feature mismatch! Expected {scaler.n_features_in_} columns.")
    else:
        data_scaled = scaler.transform(data)
        data_pca = pca.transform(data_scaled)

        preds = model.predict(data_pca)
        result = le.inverse_transform(preds)

        st.success("✅ Predictions:")
        st.write(result)


# =====================================
# 🔹 SECTION 2: MANUAL INPUT
# =====================================

st.subheader("🎛️ Manual Input (Demo - Top 10 Features)")

features = [
    'tBodyAcc-mean()-X',
    'tBodyAcc-mean()-Y',
    'tBodyAcc-mean()-Z',
    'tBodyAcc-std()-X',
    'tBodyAcc-std()-Y',
    'tBodyAcc-std()-Z',
    'tBodyAcc-max()-X',
    'tBodyAcc-max()-Y',
    'tBodyGyro-mean()-X',
    'tBodyGyro-std()-X'
]

inputs = []

for col in features:
    val = st.slider(col, -1.0, 1.0, 0.0)
    inputs.append(val)

input_data = np.array(inputs).reshape(1, -1)

# Create full input
total_features = scaler.n_features_in_
full_input = np.zeros((1, total_features))
full_input[0, :len(inputs)] = input_data


# =====================================
# 🔹 PREDICT BUTTON
# =====================================

if st.button("🔍 Predict Activity"):

    input_scaled = scaler.transform(full_input)
    input_pca = pca.transform(input_scaled)

    prediction = model.predict(input_pca)
    result = le.inverse_transform(prediction)[0]

    probs = model.predict_proba(input_pca)
    confidence = np.max(probs)

    if result == "WALKING":
        st.success("🚶 Walking Detected")

    elif result == "WALKING_UPSTAIRS":
        st.success("🧗 Walking Upstairs Detected")

    elif result == "WALKING_DOWNSTAIRS":
        st.success("⬇️ Walking Downstairs Detected")

    elif result == "SITTING":
        st.success("🪑 Sitting Detected")

    elif result == "STANDING":
        st.success("🧍 Standing Detected")

    elif result == "LAYING":
        st.success("🛌 Laying Detected")

    else:
        st.info(f"Prediction: {result}")

    st.info(f"Confidence: {confidence:.2f}")


# =====================================
# 🔹 PRESET SIMULATION
# =====================================

st.subheader("⚡ Quick Simulation")

col1, col2 = st.columns(2)

with col1:
    if st.button("🛌 Simulate LAYING"):
        demo_input = np.zeros((1, total_features))

        demo_scaled = scaler.transform(demo_input)
        demo_pca = pca.transform(demo_scaled)

        pred = model.predict(demo_pca)
        result = le.inverse_transform(pred)[0]

        st.success(f"🛌 {result}")


with col2:
    if st.button("🚶 Simulate WALKING"):
        demo_input = np.random.uniform(-1, 1, (1, total_features))

        demo_scaled = scaler.transform(demo_input)
        demo_pca = pca.transform(demo_scaled)

        pred = model.predict(demo_pca)
        result = le.inverse_transform(pred)[0]

        st.success(f"🚶 {result}")


# =====================================
# 🔹 SIDEBAR
# =====================================

st.sidebar.title("ℹ️ About")
st.sidebar.info("""
This app predicts human activities using a machine learning model.

✔ Model: RandomForest / XGBoost  
✔ Features: Sensor-based signals  
✔ Accuracy: ~97%  

💡 Use CSV upload for best results.
""")
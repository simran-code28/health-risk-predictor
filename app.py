# app.py
import streamlit as st
import pandas as pd
import joblib

# ---------------- Authentication ----------------
USER_CREDENTIALS = {
    "doctor": "doc123",
    "nurse": "nurse123",
}

st.set_page_config(page_title="Health Risk Predictor", page_icon="🩺", layout="centered")

st.title("🔐 Rural Health Risk Predictor")

# Session state for login
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Login Page
if not st.session_state["authenticated"]:
    st.subheader("🔑 Please Login to Continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success(f"✅ Welcome {username}!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")
    st.stop()  # stop execution until login

# ---------------- Prediction Code (runs only after login) ----------------
st.sidebar.success(f"👋 Logged in as: {st.session_state['username']}")

# Logout button
if st.sidebar.button("🚪 Logout"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.rerun()

# ---------------- Model Load ----------------
model = joblib.load("./models/health_model.pkl")

st.header("🩺 Patient Health Risk Prediction")

# Input fields
age = st.number_input("Age", 0, 100, 25)
bmi = st.number_input("BMI", 10.0, 50.0, 22.5)
bp = st.number_input("Blood Pressure", 50, 200, 120)
sugar = st.number_input("Sugar Level", 50, 400, 100)
pa = st.radio("Physical Activity", [0, 1], index=1)
smoke = st.radio("Smoking", [0, 1], index=0)

# Patient Details Table
input_data = pd.DataFrame([[age, bmi, bp, sugar, pa, smoke]],
                          columns=["age", "bmi", "blood_pressure", "sugar_level", "physical_activity", "smoking"])

st.subheader("📋 Patient Details")
st.dataframe(input_data, hide_index=True)

# Prediction
if st.button("Predict Risk"):
    pred = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]

    risk_label = "Low Risk of Disease" if pred == 0 else "High Risk of Disease"
    confidence = round(max(proba) * 100, 2)

    st.subheader("Result")
    if pred == 0:
        st.success(f"✅ {risk_label} (Confidence: {confidence}%)")
    else:
        st.error(f"🚨 {risk_label} (Confidence: {confidence}%)")

    # Recommendations
    st.markdown("### 📝 Recommendations")
    tips = []
    if smoke == 1: tips.append("• Quit smoking or seek cessation support.")
    if pa == 0: tips.append("• Aim for ≥30 mins moderate exercise daily.")
    if bmi >= 25: tips.append("• Work towards a healthy BMI with balanced diet.")
    if bp >= 130: tips.append("• Monitor BP; reduce salt and manage stress.")
    if sugar >= 140: tips.append("• Limit refined sugar; check fasting glucose regularly.")
    if not tips:
        tips = ["• Keep up the healthy habits! Maintain regular checkups."]
    st.write("\n".join(tips))

    st.caption("⚠ Note: This is an aid, not a medical diagnosis. Consult a professional for clinical decisions.")
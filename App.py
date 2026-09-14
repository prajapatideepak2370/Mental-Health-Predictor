"""
Streamlit Frontend for ML Mental Health Prediction API
--------------------------------------------------------
Connects to a FastAPI backend running at http://127.0.0.1:2200/predict

Run with:
    streamlit run app.py

Make sure your FastAPI backend is running first:
    uvicorn main:app --port 2200 --reload
"""

import time
import requests
import streamlit as st

# --------------------------------------------------------------------------
# CONFIG
# --------------------------------------------------------------------------
API_BASE_URL = "http://127.0.0.1:2200"
PREDICT_ENDPOINT = f"{API_BASE_URL}/predict"

PLATFORMS = [
    "Facebook", "LinkedIn", "Instagram", "Snapchat", "Twitter",
    "YouTube", "TikTok", "LINE", "KakaoTalk", "VKontakte",
    "WhatsApp", "WeChat",
]
PURPOSES = ["Networking", "Education", "Entertainment", "News"]
ACADEMIC_LEVELS = ["Undergraduate", "Graduate", "High School"]
GENDERS = ["Male", "Female"]
STRESS_LEVELS = ["Low", "Medium", "High", "Very High"]

TOP_COUNTRIES = [
    "India", "USA", "Canada", "Australia", "UK", "Germany",
    "Mexico", "Turkey", "France", "Other",
]

# --------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Mental Health Score Predictor",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* Overall background */
        .stApp {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        }

        /* Hide default streamlit chrome */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Title block */
        .main-title {
            text-align: center;
            font-size: 2.6rem;
            font-weight: 800;
            background: linear-gradient(90deg, #7ee8fa 0%, #eec0c6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
        }
        .sub-title {
            text-align: center;
            color: #cfd8e3;
            font-size: 1.05rem;
            margin-top: 0px;
            margin-bottom: 2rem;
        }

        /* Card container for the form */
        .form-card {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(10px);
            border-radius: 18px;
            padding: 1.8rem 2rem 1rem 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
            margin-bottom: 1.5rem;
        }

        .section-header {
            color: #7ee8fa;
            font-size: 1.1rem;
            font-weight: 700;
            margin-top: 0.5rem;
            margin-bottom: 0.7rem;
            border-left: 4px solid #7ee8fa;
            padding-left: 10px;
        }

        /* Inputs */
        .stNumberInput input, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
            border-radius: 10px !important;
        }

        label, .stMarkdown p {
            color: #eaeef2 !important;
        }

        /* Predict button */
        div.stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #7ee8fa 0%, #eec0c6 100%);
            color: #10202b;
            font-weight: 700;
            font-size: 1.1rem;
            padding: 0.7rem 0;
            border-radius: 14px;
            border: none;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            box-shadow: 0 4px 18px rgba(126, 232, 250, 0.35);
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(126, 232, 250, 0.5);
            color: #10202b;
        }

        /* Result Card */
        .result-card {
            background: linear-gradient(135deg, rgba(126,232,250,0.18) 0%, rgba(238,192,198,0.18) 100%);
            border: 1px solid rgba(255,255,255,0.25);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            margin-top: 1.5rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 40px rgba(0,0,0,0.35);
            animation: fadeIn 0.6s ease-in-out;
        }
        .result-score {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(90deg, #7ee8fa 0%, #eec0c6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0.3rem 0;
        }
        .result-label {
            color: #dfe9f0;
            font-size: 1.1rem;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .result-tag {
            display: inline-block;
            margin-top: 0.8rem;
            padding: 0.4rem 1.2rem;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.95rem;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .error-box {
            background: rgba(255, 80, 80, 0.15);
            border: 1px solid rgba(255, 80, 80, 0.4);
            border-radius: 14px;
            padding: 1rem 1.3rem;
            color: #ffd6d6;
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------
st.markdown('<div class="main-title">🧠 Mental Health Score Predictor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">AI-powered insight into student mental well-being, '
    'based on lifestyle and social media habits.</div>',
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# FORM
# --------------------------------------------------------------------------
with st.form("student_form"):

    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    st.markdown('<div class="section-header">👤 Personal Details</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Age", min_value=10, max_value=100, value=20, step=1)
    with c2:
        gender = st.selectbox("Gender", GENDERS)
    with c3:
        country = st.selectbox("Country", TOP_COUNTRIES)

    academic_level = st.selectbox("Academic Level", ACADEMIC_LEVELS)

    st.markdown('<div class="section-header">📱 Social Media Habits</div>', unsafe_allow_html=True)
    c4, c5 = st.columns(2)
    with c4:
        most_used_platform = st.selectbox("Most Used Platform", PLATFORMS)
    with c5:
        purpose_of_use = st.selectbox("Purpose of Use", PURPOSES)

    c6, c7 = st.columns(2)
    with c6:
        avg_daily_usage_hours = st.slider("Avg. Daily Usage (hrs)", 0.0, 24.0, 3.0, 0.1)
    with c7:
        daily_unlocks = st.number_input("Daily Phone Unlocks", min_value=0, value=50, step=1)

    st.markdown('<div class="section-header">🏃 Lifestyle & Well-being</div>', unsafe_allow_html=True)
    c8, c9, c10 = st.columns(3)
    with c8:
        study_hours = st.slider("Study Hours / Day", 0.0, 24.0, 4.0, 0.1)
    with c9:
        physical_activity_hours = st.slider("Physical Activity (hrs)", 0.0, 24.0, 1.0, 0.1)
    with c10:
        sleep_hours_per_night = st.slider("Sleep Hours / Night", 0.0, 24.0, 7.0, 0.1)

    stress_level = st.select_slider("Stress Level", options=STRESS_LEVELS, value="Medium")

    st.markdown("</div>", unsafe_allow_html=True)

    submitted = st.form_submit_button("🔮 Predict Mental Health Score")

# --------------------------------------------------------------------------
# HANDLE SUBMISSION
# --------------------------------------------------------------------------
if submitted:
    payload = {
        "age": int(age),
        "gender": gender,
        "country": country,
        "academic_level": academic_level,
        "most_used_platform": most_used_platform,
        "purpose_of_use": purpose_of_use,
        "avg_daily_usage_hours": float(avg_daily_usage_hours),
        "daily_unlocks": int(daily_unlocks),
        "study_hours": float(study_hours),
        "physical_activity_hours": float(physical_activity_hours),
        "sleep_hours_per_night": float(sleep_hours_per_night),
        "stress_level": stress_level,
    }

    placeholder = st.empty()
    with placeholder.container():
        with st.spinner("Analyzing lifestyle data and predicting mental health score..."):
            try:
                response = requests.post(PREDICT_ENDPOINT, json=payload, timeout=15)
                time.sleep(0.4)  # tiny pause so the loading animation feels smooth
            except requests.exceptions.ConnectionError:
                response = None
                connection_error = True
            else:
                connection_error = False

    placeholder.empty()

    if connection_error:
        st.markdown(
            '<div class="error-box">🚫 <b>Connection Error:</b> Could not reach the FastAPI backend at '
            f'<code>{PREDICT_ENDPOINT}</code>. Make sure it is running '
            '(<code>uvicorn main:app --port 2200 --reload</code>).</div>',
            unsafe_allow_html=True,
        )
    elif response is not None and response.status_code == 200:
        score = response.json().get("predicted_mental_health_score")

        # Simple qualitative tag based on score (assumes 0-10 scale; adjust if needed)
        if score >= 7:
            tag_text, tag_color = "Good 🙂", "#4ade80"
        elif score >= 4:
            tag_text, tag_color = "Moderate 😐", "#facc15"
        else:
            tag_text, tag_color = "Needs Attention ⚠️", "#f87171"

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Predicted Mental Health Score</div>
                <div class="result-score">{score}</div>
                <span class="result-tag" style="background:{tag_color}33; color:{tag_color};
                    border: 1px solid {tag_color};">{tag_text}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        detail = ""
        try:
            detail = response.json()
        except Exception:
            detail = response.text if response is not None else "Unknown error"
        st.markdown(
            f'<div class="error-box">⚠️ <b>Prediction failed</b> (status code '
            f'{response.status_code if response is not None else "N/A"}).<br>{detail}</div>',
            unsafe_allow_html=True,
        )
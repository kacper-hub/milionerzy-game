import streamlit as st
import json
import os
import base64
import random
import time

st.set_page_config(page_title="VETTER - quiz Milionerzy", layout="wide", initial_sidebar_state="collapsed")

def set_background(image_path):
    with open(image_path, "rb") as image_file:
        img_data = base64.b64encode(image_file.read()).decode("utf-8")
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{img_data}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

set_background("pliczek.jpg")

COLORS = {
    "background": "#2c3e50",
    "question": "#ecf0f1",
    "button": "#3498db",
    "correct": "#2ecc71",
    "wrong": "#e74c3c",
    "text": "#ecf0f1",
    "highlight": "#f1c40f",
    "timer": "#e67e22",
    "menu_button": "#9b59b6"
}

ladder = [
    "1. 500 zł", "2. 1 000 zł", "3. 2 000 zł", "4. 5 000 zł", "5. 10 000 zł",
    "6. 20 000 zł", "7. 40 000 zł", "8. 75 000 zł", "9. 125 000 zł", "10. 250 000 zł",
    "11. 500 000 zł", "12. 1 000 000 zł"
]

@st.cache_data
def load_questions():
    all_questions = []
    for i in range(1, 10):
        file_name = f"physics_set{i}.json"
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as f:
                all_questions.extend(json.load(f))
    return all_questions

if "questions" not in st.session_state:
    st.session_state.questions = load_questions()
    random.shuffle(st.session_state.questions)

if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "is_correct" not in st.session_state:
    st.session_state.is_correct = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "used_5050" not in st.session_state:
    st.session_state.used_5050 = False
if "used_phone" not in st.session_state:
    st.session_state.used_phone = False
if "hidden_answers" not in st.session_state:
    st.session_state.hidden_answers = []

def reset_game():
    st.session_state.questions = load_questions()
    random.shuffle(st.session_state.questions)
    st.session_state.current_question = 0
    st.session_state.answered = False
    st.session_state.is_correct = None
    st.session_state.game_over = False
    st.session_state.used_5050 = False
    st.session_state.used_phone = False
    st.session_state.hidden_answers = []

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    if st.session_state.game_over:
        st.markdown("<h1 style='color:red; font-size: 64px;'>❌ KONIEC GRY ❌</h1>", unsafe_allow_html=True)
        time.sleep(3)
        reset_game()
        st.rerun()

    elif st.session_state.current_question < len(st.session_state.questions):
        q_index = st.session_state.current_question
        q = st.session_state.questions[q_index]

        st.markdown(f"<div style='background-color:#1a252f;padding:10px;border-radius:12px;'>"
                    f"<h3 style='color:{COLORS['highlight']};'>Pytanie {q_index + 1}</h3>"
                    f"<h2 style='color:{COLORS['question']};'>{q['pytanie']}</h2></div>",
                    unsafe_allow_html=True)

        # 🆘 Koła ratunkowe
        with st.container():
            st.markdown("<div style='background-color:#1a252f;padding:10px;border-radius:12px;margin-top:10px;'>", unsafe_allow_html=True)
            cols_help = st.columns(2)

            with cols_help[0]:
                if st.button("🧠 Pół na pół", disabled=st.session_state.used_5050):
                    st.session_state.used_5050 = True
                    correct = q["poprawna"]
                    wrongs = [i for i in range(4) if i != correct]
                    remove = random.sample(wrongs, 2)
                    st.session_state.hidden_answers = remove

            with cols_help[1]:
                if st.button("📞 Telefon do przyjaciela", disabled=st.session_state.used_phone):
                    st.session_state.used_phone = True
                    friend_answer = q["odpowiedzi"][q["poprawna"]]
                    st.success(f"Przyjaciel: Hmm... myślę, że to będzie **{friend_answer}**.")

            st.markdown("</div>", unsafe_allow_html=True)

        # Odpowiedzi
        cols = st.columns(2)
        for i, answer in enumerate(q["odpowiedzi"]):
            if i in st.session_state.hidden_answers:
                continue

            with cols[i % 2]:
                style = "font-size: 22px; padding: 12px; margin-bottom: 8px; width: 100%;"

                if not st.session_state.answered:
                    if st.button(answer, key=f"btn_{i}", use_container_width=True):
                        st.session_state.answered = True
                        st.session_state.is_correct = (i == q["poprawna"])

                        if not st.session_state.is_correct:
                            st.session_state.game_over = True
                            st.rerun()
                        else:
                            time.sleep(2)
                            st.session_state.current_question += 1
                            st.session_state.answered = False
                            st.session_state.is_correct = None
                            st.session_state.hidden_answers = []
                            st.rerun()
                else:
                    if i == q["poprawna"]:
                        st.markdown(f"<button style='background-color:{COLORS['correct']}; color:white; {style}' disabled>{answer}</button>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<button style='{style}' disabled>{answer}</button>", unsafe_allow_html=True)

    else:
        st.markdown("<h2 style='color:#f1c40f;'>🎉 Gratulacje! Ukończyłeś quiz.</h2>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<h2 style='color:{COLORS['highlight']};'>💰 Drabinka</h2>", unsafe_allow_html=True)
    for i, level in enumerate(reversed(ladder)):
        idx = len(ladder) - 1 - i
        color = COLORS["highlight"] if idx == st.session_state.current_question else COLORS["text"]
        st.markdown(f"<p style='color:{color}; font-size: 18px;'>{level}</p>", unsafe_allow_html=True)

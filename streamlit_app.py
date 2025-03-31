import streamlit as st
import json
import random
import os
from itertools import cycle
from PIL import Image

# Kolorystyka
COLORS = {
    "background": "#2c3e50",
    "question": "#ecf0f1",
    "button": "#3498db",
    "correct": "#2ecc71",
    "wrong": "#e74c3c",
    "text": "#2c3e50",
    "highlight": "#f1c40f",
    "timer": "#e67e22",
    "menu_button": "#9b59b6"
}

# Lista nagród
nagrody = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000,
           64000, 125000, 250000, 500000, 1000000]

# Ustawienia strony Streamlit
st.set_page_config(page_title="VETTER - quiz Milionerzy", layout="wide", initial_sidebar_state="collapsed")
st.title('VETTER - Milionerzy')

# Sprawdzenie katalogu roboczego
current_dir = os.getcwd()
st.write(f"Aktualny katalog roboczy: {current_dir}")

# Ścieżka do folderu z plikami JSON
json_folder = current_dir  # Jeśli pliki są w tym samym katalogu co skrypt

if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.time_left = 30
    st.session_state.questions = []

# Załaduj pytania z plików JSON
sets = [
    "physics_set1.json", "physics_set2.json", "physics_set3.json", 
    "physics_set4.json", "physics_set5.json", "physics_set6.json", 
    "physics_set7.json", "physics_set8.json", "physics_set9.json"
]
chosen_set = random.choice(sets)
chosen_set_path = os.path.join(json_folder, chosen_set)

try:
    with open(chosen_set_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
        st.session_state.questions = random.sample(all_questions, min(15, len(all_questions)))
except FileNotFoundError:
    st.error(f"Nie znaleziono pliku: {chosen_set_path}")
    st.stop()

if st.button('Rozpocznij Grę'):
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.time_left = 30
    st.experimental_rerun()

if st.session_state.questions:
    current_question = st.session_state.questions[st.session_state.current_question_index]
    st.write(f"### Pytanie {st.session_state.current_question_index + 1}: {current_question['pytanie']}")

    answers = current_question['odpowiedzi']
    random.shuffle(answers)

    for answer in answers:
        if st.button(answer):
            if answer == current_question['odpowiedzi'][current_question['poprawna']]:
                st.session_state.score += 1
                st.write(f'✅ Poprawna odpowiedź! Zdobyte punkty: {nagrody[st.session_state.score - 1]} zł')
            else:
                st.write(f'❌ Zła odpowiedź! Koniec gry.')
                st.write(f'Twój wynik to: {nagrody[max(0, st.session_state.score - 1)]} zł')
                st.stop()

            st.session_state.current_question_index += 1

            if st.session_state.current_question_index >= len(st.session_state.questions):
                st.write(f'🎉 Gratulacje! Wygrałeś {nagrody[-1]} zł!')
                st.stop()

            st.experimental_rerun()

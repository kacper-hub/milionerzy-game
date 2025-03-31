import streamlit as st
st.set_page_config(page_title="VETTER - quiz Milionerzy", layout="wide", initial_sidebar_state="collapsed")

import json
import random
import os
import base64
from itertools import cycle
from PIL import Image

# Funkcja do ustawienia obrazu w tle
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

# Ustawienie obrazu w tle
set_background("pliczek.jpg")

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

# Przykładowe pytanie i odpowiedzi
question = "Który język programowania jest używany do budowy aplikacji webowych w Streamlit?"
answers = ["C++", "Python", "Java", "Ruby"]
correct_answer = "Python"

# Wyświetlenie pytania i odpowiedzi
st.markdown(f"<h2 style='color:{COLORS['question']};'>{question}</h2>", unsafe_allow_html=True)

for answer in answers:
    if st.button(answer):
        if answer == correct_answer:
            st.markdown(f"<p style='color:{COLORS['correct']};'>Dobrze! Odpowiedź '{answer}' jest poprawna.</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color:{COLORS['wrong']};'>Źle! Odpowiedź '{answer}' jest niepoprawna.</p>", unsafe_allow_html=True)

import streamlit as st
import requests

st.title("🚀 InnoFocus: Smart Planner")

user_input = st.text_area("Введи свои задачи (brain dump):", placeholder="Нужно сделать лабу по ОС к пятнице и выучить 20 иероглифов...")

if st.button("Расставить приоритеты"):
    if user_input:
        response = requests.post("http://backend:8000/generate-plan", json={"content": user_input})
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Ошибка связи с ИИ")

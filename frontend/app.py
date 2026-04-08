import streamlit as st
import requests
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")
USER_ID = "streamlit-user"

st.set_page_config(page_title="AI Smart Planner", page_icon="🎯", layout="wide")
st.title("🎯 AI Smart Planner")

def load_tasks():
    try:
        resp = requests.get(f"{API_BASE_URL}/tasks/all?user_id={USER_ID}", timeout=10)
        return resp.json().get("tasks", []) if resp.status_code == 200 else []
    except:
        return []

def render():
    tasks = load_tasks()

    st.header("✨ Parse & Add Tasks")
    txt = st.text_area("Your brain dump:", height=100, placeholder="I need to finish lab by Friday...")

    if st.button("🚀 Parse & Add"):
        if txt.strip():
            with st.spinner("Analyzing..."):
                try:
                    r = requests.post(f"{API_BASE_URL}/tasks/parse", json={"text": txt, "user_id": USER_ID}, timeout=120)
                    if r.status_code == 200:
                        st.success(f"Added {r.json()['total_count']} tasks!")
                    else:
                        st.error(r.json().get("detail", "Error"))
                except Exception as e:
                    st.error(str(e))

    # Sort: active first, then by priority (high→medium→low), then by deadline
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda t: (
        t.get("completed", False),
        priority_order.get(t.get("priority", "medium"), 1),
        t.get("deadline") or "9999-99-99"
    ))

    st.write(f"**You have {len(tasks)} tasks** (sorted by priority):")

    if tasks:
        for t in tasks:
            status = "✅ " if t.get("completed") else ""
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(t.get("priority"), "⚪")
            deadline = f"📅 {t['deadline']}" if t.get("deadline") else ""

            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                line = f"{status}{priority_icon} **{t.get('title', 'Task')}**"
                if deadline:
                    line += f" — {deadline}"
                st.markdown(line)
            with col2:
                if not t.get("completed"):
                    key = f"done_{t['id']}"
                    if st.button("Done", key=key):
                        requests.put(f"{API_BASE_URL}/tasks/{t['id']}/complete")
                        st.rerun()
            with col3:
                key = f"del_{t['id']}"
                if st.button("Delete", key=key):
                    requests.delete(f"{API_BASE_URL}/tasks/{t['id']}")
                    st.rerun()
    else:
        st.info("No tasks. Add some above!")

render()

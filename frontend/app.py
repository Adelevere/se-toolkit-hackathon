import streamlit as st
import requests
import os

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Smart Planner",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Smart Planner")
st.markdown("Transform your brain dump into a structured, prioritized task list using AI")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("This app uses GPT-4 to analyze your text and extract actionable tasks with priorities and subtasks.")
    
    if st.button("Load Sample Tasks"):
        st.session_state.show_sample = True
    
    if st.button("Clear All"):
        st.session_state.show_sample = False
        if 'parsed_tasks' in st.session_state:
            del st.session_state['parsed_tasks']
        st.rerun()

# Main content
tab1, tab2 = st.tabs(["✨ Parse Tasks", "📋 Sample Tasks"])

with tab1:
    st.header("Parse Your Tasks")
    st.markdown("Enter your unstructured thoughts, and AI will organize them into prioritized tasks.")
    
    user_input = st.text_area(
        "Your brain dump:",
        height=200,
        placeholder="Example: I need to finish the lab report by Friday, study for the midterm next week, maybe update my portfolio if I have time, and I should also read that research paper for the seminar on Monday..."
    )
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        parse_button = st.button("🚀 Parse Tasks", type="primary", use_container_width=True)
    
    if parse_button or st.session_state.get('processing', False):
        if not user_input.strip():
            st.error("Please enter some text to parse.")
        else:
            with st.spinner("🤖 AI is analyzing your text..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/tasks/parse",
                        json={"text": user_input, "user_id": "streamlit-user"},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state['parsed_tasks'] = data['tasks']
                        st.success(f"✅ Successfully parsed {data['total_count']} tasks!")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API. Make sure the backend is running.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Display parsed tasks
    if 'parsed_tasks' in st.session_state:
        st.subheader(f"📊 Your Structured Tasks ({len(st.session_state['parsed_tasks'])})")
        
        for idx, task in enumerate(st.session_state['parsed_tasks'], 1):
            priority_color = {
                "high": "🔴",
                "medium": "🟡",
                "low": "🟢"
            }.get(task['priority'], "⚪")
            
            with st.expander(f"{priority_color} **{task['title']}** - Priority: {task['priority'].upper()}", expanded=True):
                if task.get('deadline'):
                    st.caption(f"📅 Deadline: {task['deadline']}")
                
                if task.get('subtasks'):
                    st.markdown("**Subtasks:**")
                    for subtask in task['subtasks']:
                        st.checkbox(subtask['title'], value=subtask.get('completed', False), key=f"task{idx}_{subtask['title']}")

with tab2:
    st.header("Sample Tasks")
    st.markdown("Click the button in the sidebar to load sample tasks for testing.")
    
    if st.session_state.get('show_sample', False):
        with st.spinner("Loading sample tasks..."):
            try:
                response = requests.get(f"{API_BASE_URL}/tasks/mock", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state['parsed_tasks'] = data['tasks']
                    st.success(f"Loaded {data['total_count']} sample tasks!")
                    st.rerun()
                else:
                    st.error("Failed to load sample tasks")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using FastAPI + Streamlit + OpenAI GPT-4")

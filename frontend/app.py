import streamlit as st
import requests
import os

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(
    page_title="InnoFocus - Smart Planner",
    page_icon="🎯",
    layout="wide"
)

# CSS Styles
st.markdown("""
<style>
    .task-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #007bff;
    }
    .priority-High { border-left-color: #dc3545; }
    .priority-Medium { border-left-color: #ffc107; }
    .priority-Low { border-left-color: #28a745; }
    .stat-box {
        background: white;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def get_tasks():
    """Fetch all tasks from backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/tasks", timeout=5)
        if response.status_code == 200:
            return response.json()
        return {"tasks": [], "total": 0}
    except:
        return {"tasks": [], "total": 0}

def get_stats():
    """Fetch task statistics"""
    try:
        response = requests.get(f"{BACKEND_URL}/tasks/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}

def generate_plan(content: str):
    """Generate plan via LLM"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/generate-plan",
            json={"content": content},
            timeout=60
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def create_task(title: str, priority: str):
    """Create a task manually"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/tasks",
            json={"title": title, "priority": priority},
            timeout=5
        )
        return response.status_code == 201 or response.status_code == 200
    except:
        return False

def update_task(task_id: int, updates: dict):
    """Update a task"""
    try:
        response = requests.put(
            f"{BACKEND_URL}/tasks/{task_id}",
            json=updates,
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

def delete_task(task_id: int):
    """Delete a task"""
    try:
        response = requests.delete(f"{BACKEND_URL}/tasks/{task_id}", timeout=5)
        return response.status_code == 200
    except:
        return False

# === UI ===
st.title("🎯 InnoFocus")
st.caption("AI-powered task planner for students")

# Sidebar
with st.sidebar:
    st.header("📊 Statistics")
    stats = get_stats()
    
    if stats:
        st.metric("Total Tasks", stats.get("total", 0))
        st.metric("Completed", stats.get("completed", 0))
        st.metric("In Progress", stats.get("pending", 0))
        
        st.divider()
        st.subheader("By Priority:")
        priority_data = stats.get("by_priority", {})
        st.markdown(f"🔴 **High:** {priority_data.get('High', 0)}")
        st.markdown(f"🟡 **Medium:** {priority_data.get('Medium', 0)}")
        st.markdown(f"🟢 **Low:** {priority_data.get('Low', 0)}")
    
    st.divider()
    if st.button("🔄 Refresh"):
        st.rerun()

# Tabs
tab1, tab2, tab3 = st.tabs(["✨ AI Generator", "📋 My Tasks", "➕ Add Manually"])

# Tab 1: AI Generator
with tab1:
    st.header("✨ AI Plan Generator")
    st.markdown("Describe your tasks in natural language, and AI will structure them and assign priorities.")
    
    user_input = st.text_area(
        "Enter your tasks (brain dump):",
        placeholder="Need to finish OS lab by Friday, learn 20 kanji by Wednesday, prepare database presentation, and call mom...",
        height=150
    )
    
    if st.button("🚀 Generate Plan", type="primary"):
        if user_input.strip():
            with st.spinner("AI is analyzing your tasks..."):
                result = generate_plan(user_input)
                
                if result and result.get("tasks"):
                    st.success(f"✅ Created {result['total']} tasks!")
                    st.session_state["just_generated"] = True
                    st.rerun()
                else:
                    st.error("❌ Generation failed. Check LLM connection.")
        else:
            st.warning("Please enter your tasks")

# Tab 2: Task List
with tab2:
    st.header("📋 Task List")
    
    task_data = get_tasks()
    tasks = task_data.get("tasks", [])
    
    if not tasks:
        st.info("No tasks yet. Generate a plan in the 'AI Generator' tab or add manually.")
    else:
        # Filters
        col1, col2 = st.columns([1, 2])
        with col1:
            filter_priority = st.selectbox(
                "Priority:",
                ["All", "High", "Medium", "Low"]
            )
        with col2:
            filter_status = st.selectbox(
                "Status:",
                ["All", "Active", "Completed"]
            )
        
        # Apply filters
        filtered_tasks = tasks
        if filter_priority != "All":
            filtered_tasks = [t for t in filtered_tasks if t["priority"] == filter_priority]
        if filter_status == "Active":
            filtered_tasks = [t for t in filtered_tasks if not t["is_completed"]]
        elif filter_status == "Completed":
            filtered_tasks = [t for t in filtered_tasks if t["is_completed"]]
        
        st.divider()
        
        # Display tasks
        for task in filtered_tasks:
            priority_icon = {
                "High": "🔴",
                "Medium": "🟡",
                "Low": "🟢"
            }.get(task["priority"], "⚪")
            
            col1, col2, col3, col4 = st.columns([1, 4, 2, 1])
            
            with col1:
                st.markdown(f"**{priority_icon}**")
            
            with col2:
                if task["is_completed"]:
                    st.markdown(f"~~{task['title']}~~")
                else:
                    st.markdown(task["title"])
            
            with col3:
                if not task["is_completed"]:
                    if st.button("✓ Complete", key=f"complete_{task['id']}"):
                        update_task(task["id"], {"is_completed": True})
                        st.rerun()
                else:
                    st.markdown("✅")
            
            with col4:
                if st.button("🗑", key=f"delete_{task['id']}"):
                    delete_task(task["id"])
                    st.rerun()

# Tab 3: Manual Add
with tab3:
    st.header("➕ Add Task Manually")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        task_title = st.text_input("Task Name:", placeholder="What needs to be done?")
    
    with col2:
        task_priority = st.selectbox("Priority:", ["High", "Medium", "Low"])
    
    if st.button("Create Task", type="primary"):
        if task_title.strip():
            success = create_task(task_title.strip(), task_priority)
            if success:
                st.success(f"✅ Task '{task_title}' created!")
                st.rerun()
            else:
                st.error("❌ Failed to create task")
        else:
            st.warning("Please enter a task name")

# Footer
st.divider()
st.caption("InnoFocus v2.0 | AI-powered task planner for students")

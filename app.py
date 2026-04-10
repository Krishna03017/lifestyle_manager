import streamlit as st
from datetime import datetime, date, timedelta
import json
import os

# App configuration
st.set_page_config(page_title="AI Lifestyle Manager", page_icon="🌟")
st.title("🌟 AI Lifestyle Manager")

# Initialize session state
if 'habits' not in st.session_state:
    st.session_state.habits = {}
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'goals' not in st.session_state:
    st.session_state.goals = []
if 'mood_log' not in st.session_state:
    st.session_state.mood_log = []

# Data persistence
DATA_FILE = "lifestyle_data.json"

def save_data():
    data = {
        "habits": st.session_state.habits,
        "tasks": st.session_state.tasks,
        "goals": st.session_state.goals,
        "mood_log": st.session_state.mood_log
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        st.session_state.habits = data.get("habits", {})
        st.session_state.tasks = data.get("tasks", [])
        st.session_state.goals = data.get("goals", [])
        st.session_state.mood_log = data.get("mood_log", [])

load_data()

# Sidebar navigation
menu = st.sidebar.selectbox(
    "Choose a feature:",
    ["Dashboard", "Habit Tracker", "Task Manager", "Goal Setter", "Mood Tracker", "AI Insights"]
)

# Dashboard
if menu == "Dashboard":
    st.header("Your Personal Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Today's Habits")
        completed = sum(1 for h in st.session_state.habits.values() 
                       if h.get(str(date.today()), False))
        total = len(st.session_state.habits)
        st.metric("Completion Rate", f"{completed}/{total}" if total else "0/0")
        
    with col2:
        st.subheader("Pending Tasks")
        pending = len([t for t in st.session_state.tasks if not t['done']])
        st.metric("Tasks to Do", pending)
        
    with col3:
        st.subheader("Active Goals")
        active_goals = len([g for g in st.session_state.goals if not g['achieved']])
        st.metric("Goals in Progress", active_goals)
    
    # Recent mood chart
    if st.session_state.mood_log:
        st.subheader("Recent Mood Trends")
        moods = st.session_state.mood_log[-7:]  # Last 7 entries
        dates = [entry['date'] for entry in moods]
        values = [entry['mood'] for entry in moods]
        st.line_chart(dict(zip(dates, values)))

# Habit Tracker
elif menu == "Habit Tracker":
    st.header(" Habit Tracker")
    
    with st.form("add_habit"):
        new_habit = st.text_input("Add a new habit:")
        submitted = st.form_submit_button("Add Habit")
        if submitted and new_habit:
            st.session_state.habits[new_habit] = {}
            save_data()
            st.success(f"Added habit: {new_habit}")
    
    if st.session_state.habits:
        st.subheader("Track Your Habits")
        for habit in list(st.session_state.habits.keys()):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(habit)
                
            with col2:
                done = st.session_state.habits[habit].get(str(date.today()), False)
                if st.button("✅" if done else "⬜", key=f"toggle_{habit}"):
                    st.session_state.habits[habit][str(date.today())] = not done
                    save_data()
                    st.experimental_rerun()
                    
            with col3:
                if st.button("🗑️", key=f"delete_{habit}"):
                    del st.session_state.habits[habit]
                    save_data()
                    st.experimental_rerun()
    else:
        st.info("No habits added yet. Start by adding one!")

# Task Manager
elif menu == "Task Manager":
    st.header(" Task Manager")
    
    with st.form("add_task"):
        task_desc = st.text_input("New task description:")
        task_priority = st.select_slider("Priority:", options=["Low", "Medium", "High"])
        task_date = st.date_input("Due date:", value=date.today())
        submitted = st.form_submit_button("Add Task")
        
        if submitted and task_desc:
            st.session_state.tasks.append({
                "description": task_desc,
                "priority": task_priority,
                "due_date": str(task_date),
                "done": False
            })
            save_data()
            st.success("Task added!")
    
    if st.session_state.tasks:
        st.subheader("Your Tasks")
        sorted_tasks = sorted(st.session_state.tasks, 
                             key=lambda x: (x['due_date'], x['priority']))
        
        for i, task in enumerate(sorted_tasks):
            col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
            
            with col1:
                done = task['done']
                if st.checkbox("", value=done, key=f"task_{i}"):
                    st.session_state.tasks[i]['done'] = not done
                    save_data()
                    
            with col2:
                due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
                days_left = (due_date - date.today()).days
                color = "red" if days_left < 0 and not done else "orange" if days_left <= 1 else "green"
                st.markdown(f"<span style='color:{color}'>{task['description']}</span>", 
                           unsafe_allow_html=True)
                
            with col3:
                st.write(f"Due: {task['due_date']}")
                
            with col4:
                if st.button("🗑️", key=f"del_task_{i}"):
                    st.session_state.tasks.pop(i)
                    save_data()
                    st.experimental_rerun()
    else:
        st.info("No tasks yet. Add your first task!")

# Goal Setter
elif menu == "Goal Setter":
    st.header(" Goal Setter")
    
    with st.form("add_goal"):
        goal_desc = st.text_input("Goal description:")
        goal_deadline = st.date_input("Target completion date:")
        submitted = st.form_submit_button("Set Goal")
        
        if submitted and goal_desc:
            st.session_state.goals.append({
                "description": goal_desc,
                "deadline": str(goal_deadline),
                "achieved": False
            })
            save_data()
            st.success("Goal added!")
    
    if st.session_state.goals:
        st.subheader("Your Goals")
        for i, goal in enumerate(st.session_state.goals):
            col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
            
            with col1:
                achieved = goal['achieved']
                if st.checkbox("", value=achieved, key=f"goals_{i}"):
                    st.session_state.goals[i]['achieved'] = not achieved
                    save_data()
                    
            with col2:
                st.write(goal['description'])
                
            with col3:
                deadline = datetime.strptime(goal['deadline'], "%Y-%m-%d").date()
                days_left = (deadline - date.today()).days
                status = f"{days_left} days left" if days_left >= 0 else "Overdue"
                st.write(status)
                
            with col4:
                if st.button("🗑️", key=f"del_goal_{i}"):
                    st.session_state.goals.pop(i)
                    save_data()
                    st.experimental_rerun()
    else:
        st.info("No goals set yet. Define your first goal!")

# Mood Tracker
elif menu == "Mood Tracker":
    st.header(" Mood Tracker")
    
    with st.form("mood_entry"):
        mood = st.slider("How are you feeling today?", 1, 10, 5)
        note = st.text_area("Any notes about your day?")
        submitted = st.form_submit_button("Log Mood")
        
        if submitted:
            st.session_state.mood_log.append({
                "date": str(date.today()),
                "mood": mood,
                "note": note
            })
            save_data()
            st.success("Mood logged!")
    
    if st.session_state.mood_log:
        st.subheader("Recent Entries")
        for entry in reversed(st.session_state.mood_log[-5:]):
            st.markdown(f"**{entry['date']}**: Mood {entry['mood']}/10")
            if entry['note']:
                st.write(f"_Note_: {entry['note']}")
            st.progress(entry['mood']/10)
    else:
        st.info("No mood entries yet. Share how you feel!")

# AI Insights
elif menu == "AI Insights":
    st.header("🤖 AI Lifestyle Insights")
    
    # Generate insights based on user data
    insights = []
    
    # Habit insights
    if st.session_state.habits:
        consistent_habits = [h for h, d in st.session_state.habits.items() 
                            if all(d.get(str(date.today() - timedelta(days=i)), False) 
                                  for i in range(7))]
        if consistent_habits:
            insights.append(f"You're consistently maintaining: {', '.join(consistent_habits)}. Keep it up!")
        else:
            insights.append("Try focusing on building consistency in one habit this week.")
    
    # Task insights
    overdue_tasks = [t for t in st.session_state.tasks 
                     if not t['done'] and datetime.strptime(t['due_date'], "%Y-%m-%d").date() < date.today()]
    if overdue_tasks:
        insights.append(f"You have {len(overdue_tasks)} overdue tasks. Prioritize catching up!")
    
    # Mood insights
    if len(st.session_state.mood_log) >= 3:
        recent_moods = [entry['mood'] for entry in st.session_state.mood_log[-3:]]
        avg_mood = sum(recent_moods) / len(recent_moods)
        if avg_mood < 5:
            insights.append("Your recent mood scores are low. Consider taking time for self-care.")
        elif avg_mood > 8:
            insights.append("You've been in a great mood recently! What's contributing to this?")
    
    # Goal insights
    near_deadline_goals = [g for g in st.session_state.goals 
                          if not g['achieved'] and 
                          (datetime.strptime(g['deadline'], "%Y-%m-%d").date() - date.today()).days <= 7]
    if near_deadline_goals:
        insights.append(f"You have {len(near_deadline_goals)} goals with upcoming deadlines. Focus on progress!")
    
    # Display insights
    if insights:
        for insight in insights:
            st.info(insight)
    else:
        st.info("Not enough data yet to generate insights. Keep using the app!")
        
    # General tips
    st.subheader("Daily Tip")
    tips = [
        "Start your day with 5 minutes of deep breathing",
        "Take short breaks every hour to stretch",
        "Write down 3 things you're grateful for each day",
        "Drink at least 8 glasses of water daily",
        "Spend 15 minutes outdoors each day"
    ]
    st.success(tips[date.today().weekday() % len(tips)])

# Footer
st.sidebar.divider()
st.sidebar.info("Your data is saved locally in your browser. It's never uploaded anywhere.")

import streamlit as st

# Initialize session state for todos
if "todo" not in st.session_state:
    st.session_state["todo"] = ""

# Initialize todo states for specific forms
if "todo_use" not in st.session_state:
    st.session_state["todo_use"] = ""
if "todo_form" not in st.session_state:
    st.session_state["todo_form"] = ""

st.json(st.session_state)

def _create_todo(name, Description, due_date):
    return f"{name}-{Description}-{due_date}"

def add_todo_callback(todo_id: str):  # Added todo_id parameter
    name = st.session_state[f"title__form_{todo_id}"]
    Description = st.session_state[f"description__form_{todo_id}"]
    due_date = st.session_state[f"due_date__form_{todo_id}"]
    st.session_state[f"todo_{todo_id}"] = _create_todo(name, Description, due_date)

def todo_edit_form(todo_id: str):
    st.subheader(f"Edit todo {todo_id}")  # Fixed f-string
    with st.form(f"form_{todo_id}", clear_on_submit=False):
        title = st.text_input("Title", key=f"title__form_{todo_id}")
        description = st.text_area("Description", key=f"description__form_{todo_id}")
        due_date = st.date_input("Due Date", key=f"due_date__form_{todo_id}")

        st.form_submit_button(
            "Add todo", 
            on_click=add_todo_callback, 
            args=(todo_id,),
            type="primary"
        )

    st.write(st.session_state[f"todo_{todo_id}"])

todo_edit_form("use")
todo_edit_form("form")

st.json(st.session_state)

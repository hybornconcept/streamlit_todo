import streamlit as st





def _create_todo(name, Description, due_date):
    return f"{name}-{Description}-{due_date}"

def add_todo_callback(todo_id: str):  # Added todo_id parameter
    name = st.session_state[f"title__form_{todo_id}"]
    Description = st.session_state[f"description__form_{todo_id}"]
    due_date = st.session_state[f"due_date__form_{todo_id}"]
    st.session_state[f"todo_{todo_id}"] = _create_todo(name, Description, due_date)

@st.fragment
def todo_edit_form(todo_id: str):
    if f"todo_{todo_id}" not in st.session_state:
        st.session_state[f"todo_{todo_id}"] = ""
    
    with st.container(border=True):
        st.subheader(f"Edit todo {todo_id}")  # Fixed f-string
        with st.form(f"form_{todo_id}", enter_to_submit=False, border=False):
            title = st.text_input("Title", key=f"title__form_{todo_id}")
            description = st.text_area("Description", key=f"description__form_{todo_id}")
            due_date = st.date_input("Due Date", key=f"due_date__form_{todo_id}")

            st.form_submit_button(
                "Edit todo", 
                on_click=add_todo_callback, 
                args=(todo_id,),
                type="primary"
            )

        st.write(st.session_state[f"todo_{todo_id}"])

todo_edit_form("use")
todo_edit_form("form")

st.json(st.session_state)

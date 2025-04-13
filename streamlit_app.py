from dataclasses import dataclass
from datetime import date
from typing import Dict
from typing import Optional

from sqlalchemy import Boolean, Column, Date, Integer, MetaData, String, Table; import sqlalchemy as sa; import streamlit as st
from streamlit.connections import SQLConnection

st.set_page_config(
    page_title="Task Manager Pro",
    page_icon="📝",
    initial_sidebar_state="collapsed",
)

##################################################
### MODELS
##################################################

TABLE_NAME = "tasks"
SESSION_STATE_KEY_TASKS = "tasks_data"


@dataclass
class Task:
    id: Optional[int] = None
    name: str = ""
    notes: Optional[str] = None
    created_date: Optional[date] = None
    deadline: Optional[date] = None
    finished: bool = False

    @classmethod
    def from_row(cls, row):
        if row:
            return cls(**row._mapping)
        return None


@st.cache_resource
def connect_table():
    metadata_obj = MetaData()
    task_table = Table(
        TABLE_NAME,
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("name", String(30)),
        Column("notes", String, nullable=True),
        Column("created_date", Date),
        Column("deadline", Date, nullable=True),
        Column("finished", Boolean, nullable=True),
    )
    return metadata_obj, task_table


##################################################
### DATA INTERACTION
##################################################


def check_table_exists(connection: SQLConnection, table_name: str) -> bool:
    inspector = sa.inspect(connection.engine)
    return inspector.has_table(table_name)


def load_all_tasks(connection: SQLConnection, table: Table) -> Dict[int, Task]:
    """Fetches all tasks from the DB and returns as a dict keyed by id."""
    stmt = sa.select(table).order_by(table.c.id)
    with connection.session as session:
        result = session.execute(stmt)
        tasks = [Task.from_row(row) for row in result.all()]
        return {task.id: task for task in tasks if task}


def load_task(connection: SQLConnection, table: Table, task_id: int) -> Optional[Task]:
    """Fetches a single task by id from the DB."""
    stmt = sa.select(table).where(table.c.id == task_id)
    with connection.session as session:
        result = session.execute(stmt)
        row = result.first()
        return Task.from_row(row)


##################################################
### STREAMLIT CALLBACKS
##################################################


def create_task_callback(connection: SQLConnection, table: Table):
    if not st.session_state.new_task_form__name:
        st.toast("Name empty, not adding task")
        return

    new_task_data = {
        "name": st.session_state.new_task_form__name,
        "notes": st.session_state.new_task_form__notes,
        "created_date": date.today(),
        "deadline": st.session_state.new_task_form__deadline,
        "finished": False,
    }

    stmt = table.insert().values(**new_task_data)
    with connection.session as session:
        session.execute(stmt)
        session.commit()

    st.session_state[SESSION_STATE_KEY_TASKS] = load_all_tasks(conn, task_table)


def open_update_callback(task_id: int):
    st.session_state[f"currently_editing__{task_id}"] = True


def cancel_update_callback(task_id: int):
    st.session_state[f"currently_editing__{task_id}"] = False


def update_task_callback(connection: SQLConnection, table: Table, task_id: int):
    updated_values = {
        "name": st.session_state[f"edit_task_form_{task_id}__name"],
        "notes": st.session_state[f"edit_task_form_{task_id}__notes"],
        "deadline": st.session_state[f"edit_task_form_{task_id}__deadline"],
    }

    if not updated_values["name"]:
        st.toast("Name cannot be empty.", icon="⚠️")
        st.session_state[f"currently_editing__{task_id}"] = True
        return

    stmt = table.update().where(table.c.id == task_id).values(**updated_values)
    with connection.session as session:
        session.execute(stmt)
        session.commit()

    st.session_state[SESSION_STATE_KEY_TASKS][task_id] = load_task(
        connection, table, task_id
    )
    st.session_state[f"currently_editing__{task_id}"] = False


def delete_task_callback(connection: SQLConnection, table: Table, task_id: int):
    stmt = table.delete().where(table.c.id == task_id)
    with connection.session as session:
        session.execute(stmt)
        session.commit()

    st.session_state[SESSION_STATE_KEY_TASKS] = load_all_tasks(conn, task_table)
    st.session_state[f"currently_editing__{task_id}"] = False


def mark_finished_callback(connection: SQLConnection, table: Table, task_id: int):
    current_status = st.session_state[SESSION_STATE_KEY_TASKS][task_id].finished

    stmt = (
        table.update().where(table.c.id == task_id).values(finished=not current_status)
    )
    with connection.session as session:
        session.execute(stmt)
        session.commit()

    st.session_state[SESSION_STATE_KEY_TASKS][task_id] = load_task(
        connection, table, task_id
    )


##################################################
### UI WIDGETS
##################################################


def task_card(connection: SQLConnection, table: Table, task_item: Task):
    task_id = task_item.id

    with st.container(border=True):
        display_name = task_item.name
        display_notes = task_item.notes or ":grey[*No notes*]"
        display_deadline = f":grey[Due {task_item.deadline.strftime('%Y-%m-%d')}]"

        if task_item.finished:
            strikethrough = "~~"
            display_name = f"{strikethrough}{display_name}{strikethrough}"
            display_notes = f"{strikethrough}{display_notes}{strikethrough}"
            display_deadline = f"{strikethrough}{display_deadline}{strikethrough}"

        st.subheader(display_name)
        st.markdown(display_notes)
        st.markdown(display_deadline)

        finish_col, edit_col, delete_col = st.columns(3)
        finish_col.button(
            "Complete" if not task_item.finished else "Reopen",
            icon=":material/check_circle:",
            key=f"display_task_{task_id}__finish",
            on_click=mark_finished_callback,
            args=(conn, task_table, task_id),
            type="secondary" if task_item.finished else "primary",
            use_container_width=True,
        )

        edit_col.button(
            "Edit",
            icon=":material/edit:",
            key=f"display_task_{task_id}__edit",
            on_click=open_update_callback,
            args=(task_id,),
            disabled=task_item.finished,
            use_container_width=True,
        )
        if delete_col.button(
            "Delete",
            icon=":material/delete:",
            key=f"display_task_{task_id}__delete",
            use_container_width=True,
        ):
            delete_task_callback(connection, table, task_id)
            st.rerun(scope="app")


def task_edit_widget(connection: SQLConnection, table: Table, task_item: Task):
    task_id = task_item.id

    with st.form(f"edit_task_form_{task_id}"):
        st.text_input(
            "Name", value=task_item.name, key=f"edit_task_form_{task_id}__name"
        )
        st.text_area(
            "Notes",
            value=task_item.notes,
            key=f"edit_task_form_{task_id}__notes",
        )

        st.date_input(
            "Deadline",
            value=task_item.deadline,
            key=f"edit_task_form_{task_id}__deadline",
        )

        submit_col, cancel_col = st.columns(2)
        submit_col.form_submit_button(
            "Save",
            icon=":material/save:",
            type="primary",
            on_click=update_task_callback,
            args=(connection, table, task_id),
            use_container_width=True,
        )

        cancel_col.form_submit_button(
            "Cancel",
            on_click=cancel_update_callback,
            args=(task_id,),
            use_container_width=True,
        )


@st.fragment
def task_component(connection: SQLConnection, table: Table, task_id: int):
    task_item = st.session_state[SESSION_STATE_KEY_TASKS][task_id]

    currently_editing = st.session_state.get(f"currently_editing__{task_id}", False)

    if not currently_editing:
        task_card(connection, table, task_item)
    else:
        task_edit_widget(connection, table, task_item)


##################################################
### USER INTERFACE
##################################################

st.title("Task Manager Pro")

conn = st.connection("task_db", ttl=5 * 60)
metadata_obj, task_table = connect_table()

with st.sidebar:
    st.header("Admin")
    if st.button(
        "Create table",
        type="secondary",
        help="Creates the 'tasks' table if it doesn't exist.",
    ):
        metadata_obj.create_all(conn.engine)
        st.toast("Task table created successfully!", icon="✅")

    st.divider()
    st.subheader("Session State Debug", help="Is not updated by fragment rerun!")
    st.json(st.session_state)

if not check_table_exists(conn, TABLE_NAME):
    st.warning("Create table from admin sidebar", icon="⚠")
    st.stop()

if SESSION_STATE_KEY_TASKS not in st.session_state:
    with st.spinner("Loading Tasks..."):
        st.session_state[SESSION_STATE_KEY_TASKS] = load_all_tasks(conn, task_table)

current_tasks: Dict[int, Task] = st.session_state.get(SESSION_STATE_KEY_TASKS, {})
for task_id in current_tasks.keys():
    if f"currently_editing__{task_id}" not in st.session_state:
        st.session_state[f"currently_editing__{task_id}"] = False
    task_component(conn, task_table, task_id)

with st.form("new_task_form", clear_on_submit=True):
    st.subheader(":material/add_circle: New Task")
    st.text_input("Name", key="new_task_form__name", placeholder="Enter task name")
    st.text_area(
        "Notes",
        key="new_task_form__notes",
        placeholder="Add task details...",
    )

    date_col, submit_col = st.columns((1, 2), vertical_alignment="bottom")
    date_col.date_input("Deadline", key="new_task_form__deadline")
    submit_col.form_submit_button(
        "Add Task",
        on_click=create_task_callback,
        args=(conn, task_table),
        type="primary",
        use_container_width=True,
    )
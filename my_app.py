import streamlit as st
import time







    



def increment(name:str):
    st.session_state[f'counter_{name}'] += 1

st.title('Hello Datafans')

st.json(st.session_state)
@st.fragment
def display_counter(name:str):
    time.sleep(3)
    key_state = f"counter_{name}"
    if key_state not in st.session_state:
        st.session_state[key_state] =0
    st.subheader(f"Counter {name}")
    # st.button("No click me")
    st.button("click me ++", type ="primary", on_click=increment, key=f"button {name}", args=(name,))

    st.write(f"Counter: {st.session_state[key_state]}")

display_counter("frank")
display_counter("jaja")
display_counter("freed")
import os
import streamlit as st

if "username" not in st.session_state:
    st.session_state["username"] = None


def login_frontend():
    existing_usernames = os.listdir("user_data")

    username = st.text_input("Enter your username to use existing or upload new videos:")
    if st.button("Submit"):
        st.session_state["username"] = username
        if st.session_state["username"] in existing_usernames:
            st.success("Welcome back!")
        else:
            st.warning("New user detected. A new folder will be created for you.")
            os.makedirs(f"user_data/{st.session_state['username']}")

import streamlit as st

st.set_page_config(
    page_title="Generate a Notes Sheet",
    page_icon="🧊",
)

import add_title
add_title.add_logo()

st.title("Generate A Notes Sheet")

if st.session_state.processed_video is not None:
    st.markdown("""#### "You can now generate a notes sheet""")
else:
    st.error("Please go to video processing, and process a video before generating a notes sheet.")
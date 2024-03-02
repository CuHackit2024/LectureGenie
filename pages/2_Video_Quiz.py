import streamlit as st

from quiz_question_handler import QuizQuestion




st.set_page_config(
    page_title="Generate Quiz Questions",
    page_icon="🧊",
)

st.title("Generate Quiz Questions")

if st.session_state.processed_video is not None:
    st.markdown("""#### "You can now generate quiz questions.""")
else:
    st.error("Please go to video processing, and process a video before generating quiz questions.")
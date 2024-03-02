import streamlit as st


st.set_page_config(
    page_title="Generate Quiz Questions",
    page_icon="🧊",
)

st.title("Generate Quiz Questions")

if st.session_state.processed_video is not None:
    st.markdown("""#### "You can now generate flashcards.""")
else:
    st.error("Please go to video processing, and process a video before generating flashcards.")
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64
from st_clickable_images import clickable_images
from PIL import Image
from streamlit import components
import os

st.set_page_config(
    page_title="LectureGenie Home",
    layout="centered",
    page_icon=Image.open("icons/icon_icon.png"),
)

from video_processing.frontend import process_video_frontend
process_video_frontend()




col1, col2, col3 = st.columns(3)

col2.write(r"$\textsf{\Huge LectureGenie}$")

# st.write(r"$\textsf{\normalsize A web application to help you understand and retain information from your study materials}$")

st.write("##### Upload your lecture videos and get interactive quizzes, notes and flashcards")



st.markdown(
    """

    1. **Go to the sidebar** to login and/or upload a video
    2. Once the video has been processed you can:
        - **Go to Video Quiz** for an interactive quiz
        - **Go to Notes Generator** to get detailed notes
        - **Go to Flashcard Generator** to get flashcards
"""
)



# Embed ko-fi
st.markdown(
   "[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/A0A5VDT0M)"
)


st.warning("Uploaded videos are not secure, anyone who knows your username can access your videos."
           " Do not upload sensitive information. Videos will be deleted after 24 hours. This is only a prototype.")

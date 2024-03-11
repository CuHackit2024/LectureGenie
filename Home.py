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


if "username" not in st.session_state:
    st.session_state["username"] = None



col1, col2, col3 = st.columns(3)

col2.write(r"$\textsf{\Huge LectureGenie}$")

# st.write(r"$\textsf{\normalsize A web application to help you understand and retain information from your study materials}$")

st.write("##### Upload your lecture videos and get interactive quizzes, notes and flashcards")

existing_usernames = os.listdir("user_data")

if st.session_state["username"] is None:

    username = st.text_input("Enter your username to access previously processed videos:")
    if st.button("Submit"):
        st.session_state["username"] = username
        if st.session_state["username"] in existing_usernames:
            st.success("Welcome back!")
        else:
            st.warning("New user detected. A new folder will be created for you.")
            os.makedirs(f"user_data/{st.session_state['username']}")


st.markdown(
    """

    1. **Go to Video Processing** to upload your video
    2. Once the video has been processed you can:
        - **Go to Video Quiz** for an interactive quiz
        - **Go to Notes Generator** to get detailed notes
        - **Go to Flashcard Generator** to get flashcards
"""
)



#col4.image('Video_Processing.jpg', use_column_width=True, caption='Video Processing')


images = []
for file in ["icons/Video_Processing.png", "icons/Video_Quiz.png", "icons/Notes_Generator.png", "icons/Flashcard_Generator.png"]:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        images.append(f"data:image/jpeg;base64,{encoded}")


# Embed ko-fi
st.markdown(
   "[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/A0A5VDT0M)"
)

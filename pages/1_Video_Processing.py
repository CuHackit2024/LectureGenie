import streamlit as st

if "video_processing_stage" not in st.session_state:
    st.session_state["video_processing_stage"] = "upload_video"

if "processed_video" not in st.session_state:
    st.session_state["processed_video"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None

# import the backend code for the video processing
from PIL import Image

import time

from video_processing import frontend

st.set_page_config(
    page_title="Video Processing",
    page_icon=Image.open("icons/icon_icon.png"),
)

import add_title
add_title.add_logo()

# Streamlit UI
st.title("Video Processing")

status = st.empty()

if st.session_state["username"] is None:
    st.warning("You need to be logged in to access this page")
else:
    frontend.process_video_frontend()



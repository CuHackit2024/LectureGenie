import streamlit as st
from .upload_video_frontend import upload_video_frontend
from .transcribe_video_frontend import transcribe_video_frontend
from .keyframe_processing_frontend import keyframe_processing_frontend
from .login_frontend import login_frontend

if "video_processing_stage" not in st.session_state:
    st.session_state["video_processing_stage"] = "upload_video"
if "processed_video" not in st.session_state:
    st.session_state["processed_video"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None

def start_over():
    st.session_state["video_processing_stage"] = "upload_video"
    st.session_state["processed_video"] = None


def process_video_frontend():
    # Container for the video processing frontend
    video_processing_container = st.sidebar.container()
    with video_processing_container:
        login_frontend()

        if st.session_state["video_processing_stage"] == "upload_video" and st.session_state["username"] is not None:
            upload_video_frontend()

        if st.session_state["video_processing_stage"] == "transcribe_video":
            transcribe_video_frontend()

        if st.session_state["video_processing_stage"] == "keyframe_processing":
            keyframe_processing_frontend()

        if st.session_state["video_processing_stage"] == "finished":
            processed_video = st.session_state["processed_video"]
            # Save the json
            video_name = processed_video.video_name
            processed_video.save_to_json(f"user_data/{st.session_state['username']}/{video_name}/processed.json")
            st.success(f"Video processed and loaded! {video_name} is ready to go!")

            st.button("Start Over", on_click=start_over)

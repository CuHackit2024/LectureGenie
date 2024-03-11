import streamlit as st
from .upload_video_frontend import upload_video_frontend
from .transcribe_video_frontend import transcribe_video_frontend
from .keyframe_processing_frontend import keyframe_processing_frontend


def process_video_frontend():
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
        st.success(f"Video processing complete")
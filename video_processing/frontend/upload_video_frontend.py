import streamlit as st
import os
from video_processing.processed_video import ProcessedVideo


def upload_video_frontend():
    users_path = f"user_data/{st.session_state['username']}"
    st.markdown("#### Select a lecture video")
    st.markdown("Choose an already processed video **OR** upload a new video to process")
    if st.session_state["username"] is not None:
        available_folders = os.listdir(users_path)
        selected_folder = st.selectbox("Select a folder to load an already processed video", available_folders)
        if len(available_folders) > 0 and st.button("Load processed video"):
            # Load the processed video
            processed_video = ProcessedVideo()
            processed_video.load_from_json(f"{users_path}/{selected_folder}/processed.json")
            processed_video.path_to_video = f"{users_path}/{selected_folder}/processed.mp4"
            processed_video.video_name = selected_folder
            st.session_state["processed_video"] = processed_video
            st.session_state[
                "processed_video"].path_to_video = f"{users_path}/{selected_folder}/processed.mp4"
            st.success("Processed video loaded")
            st.session_state["video_processing_stage"] = "finished"
    else:
        st.warning("You need to be logged in to load a processed video")

    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov"])

    if uploaded_file is not None:
        # Create a folder using the name of the video
        video_name = uploaded_file.name.split(".")[0]
        os.makedirs(f"{users_path}/{video_name}", exist_ok=True)

        st.session_state["processed_video"] = ProcessedVideo()
        st.session_state[
            "processed_video"].path_to_video = f"{users_path}/{video_name}/processed.mp4"
        st.session_state["processed_video"].video_name = video_name

        # If the video name folder doesn't exist, create it
        if not os.path.exists(f"{users_path}/{video_name}"):
            os.makedirs(f"{users_path}/{video_name}")

        with open(st.session_state["processed_video"].path_to_video, "wb") as file:
            file.write(uploaded_file.getvalue())

        st.session_state["video_processing_stage"] = "transcribe_video"

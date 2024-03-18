import streamlit as st
from video_processing.backend.keyframe import get_descriptions, timed_frames
import os
import PIL


def keyframe_processing_frontend():
    """
    Processing video for keyframes
    """
    status = st.empty()
    key_frame_times = []
    for t in st.session_state.processed_video.segments:
        key_frame_times.append((t.start + t.end) / 2)

    # Get the keyframes from the video
    status.status(f"Getting {len(key_frame_times)} keyframes from the video...")

    frames = timed_frames(st.session_state.processed_video.path_to_video, timestamps=key_frame_times)

    # Saving the keyframes as images in the folder
    # Creating a folder for the keyframes
    # Example path to vide: user_data/Ethan/1000000713/processed.mp4
    keyframe_folder = st.session_state.processed_video.path_to_video.split("/")
    keyframe_folder = "/".join(keyframe_folder[:-1]) + "/keyframes"
    os.makedirs(keyframe_folder, exist_ok=True)

    for i, frame in enumerate(frames): # frames is a list of tuples (timestamp, ndarray)
        PIL.Image.fromarray(frame[1]).save(f"{keyframe_folder}/frame_{i}.jpg")


    status.success("Keyframes extracted")
    status.status("Generating descriptions for keyframes...")
    # loading progress.txt to get the current progress
    descriptions = get_descriptions([f[1] for f in frames])

    if descriptions is None:
        st.error("Failed to generate descriptions for keyframes (Check FD service is running)")
        return

    status.success("Descriptions generated")
    st.session_state["processed_video"].add_descriptions(descriptions)
    st.session_state["video_processing_stage"] = "finished"

import streamlit as st
from video_processing.backend.keyframe import get_descriptions, timed_frames

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
    status.success("Keyframes extracted")
    status.status("Generating descriptions for keyframes...")
    # loading progress.txt to get the current progress
    print(f"frames: {len(frames)}")
    descriptions = get_descriptions([f[1] for f in frames])

    if descriptions is None:
        st.error("Failed to generate descriptions for keyframes, have to run description script")

    status.success("Descriptions generated")
    st.session_state["processed_video"].add_descriptions(descriptions)
    st.session_state["video_processing_stage"] = "finished"
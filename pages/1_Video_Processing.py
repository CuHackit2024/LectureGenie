import streamlit as st

if "video_processing_stage" not in st.session_state:
    st.session_state["video_processing_stage"] = "upload_video"

if "processed_video" not in st.session_state:
    st.session_state["processed_video"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None

# import the backend code for the video processing
from PIL import Image
import cv2
import os
import time
import random

from video_processing.transcript.whisper_transcription import transcribe
from video_processing.keyframe.descriptor import get_descriptions
from video_processing.keyframe.graber import timed_frames
from video_processing.processed_video import ProcessedVideo

st.set_page_config(
    page_title="Video Processing",
    page_icon=Image.open("icons/icon_icon.png"),
)


def update_progress():
    while True:
        with open("progress.txt", "r") as file:
            progress = file.read().strip()
            progress = float(progress)
        status.status(f"Generating descriptions for keyframes... {progress}/{len(frames)}")
        time.sleep(1)  # Sleep for 1 second


import add_title

add_title.add_logo()

# Streamlit UI
st.title("Video Processing")

status = st.empty()

if st.session_state["username"] is None:
    st.warning("You need to be logged in to access this page")

if st.session_state["video_processing_stage"] == "upload_video" and st.session_state["username"] is not None:
    st.markdown("#### Upload Lecture Video")
    st.write("Choose an already processed video to load")
    if st.session_state["username"] is not None:
        available_folders = os.listdir(f"user_data/{st.session_state['username']}")
        selected_folder = st.selectbox("Select a folder to load an already processed video", available_folders)
        if len(available_folders) > 0 and st.button("Load processed video"):
            # Load the processed video
            processed_video = ProcessedVideo()
            processed_video.load_from_json(f"data/{selected_folder}/processed.json")
            st.session_state["processed_video"] = processed_video
            st.session_state[
                "processed_video"].path_to_video = f"user_data/{st.session_state['username']}/{selected_folder}/processed.mp4"
            st.success("Processed video loaded")
            st.session_state["video_processing_stage"] = "finished"
    else:
        st.warning("You need to be logged in to load a processed video")

    uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])

    if uploaded_file is not None:
        # Create a folder using the name of the video
        video_name = uploaded_file.name.split(".")[0]
        os.makedirs(f"user_data/{video_name}", exist_ok=True)

        st.session_state["processed_video"] = ProcessedVideo()
        st.session_state[
            "processed_video"].path_to_video = f"user_data/{st.session_state['username']}/{video_name}/processed.mp4"

        # If the video name folder doesn't exist, create it
        if not os.path.exists(f"user_data/{st.session_state['username']}/{video_name}"):
            os.makedirs(f"user_data/{st.session_state['username']}/{video_name}")

        with open(st.session_state["processed_video"].path_to_video, "wb") as file:
            file.write(uploaded_file.getvalue())

        st.session_state["video_processing_stage"] = "transcribe_video"

if st.session_state["video_processing_stage"] == "transcribe_video":
    """
    Waiting for the transcription to complete
    """
    # blocking call to wait for the transcription to complete
    status.status("Waiting for transcription to complete...")
    transcription_segments = []
    for update in transcribe(st.session_state["processed_video"].path_to_video):
        if isinstance(update, list):
            transcription_segments = update
            break
        status.progress(update.progress, str(update))

    st.session_state["processed_video"].segments = transcription_segments

    # If there are less than 2 segs
    if len(st.session_state["processed_video"].segments) < 2:
        st.warning("This video doesn't have a lot of content to transcribe."
                   "Relying on video content entirely.")

        # Replacing it with 10 evenly spaced timestamps
        # Get the length of the video in second using opencv
        cap = cv2.VideoCapture(st.session_state["processed_video"].path_to_video)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        timestamps = [i / fps for i in range(0, total_frames, total_frames // 10)]
        st.session_state["processed_video"].segments = []
        # The end time is the start time of the next seg
        for i in range(len(timestamps) - 1):
            st.session_state["processed_video"].segments.append({
                "start_time": timestamps[i],
                "end_time": timestamps[i + 1],
                "transcript": "N/A"
            })

        if len(st.session_state['processed_video'].segments) > 16:
            st.session_state['processed_video'].reduce_seg_count(16)

        st.session_state["video_processing_stage"] = "keyframe_processing"
    else:
        if len(st.session_state['processed_video'].segments) > 16:
            st.session_state['processed_video'].reduce_seg_count(16)
        st.session_state["video_processing_stage"] = "keyframe_processing"


if st.session_state["video_processing_stage"] == "keyframe_processing":

    """
    Processing video for keyframes
    """

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

    status = st.success("Descriptions generated")
    st.session_state["processed_video"].add_descriptions(descriptions)
    st.session_state["video_processing_stage"] = "finished"

if st.session_state["video_processing_stage"] == "finished":
    processed_video = st.session_state["processed_video"]
    # Save the json
    processed_video.save_to_json(f"user_data/{st.session_state['username']}/{video_name}/processed.json")


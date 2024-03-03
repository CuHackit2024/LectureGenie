import streamlit as st
import os 
from PIL import Image

# Setup session state variables
if "processed" not in st.session_state:
    st.session_state["processed"] = False
if "transcription_started" not in st.session_state:
    st.session_state["transcription_started"] = False
if "transcribed" not in st.session_state:
    st.session_state["transcribed"] = False
if "job_name" not in st.session_state:
    st.session_state["job_name"] = ""
if "processed_video" not in st.session_state:
    st.session_state["processed_video"] = None
if "video_path" not in st.session_state:
    st.session_state["video_path"] = None
if "transcription_response" not in st.session_state:
    st.session_state["transcription_response"] = None

#import the backend code for the video processing
import json
from PIL import Image
import cv2
import os
import time

from video_processing.transcript.video_transcriber import VideoTranscriber
from video_processing.keyframe.descriptor import get_descriptions
from video_processing.keyframe.graber import timed_frames
from processed_video import ProcessedVideo


st.set_page_config(
    page_title="Video Processing",
page_icon=Image.open("icon_icon.png"),
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

transcriber = VideoTranscriber(region="us-west-2", s3_bucket="transcibe-cuhackit", job_name_prefix="TRANSCRIBE")



# Streamlit UI
st.title("Video Processing")
st.markdown("#### Upload Lecture Video")

# Reset button
if st.button("Reset"):
    st.session_state["processed"] = False
    st.session_state["transcription_started"] = False
    st.session_state["transcribed"] = False
    st.session_state["job_name"] = ""
    st.session_state["processed_video"] = None

if st.button("activate skip"):
    st.session_state["processed"] = False
    st.session_state["transcribed"] = True
    st.session_state["transcription_response"] = json.load(open("data/data_science_full.json", "r"))
    st.session_state["transcription_response"] = st.session_state["transcription_response"]["segments"]


# Checking their are directories inside of data/
available_folders = []
if os.path.exists("data"):
    available_folders = [f for f in os.listdir("data") if os.path.isdir(f"data/{f}")]
    # Provide a dropdown to select the folder
    selected_folder = st.selectbox("Select a folder to load a processed video", available_folders)
    if st.button("Load processed video"):
        # Load the processed video
        processed_video = ProcessedVideo()
        processed_video.load_from_json(f"data/{selected_folder}/processed.json")
        st.session_state["processed_video"] = processed_video
        st.session_state["processed_video"].path_to_video = f"data/{selected_folder}/processed.mp4"
        st.success("Processed video loaded")




uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "wmv", "flv", "mkv", "webm"])

status = st.empty()

print("uploaded_file", uploaded_file)

# # When a new file is uploaded, reset the session state variables
# if uploaded_file is not None:
#     st.session_state["processed"] = False
#     st.session_state["transcription_started"] = True
#     st.session_state["transcribed"] = True
#     st.session_state["job_name"] = ""


# Process and upload video
if uploaded_file is not None and not st.session_state["transcription_started"] and st.button("Process and Upload Video"):
    with st.spinner('Uploading video to transcribe...'):

        """
        Transcribing the video
        """
        # Assuming direct upload without any processing
        s3_file_name = f"processed_videos/{uploaded_file.name}"
        
        # Upload the video to S3 directly from the uploaded file
        transcriber.upload_video_to_s3(uploaded_file, s3_file_name)
        st.status("Video uploaded to S3")
        # Start the transcription job
        job_name = transcriber.start_transcription_job(s3_file_name)
        st.status("Transcription job started")
        st.session_state["job_name"] = job_name
        st.session_state["transcription_started"] = True

if st.session_state["transcription_started"] and not st.session_state["transcribed"]:
    with st.spinner("Waiting for transcription to complete..."):
        """
        Waiting for the transcription to complete
        """
        # blocking call to wait for the transcription to complete
        st.session_state.transcription_response = transcriber.get_transcription_times(st.session_state["job_name"])
        if st.session_state.transcription_response:
            st.status("Transcription complete")
            st.session_state["transcribed"] = True

if st.session_state["transcribed"] and not st.session_state["processed"]:

    """
    Processing video for keyframes
    """

    start_times = []
    for t in st.session_state.transcription_response:
        start_times.append(float(t["start_time"]))

    # Save the video to a temp folder
    video_name = uploaded_file.name
    path = f"vids/{video_name}"
    os.makedirs("vids", exist_ok=True)
    with open(path, "wb") as file:
        file.write(uploaded_file.getvalue())

    # Get the keyframes from the video
    status.status(f"Getting {len(start_times)} keyframes from the video...")
    frames = timed_frames(path, timestamps=start_times)
    status.success("Keyframes extracted")
    status.status("Generating descriptions for keyframes...")
    # loading progress.txt to get the current progress
    print(f"frames: {len(frames)}")
    descriptions = get_descriptions([f[1] for f in frames])
    
    if descriptions is None:
        st.error("Failed to generate descriptions for keyframes, have to run description script")

        
    status.success("Descriptions generated")
    st.session_state["processed"] = True

    # Creating the processed video
    processed_video = ProcessedVideo()
    processed_video.create(st.session_state.transcription_response, descriptions)
    st.session_state["processed_video"] = processed_video

if st.session_state["processed"] and st.session_state["processed_video"] is not None:
    processed_video = st.session_state["processed_video"]
    # Ask for a save name
    save_name = st.text_input("Save the processed video as (no extension)")
    confirm_save = st.button("Save")
    if confirm_save:
        save_folder_path = f"data/{save_name}"
        os.makedirs(save_folder_path, exist_ok=True)
        json_save_path = save_folder_path + "/processed.json"

        processed_video.save_to_json(json_save_path)

        # Also sav the vid there
        save_path = save_folder_path + "/processed.mp4"
        with open(save_path, "wb") as file:
            file.write(uploaded_file.getvalue())
        st.success(f"Processed video saved as {save_path}")

else:
    st.warning("No processed video to save -> " + str(st.session_state["processed_video"]) + " " + str(st.session_state["processed"]))


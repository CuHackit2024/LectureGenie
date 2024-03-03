import streamlit as st
from io import BytesIO
#import the backend code for the video processing
import os


from video_processor import VideoTranscriber


transcriber = VideoTranscriber(region="us-west-2", s3_bucket="transcibe-cuhackit", job_name_prefix="TRANSCRIBE")

# if "processed" not in st.session_state:
#     st.session_state["processed"] = None
# if "processed_video" not in st.session_state:
#     st.session_state["processed_video"] = None
# if "video" not in st.session_state:
#     st.session_state["video"] = None
import add_title
st.set_page_config(
    page_title="Video Processing",
    page_icon="🧊",
)
add_title.add_logo()

# st.title("Video Processing")

# st.markdown("#### Upload your lecture video/slides to the application for processing by selecting the file below")

# uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "wmv", "flv", "mkv", "webm"])

# st.session_state['video'] = uploaded_file

# if st.session_state['video'] is not None:
#     if st.button("Process Video"):
#         if st.session_state['video'] is not None:
#             #process the video, making sure to display a progress bar for the user
#             #st.session_state['processed_video'] = process_video(st.session_state['video'])
#             st.session_state['processed'] = True
#             pass
#         else:
#             st.error("Please upload a video file")

# st.markdown("#### (Optional) Save the processed video to your device for future use, or just use"
#             " your processed video in this session")

# if st.session_state['processed']:
#     filename = st.text_input("Enter file name to save predicted data")
#     #username = st.session_state["username"]
#     if st.button("Save Processed Video"):
#         if not os.path.exists("data"):
#             os.makedirs("data")
#             # os.makedirs(f"""predicted/{username}""")
#         # file_path = f"predicted/{username}/{filename}.csv"
#         file_path = f"data/{filename}.csv"
#         st.session_state.output.to_csv(file_path, index=False)
#         st.session_state.processed = False
#         st.success("Processed video saved")


# Setup session state variables
if "processed" not in st.session_state:
    st.session_state["processed"] = False
if "job_name" not in st.session_state:
    st.session_state["job_name"] = ""

# Streamlit UI
st.set_page_config(page_title="Video Processing", page_icon="🧊")
st.title("Video Processing")
st.markdown("#### Upload your lecture video/slides to the application for processing by selecting the file below")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "wmv", "flv", "mkv", "webm"])

# Process and upload video
if uploaded_file is not None and st.button("Process and Upload Video"):
    with st.spinner('Processing video...'):
        # Assuming direct upload without any processing
        s3_file_name = f"processed_videos/{uploaded_file.name}"
        
        # Upload the video to S3 directly from the uploaded file
        transcriber.upload_video_to_s3(uploaded_file, s3_file_name)
        
        # Start the transcription job
        job_name = transcriber.start_transcription_job(s3_file_name)
        st.session_state["job_name"] = job_name
        st.session_state["processed"] = True
        st.success(f"Video uploaded and transcription job started with name: {job_name}")

# Check Transcription Status
if st.session_state["processed"] and st.button("Check Transcription Status"):
    if st.session_state["job_name"]:
        with st.spinner('Checking transcription status...'):
            times = transcriber.get_transcription_times(st.session_state["job_name"])
            if times:
                st.write("Transcription Times:", times)
            else:
                st.write("Transcription still in progress or failed.")
    else:
        st.error("No transcription job to check.")
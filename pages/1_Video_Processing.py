import streamlit as st
#import the backend code for the video processing
import os

if "processed" not in st.session_state:
    st.session_state["processed"] = None
if "processed_video" not in st.session_state:
    st.session_state["processed_video"] = None
if "video" not in st.session_state:
    st.session_state["video"] = None

st.set_page_config(
    page_title="Video Processing",
    page_icon="🧊",
)

st.title("Video Processing")

st.markdown("#### Upload your lecture video/slides to the application for processing by selecting the file below")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "wmv", "flv", "mkv", "webm"])

st.session_state['video'] = uploaded_file

if st.session_state['video'] is not None:
    if st.button("Process Video"):
        if st.session_state['video'] is not None:
            #process the video, making sure to display a progress bar for the user
            #st.session_state['processed_video'] = process_video(st.session_state['video'])
            st.session_state['processed'] = True
            pass
        else:
            st.error("Please upload a video file")

st.markdown("#### (Optional) Save the processed video to your device for future use, or just use"
            " your processed video in this session")

if st.session_state['processed']:
    filename = st.text_input("Enter file name to save predicted data")
    #username = st.session_state["username"]
    if st.button("Save Processed Video"):
        if not os.path.exists("data"):
            os.makedirs("data")
            # os.makedirs(f"""predicted/{username}""")
        # file_path = f"predicted/{username}/{filename}.csv"
        file_path = f"data/{filename}.csv"
        st.session_state.output.to_csv(file_path, index=False)
        st.session_state.processed = False
        st.success("Processed video saved")

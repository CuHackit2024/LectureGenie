import streamlit as st
import video_playback
import os
import datetime




st.set_page_config(
    page_title="Interactive Video",
    page_icon="🧊",
)

import add_title
add_title.add_logo()

st.title("Interactive Video")
#
# if st.session_state.processed_video is not None:
#     st.markdown("""#### "You can now generate quiz questions.""")
# else:
#     st.error("Please go to video processing, and process a video before generating quiz questions.")

st.session_state.start_time = None
st.session_state.end_time = None

top_cols = st.columns(2)

# # video_file = open("sample_video/data_science.mp4", "rb")
# video_playback.play_video_with_tracking(video_path)
video_length_seconds = 46.0
with top_cols[0]:
    st.video(video_path)

with top_cols[1]:
    side_cols = st.columns(2)
    with side_cols[0]:
        start_time = st.slider("Start time", 0.0, video_length_seconds, st.session_state.start_time, .5)
    with side_cols[1]:
        end_time = st.slider("End time", 0.0, video_length_seconds, st.session_state.end_time, .5)
    side_cols_2 = st.columns(2)
    with side_cols_2[0]:
        if st.button('Generate'):
            if start_time >= end_time:
                st.error("Start time must be less than end time")
            else:
                st.session_state.start_time = start_time
                st.session_state.end_time = end_time
    with side_cols_2[1]:
        if st.session_state.start_time is not None and st.session_state.end_time is not None:
            st.markdown(f"{st.session_state.start_time} - {st.session_state.end_time}")




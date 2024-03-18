import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import toml
from functionalities import flashcard_calls
from PIL import Image

st.set_page_config(
    page_title="View Transcript",
    page_icon=Image.open("icons/icon_icon.png"),
)

from video_processing.frontend import process_video_frontend

import add_title

add_title.add_logo()

process_video_frontend()

# Checking if the st.session_state.processed_video exists
if "processed_video" not in st.session_state or st.session_state.processed_video is None:
    st.error("A video must be loaded before you can view the transcript.")
    st.stop()


def make_dataframe():
    # Creating a dataframe of the transcript by loading in the segs
    headers = ["Start time", "End time", "Transcript", "Frame Description"]
    contents = []
    for seg in st.session_state.processed_video.segments:
        contents.append([round(seg.start, 1), round(seg.end, 1), seg.text, seg.frame_description])
    return pd.DataFrame(contents, columns=headers)


st.title("Transcript")
st.table(make_dataframe())
st.markdown("Download the transcript as a CSV file.")
st.download_button(label="Download Transcript as a CSV File",
                   data=make_dataframe().to_csv().encode('utf-8'),
                   file_name=f"{st.session_state.processed_video.video_name}_transcript.csv",
                   mime="text/csv")

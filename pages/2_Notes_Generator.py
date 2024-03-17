import streamlit as st
import random
from PIL import Image
import google.generativeai as genai
import toml

st.set_page_config(
    page_title="Generate a Notes Sheet",
    page_icon=Image.open("icons/icon_icon.png"),
)

import add_title
add_title.add_logo()

if "notes" not in st.session_state:
    st.session_state.notes = None

from video_processing.frontend import process_video_frontend

process_video_frontend()


def start_over():
    st.session_state.notes = None


status = st.empty()

if "processed_video" not in st.session_state or not st.session_state["processed_video"]:
    st.error("Please load a video before generating notes.")
    st.stop()

if st.session_state.notes is None:
    if st.button('Generate Notes'):
        status.status("Processing video...")

        entire_video_as_string = ""
        for seg in st.session_state["processed_video"].segments:
            entire_video_as_string += f"""From {int(seg.start)} to {int(seg.end)} seconds, this was said: "{seg.text}" """
            entire_video_as_string += "On the screen was: " + seg.frame_description + "\n\n"

        status.status("Generating notes... (this may take a while)")
        prompt = "Create a notes sheet based on the following information: \n\n" + entire_video_as_string
        api_keys = toml.load("keys.toml")['gemini']['keys']
        genai.configure(api_key=random.choice(api_keys))
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt])
        st.session_state.notes = response.text
        status.success("Notes generated!")

if st.session_state.notes is not None:
    st.markdown(st.session_state.notes)
    video_name = st.session_state["processed_video"].video_name
    st.download_button(label="Download Notes as a TXT File (human-readable)",
                       data=st.session_state.notes.encode('utf-8'),
                       file_name=f"{video_name}_notes.txt",
                       mime="text/plain")

    st.button("Reset Note Generator", on_click=start_over)

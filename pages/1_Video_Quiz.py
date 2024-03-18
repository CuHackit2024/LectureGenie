import streamlit as st
import datetime
from functionalities.quiz_questions import quiz_generator
from functionalities.quiz_questions import quiz_frontend
from PIL import Image



st.set_page_config(
    page_title="Interactive Video",
    page_icon=Image.open("icons/icon_icon.png"),
)

if "video_path" not in st.session_state:
    st.session_state["video_path"] = None
if "processed_video" not in st.session_state:
    st.session_state["processed_video"] = None

# if st.button("Use Demo Video"):
#     st.session_state.video_path = "sample_video/data_science.mp4"
#     st.session_state.processed_video = ProcessedVideo()
#     st.session_state.processed_video.load_from_json("data/data_science_full.json")




from video_processing.frontend import process_video_frontend
process_video_frontend()

import add_title
add_title.add_logo()

st.title("Interactive Video")

if st.session_state.processed_video is None:
    st.error("Please load a video before generating a quiz.")
    st.stop()
if "question_element" not in st.session_state:
    st.session_state.question_element = None
if "start_time" not in st.session_state:
    st.session_state.start_time = 0

top_cols = st.columns([.75, .25])


with top_cols[0]:
    loaded_video = open(st.session_state.processed_video.path_to_video, "rb").read()
    with st.container(border=True):
        st.video(loaded_video)

with top_cols[1]:
    start_time_str = st.text_input("Question Time", "00:00")
    try:
        start_time_dt = datetime.datetime.strptime(start_time_str, "%M:%S")
    except ValueError:
        st.error("Invalid time format. Please use mm\:ss")
        st.stop()

    start_time = start_time_dt.minute * 60 + start_time_dt.second
    sub_cols = st.columns(2)
    question_type = st.selectbox("Question Type", ["Multiple Choice", "True/False"])

    if st.button("Generate Question"):
        my_maker = quiz_generator.QuizQuestionMaker(start_time, start_time, st.session_state.processed_video)
        try:
            question = my_maker.get_question(question_type)
        except ValueError as e:
            st.error(str(e) + " Please try a different time or try again.")
            st.stop()
        # Show the quiz question
        st.session_state.question_element = quiz_frontend.QuizQuestion(question["question"], question["answer"], question["options"], question["question_type"], question["explanation"])
if st.session_state.question_element is not None:
    st.session_state.question_element.handle()





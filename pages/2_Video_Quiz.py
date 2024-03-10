import streamlit as st
import datetime
from video_processing.processed_video import ProcessedVideo
from quiz_questions import quiz_generator
from quiz_questions import quiz_frontend
from PIL import Image



st.set_page_config(
    page_title="Interactive Video",
page_icon=Image.open("icon_icon.png"),
)

if "video_path" not in st.session_state:
    st.session_state["video_path"] = None
if "processed_video" not in st.session_state:
    st.session_state["processed_video"] = None

if st.button("Use Demo Video"):
    st.session_state.video_path = "sample_video/data_science.mp4"
    st.session_state.processed_video = ProcessedVideo()
    st.session_state.processed_video.load_from_json("data/data_science_full.json")


import add_title
add_title.add_logo()

st.title("Interactive Video")
#
# if st.session_state.processed_video is not None:
#     st.markdown("""#### "You can now generate quiz questions.""")
# else:
#     st.error("Please go to video processing, and process a video before generating quiz questions.")

try:
    if st.session_state.processed_video.path_to_video is None:
        st.error("Please upload a video at the Video Processing page.")
except AttributeError:
    st.error("Please upload a video at the Video Processing page.")
if "question_element" not in st.session_state:
    st.session_state.question_element = None
if "start_time" not in st.session_state:
    st.session_state.start_time = 0

top_cols = st.columns([.75, .25])


with top_cols[0]:
    with st.container(border=True):
        st.video(st.session_state.processed_video.path_to_video)

with top_cols[1]:
    start_time_str = st.text_input("Question Time", "00:00")
    start_time_dt = datetime.datetime.strptime(start_time_str, "%M:%S")
    start_time = start_time_dt.minute * 60 + start_time_dt.second
    sub_cols = st.columns(2)
    question_type = st.selectbox("Question Type", ["Multiple Choice", "True/False"])

    if st.button("Generate Question"):
        my_maker = quiz_generator.QuizQuestionMaker(start_time, start_time, st.session_state.processed_video)
        question = my_maker.get_question(question_type)
        # Show the quiz question
        st.session_state.question_element = quiz_frontend.QuizQuestion(question["question"], question["answer"], question["options"], question["question_type"])
if st.session_state.question_element is not None:
    st.session_state.question_element.handle()





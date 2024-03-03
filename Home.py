import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64
from st_clickable_images import clickable_images

st.set_page_config(
    page_title="Name",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

if "processed" not in st.session_state:
    st.session_state["processed"] = None
if "processed_video" not in st.session_state:
    st.session_state["processed_video"] = None
if "video" not in st.session_state:
    st.session_state["video"] = None



col1, col2, col3 = st.columns(3)

col2.write(r"$\textsf{\Huge LectureGenie}$")

# st.write(r"$\textsf{\normalsize A web application to help you understand and retain information from your study materials}$")

st.write("##### A web application to help you understand and retain information from your study materials. Usage is simple and user-friendly:")


st.markdown(
    """

    1. **Upload your lecture video/slides** to the application for processing
    2. **Save the processed media** to your device for future reference
    3. Once the video has been processed you can [probably put pictures in for each bullet point]
        - **Use generated quiz questions** with the processed information
        - **Generate a general notes sheet** and save it to your device
        - **Generate flashcards** for important terms from your media
"""
)



#col4.image('Video_Processing.jpg', use_column_width=True, caption='Video Processing')


images = []
for file in ["Video_Processing.jpg", "Video_Quiz.jpg", "Notes_Generator.jpg", "Flashcard_Generator.jpg"]:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        images.append(f"data:image/jpeg;base64,{encoded}")

clicked = clickable_images(
    images,
    titles=[f"Image #{str(i)}" for i in range(2)],
    div_style={"display": "flex", "justify-content": "left", "flex-wrap": "wrap"},
    img_style={"margin": "5px", "height": "160px"},
)

col4, col5, col6, col7= st.columns(4)


col4.write("Video Processing")
col5.write("Video Quiz")
col6.write("Notes Generator")
col7.write("Flashcard Generator")

if(clicked == 0):
    switch_page("Video Processing")

if(clicked == 1):
    switch_page("Video Quiz")

if(clicked == 2):
    switch_page("Notes Generator")

if(clicked == 3):
    switch_page("Flashcard Generator")
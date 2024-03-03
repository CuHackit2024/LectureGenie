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

import add_title
add_title.add_logo()

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

    1. **Upload your lecture video** to the application for processing
    2. **Save the processed media** to your device for future reference
    3. Once the video has been processed you can:
        - **Use generated quiz questions** with the processed information
        - **Generate a general notes sheet** and save it to your device
        - **Generate flashcards** for important terms from your media
"""
)



#col4.image('Video_Processing.jpg', use_column_width=True, caption='Video Processing')


images = []
for file in ["icons/Video_Processing.png", "icons/Video_Quiz.png", "icons/Notes_Generator.png", "icons/Flashcard_Generator.png"]:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        images.append(f"data:image/jpeg;base64,{encoded}")

clicked = clickable_images(
    images,
    titles=[f"Image #{str(i)}" for i in range(0)],
    div_style={"display": "flex", "justify-content": "left", "flex-wrap": "wrap"},
    img_style={"margin": "5px", "height": "160px"},
)

col4, col5, col6, col7= st.columns(4)


# Replace "Your text here" with your desired content
text = ["Video Processing", "Video Quiz", "Notes Generator", "Flashcard Generator"]

st.markdown(f"""
<style>
  body {{
    margin: 0; /* Remove default browser margins */
    padding: 0; /* Remove default browser paddings */
  }}

  .text-container {{
    display: flex; /* Arrange elements horizontally */
    justify-content: space-around; /* Evenly distributed elements with space on edges */
    width: 100%; /* Stretch the container to full width */
    margin-top: -50px; /* Add top margin for spacing */
  }}

  .text {{
    padding: 10px; /* Add padding to each text element */
    border: none; /* Remove default border */
    margin-right: 10px; /* Add spacing between elements */
  }}

  .text:first-child {{ /* Style the first text element (Video Processing) */
    margin-left: -5px; /* Add left margin for spacing */
  }}

  .text:last-child {{ /* Style the last text element (Flashcard Generator) */
    margin-right: 5px; /* Add right margin for spacing */
  }}

  .text:nth-child(3) {{ /* Style the third element (Notes Generator) */
    margin-right: -25px; /* Shift it slightly to the right */
  }}
</style>

<div class="text-container">
  {''.join([f'<div class="text">{item}</div>' for item in text])}
</div>
""", unsafe_allow_html=True)

if(clicked == 0):
    switch_page("Video Processing")

if(clicked == 1):
    switch_page("Video Quiz")

if(clicked == 2):
    switch_page("Notes Generator")

if(clicked == 3):
    switch_page("Flashcard Generator")
import streamlit as st
import time

def add_logo():
    print("Add logo called: ", time.time())
    if "processed_video" not in st.session_state:
        st.session_state["processed_video"] = None
    # The image is stored at icon.png

    # Access the video name from the session state
    video_name = st.session_state["processed_video"].video_name if st.session_state["processed_video"] else None

    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url("https://raw.githubusercontent.com/CuHackit2024/LectureGenie/main/icon_small.png");
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 40px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Lecture Genie";
                margin-left: 20px;
                margin-top: 40px;
                font-size: 30px;
                position: absolute;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


add_logo()

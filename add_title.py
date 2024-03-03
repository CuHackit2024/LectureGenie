import streamlit as st

def add_logo():
    # The image is stored at icon.png
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
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 30px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
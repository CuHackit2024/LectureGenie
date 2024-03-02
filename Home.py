import streamlit as st

st.set_page_config(
    page_title="Name",
    page_icon="🧊",
)

st.write("# Welcome to [Product]! 👋")


st.markdown(
    """
    [Product] is a web application that is designed to help you with understanding and retaining information from 
    your study materials. Usage is simple and user-friendly:
    
    
    **👈 Use the sidebar to navigate from page to page, making sure to start with video processing!**

    1. **Upload your lecture video/slides** to the application for processing
    2. **Save the processed media** to your device for future reference
    3. Once the video has been processed you can [probably put pictures in for each bullet point]
        - **Use generated quiz questions** with the processed information
        - **Generate a general notes sheet** and save it to your device
        - **Generate flashcards** for important terms from your media
"""
)

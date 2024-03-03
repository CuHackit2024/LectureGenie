import streamlit as st

def hello():
    st.write("hello")

def play_video_with_tracking(video_url):
  try:
    # Embed video using st.video
    video_element = st.video(video_url)

  except Exception as e:
    st.error(f"Error playing video: {e}")

  # Display playback position (if available)
  if "playback_position" in st.session_state:
    st.write(f"Current playback position: {st.session_state['playback_position']:.2f} seconds")
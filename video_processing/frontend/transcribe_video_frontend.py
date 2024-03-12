import cv2
import streamlit as st
from video_processing.backend.transcript.whisper_transcription import transcribe
from video_processing.processed_video import ProcessedVideo, Segment


def transcribe_video_frontend():
    status = st.empty()
    # blocking call to wait for the transcription to complete
    status.status("Waiting for transcription to complete...")
    transcription_segments = []
    for update in transcribe(st.session_state["processed_video"].path_to_video):
        if isinstance(update, list):
            transcription_segments = update
            break
        status.progress(update.progress, str(update))

    st.session_state["processed_video"].segments = transcription_segments

    # If there are less than 2 segs
    if len(st.session_state["processed_video"].segments) < 2:
        st.warning("This video doesn't have a lot of content to transcribe."
                   "Relying on video content entirely.")

        # Replacing it with 10 evenly spaced timestamps
        # Get the length of the video in second using opencv
        cap = cv2.VideoCapture(st.session_state["processed_video"].path_to_video)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        timestamps = [i / fps for i in range(0, total_frames, total_frames // 10)]
        st.session_state["processed_video"].segments = []
        # The end time is the start time of the next seg
        for i in range(len(timestamps) - 1):
            # Using the segment object instead
            st.session_state["processed_video"].segments.append(
                Segment(
                    start=timestamps[i],
                    end=timestamps[i + 1],
                    text="N/A",
                )
            )

        if len(st.session_state['processed_video'].segments) > 16:
            st.session_state['processed_video'].reduce_seg_count(16)

        st.session_state["video_processing_stage"] = "keyframe_processing"
    else:
        if len(st.session_state['processed_video'].segments) > 16:
            st.session_state['processed_video'].reduce_seg_count(16)
        st.session_state["video_processing_stage"] = "keyframe_processing"

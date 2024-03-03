
# import streamlit as st
# from notecard_generation.notecard_generator import NotecardGenerator  # Adjust the import path
# from video_processing.transcript.video_transcriber import VideoTranscriber  # Ensure this is your transcriber class

# # Assuming add_title.add_logo() is a custom function you've defined elsewhere
# import add_title

# # Set Streamlit page config
# st.set_page_config(page_title="Generate a Notesheet", page_icon="🧊")

# add_title.add_logo()

# st.title("Generate A Notesheet")

# # Initialize the VideoTranscriber
# transcriber = VideoTranscriber(region="us-west-2", s3_bucket="transcibe-cuhackit", job_name_prefix="TRANSCRIBE")

# # Check if a job name is already available in the session state
# if 'job_name' in st.session_state and st.session_state['job_name']:
#     job_name = st.session_state['job_name']
#     # Proceed without asking for job name again
#     st.write(f"Using job name from previous input: {job_name}")
# else:
#     # Ask for job name if not available in session state
#     job_name = st.text_input("Enter the transcription job name")
#     if job_name:
#         st.session_state['job_name'] = job_name

# if st.button('Fetch Transcript and Generate Notesheet') and job_name:
#     # Fetch the transcript text using the transcriber
#     transcript_text = transcriber.get_transcription_text(job_name)

#     if transcript_text:
#         # Generate notesheet from the fetched transcript
#         generator = NotecardGenerator(transcript_text)
#         notesheet_text = generator.generate_notecards()
        
#         # Save the notesheet text in session state to persist it
#         st.session_state['notesheet_text'] = notesheet_text
#     else:
#         st.error("Failed to fetch transcript. Please check the job name and try again.")

# # Display and offer download for notesheet if available
# if 'notesheet_text' in st.session_state and st.session_state['notesheet_text']:
#     st.markdown("## Notesheet Preview")
#     st.markdown(st.session_state['notesheet_text'], unsafe_allow_html=True)
    
#     # Download button
#     st.download_button(label="Download Notesheet as TXT",
#                        data=st.session_state['notesheet_text'].encode('utf-8'),
#                        file_name="notesheet.txt",
#                        mime="text/plain")
# else:
#     # Message when there is no notesheet to display
#     st.write("No notesheet to display. Please fetch a transcript to generate a notesheet.")

import streamlit as st
from notecard_generation.notecard_generator import NotecardGenerator  # Adjust the import path
from video_processing.transcript.video_transcriber import VideoTranscriber  # Ensure this is your transcriber class
from processed_video import ProcessedVideo
# Assuming necessary imports and setup are done here

# Initialize or fetch necessary data
transcriber = VideoTranscriber(region="us-west-2", s3_bucket="transcibe-cuhackit", job_name_prefix="TRANSCRIBE")
job_name = st.session_state.get('job_name', '')

def get_combined_content():
    """Fetches the transcript and descriptions, combines them, and returns the combined text."""
    transcript_text = ""
    descriptions = ""
    
    # Fetch transcript if available
    if job_name:
        transcript_text = transcriber.get_transcription_text(job_name)
    
    
    #if processed_video is not in the sessions state make the json from the example and put it in the session state
    if "processed_video" not in st.session_state:
        #create a file path data/data_science_full.json


        st.session_state["processed_video"] = ProcessedVideo.load_from_json("/Users/justinsilva/cuhackit/lecturegenie/data/data_science_full.json")
    
    
    # Compile descriptions if available
    if 'processed_video' in st.session_state and st.session_state['processed_video']:
        descriptions = ". ".join([segment['frame_description'] for segment in st.session_state["processed_video"].segments])
    
    return transcript_text, descriptions

if st.button('Generate Notecards'):
    transcript_text, descriptions = get_combined_content()
    if not transcript_text and not descriptions:
        st.error("No content available for generating notecards. Please ensure transcript and descriptions are available.")
    else:
        # Generate notecards from combined content
        generator = NotecardGenerator(transcript_text, descriptions)
        notecards_text = generator.generate_notecards()
        if notecards_text:
            st.session_state['notecards_text'] = notecards_text
            st.markdown("## Generated Notecards")
            st.markdown(notecards_text, unsafe_allow_html=True)
            st.download_button(label="Download Notecards as TXT",
                               data=notecards_text.encode('utf-8'),
                               file_name="notecards.txt",
                               mime="text/plain")

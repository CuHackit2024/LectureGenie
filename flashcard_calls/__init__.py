import pandas as pd
import json
import streamlit as st 

def parse(definitions_text, df):
    lines = definitions_text.split("\n")
    term_definitions = {}
    current_term = None

    for line in lines:
        if line.startswith("Term:"):
            current_term = line[len("Term:"):].strip()
        elif line.startswith("Definition:"):
            definition = line[len("Definition:"):].strip()
            term_definitions[current_term] = definition

    # Create a new DataFrame from the dictionary
    new_df = pd.DataFrame(list(term_definitions.items()), columns=['Term', 'Definition'])

    # Concatenate the new DataFrame with the existing one
    df = pd.concat([df, new_df], ignore_index=True)

    return df

def parse_processed():
    processed_video = st.session_state.processed_video

    texts = []

    # Loop over the segments in chunks of 10
    for i in range(0, len(processed_video.segments), 10):
        # Initialize an empty string to store the texts for the current chunk
        chunk_texts = ""

        # Loop over the current chunk of segments
        for segment in processed_video.segments[i:i + 10]:
            # Extract the text and frame description
            text = segment.text
            frame_description = segment.frame_description

            # Add the text and frame description to the chunk texts
            chunk_texts += text + "\n\n" + frame_description + "\n\n"

        # Add the chunk texts to the texts
        texts.append(chunk_texts)

    return texts


# import google.generativeai as genai
# import toml
# import streamlit as st

# class NotecardGenerator:
#     def __init__(self, transcript: str):
#         """
#         Initializes the notecard generator with the full video transcript.
#         :param transcript: The full transcript of the video
#         """
#         self.transcript = transcript

#         key = toml.load("keys.toml")['keys'][0]
#         genai.configure(api_key=key)
#         self.model = genai.GenerativeModel('gemini-pro')

#     def generate_notecards(self) -> None:
#         """
#         Generates notecards based on the full video transcript.
#         """
#         prompt = "Generate comprehensive notecards summarizing the key points and topics from the following transcript:\n\n" + self.transcript
        
#         response = self.model.generate_content([prompt])
#         # response_text = response.text.strip()
#         response_text = response.text
#         return response_text
    
#     def compile_descriptions_and_generate_notecards():
#         if "processed_video" in st.session_state and st.session_state["processed_video"]:
#             # Concatenate all frame descriptions into a single text block
#             descriptions = ". ".join([segment['frame_description'] for segment in st.session_state["processed_video"].segments])
            
#             # Pass the concatenated descriptions to the NotecardGenerator
#             generator = NotecardGenerator(descriptions)
#             notecards_text = generator.generate_notecards()
            
#             return notecards_text
#         else:
#             st.error("Processed video data is not available.")
#             return ""

import google.generativeai as genai
import toml

class NotecardGenerator:
    def __init__(self, transcript: str, descriptions: str):
        """
        Initializes the notecard generator with both the full video transcript and frame descriptions.
        :param transcript: The full transcript of the video.
        :param descriptions: Combined text of all frame descriptions.
        """
        self.transcript = transcript
        self.descriptions = descriptions

        key = toml.load("keys.toml")['gemini']['keys'][0]
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_notecards(self) -> str:
        """
        Generates notecards based on the combined transcript and descriptions.
        """
        combined_content = f"{self.transcript}\n\nFrame Descriptions:\n{self.descriptions}"
        prompt = "Generate comprehensive notecards summarizing the key points and topics from the following content:\n\n" + combined_content
        
        response = self.model.generate_content([prompt])
        return response.text

        

    

# Example usage
if __name__ == "__main__":
    transcript = "Your video transcript goes here."
    generator = NotecardGenerator(transcript)
    generator.generate_notecards()

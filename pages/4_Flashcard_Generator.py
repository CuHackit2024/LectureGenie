import streamlit as st
import pandas as pd
import random
import google.generativeai as genai
import toml
import flashcard_calls
from PIL import Image

if "flashcards" not in st.session_state:
    st.session_state.flashcards = None

text = """Starfish or sea stars are star-shaped echinoderms belonging to the class Asteroidea (/ˌæstəˈrɔɪdiə/). 
Common usage frequently finds these names being also applied to ophiuroids, which are correctly referred to as 
brittle stars or basket stars. Starfish are also known as asteroids due to being in the class Asteroidea. About 1,
900 species of starfish live on the seabed in all the world's oceans, from warm, tropical zones to frigid, 
polar regions. They are found from the intertidal zone down to abyssal depths, at 6,000 m (20,000 ft) below the 
surface. Starfish are marine invertebrates. They typically have a central disc and usually five arms, though some 
species have a larger number of arms. The aboral or upper surface may be smooth, granular or spiny, and is covered 
with overlapping plates. Many species are brightly coloured in various shades of red or orange, while others are 
blue, grey or brown. Starfish have tube feet operated by a hydraulic system and a mouth at the centre of the oral or 
lower surface. They are opportunistic feeders and are mostly predators on benthic invertebrates. Several species have 
specialized feeding behaviours including eversion of their stomachs and suspension feeding. They have complex life 
cycles and can reproduce both sexually and asexually. Most can regenerate damaged parts or lost arms and they can 
shed arms as a means of defense. The Asteroidea occupy several significant ecological roles. Starfish, such as the 
ochre sea star (Pisaster ochraceus) and the reef sea star (Stichaster australis), have become widely known as 
examples of the keystone species concept in ecology. The tropical crown-of-thorns starfish (Acanthaster planci) is a 
voracious predator of coral throughout the Indo-Pacific region, and the Northern Pacific seastar is on the list of 
the World's 100 Worst Invasive Alien Species."""


def flashcards_game(terms_definitions, definitions):
    flipped = st.checkbox("Flip Terms and Definitions", key="flip_terms_definitions")

    terms_definitions["Definition"] = definitions
    if "guess" not in st.session_state:
        st.session_state.guess = ""
    if "term" not in st.session_state or "definition" not in st.session_state:
        # Randomly select a term
        random_index = random.randint(0, len(terms_definitions) - 1)
        st.session_state.term = terms_definitions.iloc[random_index]['Term']
        st.session_state.definition = terms_definitions.iloc[random_index]['Definition']

    # Ask the user to guess the definition
    if flipped:
        definition_prompt = "What is the term for: \n\n**" + st.session_state.definition + "**"
    else:
        definition_prompt = "What is the definition for: \n\n**" + st.session_state.term + "**"
    st.markdown(definition_prompt)
    st.session_state.guess = st.text_input("Your guess:", value=st.session_state.guess)

    if st.button("Submit"):
        # Check the user's guess
        if flipped:
            correct_answer = st.session_state.term
        else:
            correct_answer = st.session_state.definition

        if st.session_state.guess.lower() == correct_answer.lower():
            st.write("Correct!")
        else:
            st.write(f"Here is your answer: **{st.session_state.guess}**.\n\n "
                     f"The exact definition is: **{correct_answer}**")

        # Ask the user if they want to continue
        continue_game = st.button("Continue game")
        if not continue_game:
            # Reset the term, definition, and guess for the next round
            random_index = random.randint(0, len(terms_definitions) - 1)
            st.session_state.term = terms_definitions.iloc[random_index]['Term']
            st.session_state.definition = terms_definitions.iloc[random_index]['Definition']
            st.session_state.guess = ""


st.set_page_config(
    page_title="Generate Flash Cards",
page_icon=Image.open("icon_icon.png"),
)

import add_title

add_title.add_logo()

st.subheader("Generate Flash Cards")

if "term_definitions" not in st.session_state:
    st.session_state.term_definitions = pd.DataFrame(columns=["Term", "Definition"])
    st.session_state.term_definitions.insert(0, 'Show Definitions', False)

if st.session_state.processed_video is None:
    st.markdown("""Simply press the generate button below to generate some flashcards
    from the processed video.""")

    key = toml.load("keys.toml")["gemini"]['keys'][random.randint(0, 4)]
    genai.configure(api_key=key)

    if st.button("Generate Flashcards"):
        st.session_state.flashcards = True
        model = genai.GenerativeModel('gemini-pro')
        prompt = open("flashcard_calls/prompt.txt", "r").read().strip()
        prompt = prompt.replace("$INFO", text)
        response = model.generate_content([prompt])
        response_text = response.text
        st.session_state.term_definitions = flashcard_calls.parse(response_text, st.session_state.term_definitions)

    if st.session_state.flashcards:
        st.markdown("""Flashcards have been generated! You can now view the terms and definitions below.
        If you want to change the format of the questions you are asked, you can flip the terms and definitions.
        You can also play a game that asks you to fill in a term or a definition, depending on your choice.""")

        flash_tab, game_tab = st.tabs(["Flashcards", "Game"])

        definitions = st.session_state.term_definitions["Definition"]

        st.session_state.term_definitions["Definition"] = ""

        with flash_tab:
            if st.checkbox("Flip Terms and Definitions"):
                st.session_state.term_definitions = st.session_state.term_definitions.rename(columns={"Term": "Definition", "Definition": "Term"})
                st.session_state.term_definitions["Term"] = definitions
                definitions = st.session_state.term_definitions["Definition"]

            reveal_definitions = st.checkbox("Reveal Definitions")
            if reveal_definitions:
                st.session_state["Show Definitions"] = True
                st.session_state.term_definitions["Show Definitions"] = True

            flashcard_container = st.container(height=400)

            # Display all terms with checkboxes and definitions
            for index, row in st.session_state.term_definitions.iterrows():
                with (flashcard_container):
                    # Display button, term, and definition in a row
                    show_definition = st.checkbox(f"{row['Term']}",
                                                  value=reveal_definitions, key=f"checkbox_{index}")
                    if show_definition:
                        row['Definition'] = definitions[index]
                        st.write(f"**{row['Definition']}**")
                    # Add a line break for better separation
                    st.markdown("<br>", unsafe_allow_html=True)
        with game_tab:
            flashcards_game(st.session_state.term_definitions, definitions)

else:
    st.error("Please go to video processing, and process a video before generating flashcards. ")
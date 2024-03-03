import streamlit as st
import pandas as pd
import random

if "flashcards" not in st.session_state:
    st.session_state.flashcards = None


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


# submit an api call with the processed video table to generate terms and definitions, using sample right now
# df = pd.read_csv("data/processed_video.csv")
sample = {
    "cochlea": "The coiled tube in the inner ear that contains the auditory receptors is called the:",
    "spicy": "Gustatory rececptors are sensitive to all of the following taste receptors EXCEPT:",
    "smell": "The thalamus process information for all of the following senses EXCEPT:",
    "lips": "Which of the following areas of the body has the largest number of sensory neurons?",
    "selective attention": "The ability to choose specific stimuli to learn about while filtering out or ignoring other information is called:",
    "retina": "The light-sensitive inner surface of the eye, containing the rods and cones, is the:",
    "Gestalt psychologists emphasized that": "we organize sensory information into meaningful patterns",
    "50% of time": "The absolute threshold is the minimum amount of stimulation that a person needs to detect a stimulus:",
    "Kinesthesis refers to the": "system for sensing the position and movement of muscles, tendons, and joints.",
    "cornea, pupil, lens, retina": "Which of the following is the correct order of the structures through which light passes after entering the eye?",
    "The size of the pupil is controlled by the": "iris",
    "The receptor of the eye that functions best in dim light is the": "rod",
    "Which of the following is not one of the basic tastes?": "bland",
    "In the opponent-process theory, the three pairs of processes are": "red-green, blue-yellow, black-white",
    "phi phenomenon": "When a pair of lights flashing in quick succession seems to an observer to be one light moving from place to place, the effect is referred to as",
    "Adaptation": "The longer an individual is exposed to a strong odor, the less aware of the odor the individual becomes. This phenomenon is known as sensory",
    "absolute threshold": "The minimum intensity at which a stimulus can be detected at least 50 percent of the time is known as the:",
    "Intensity": "Which of the following is NOT a Gestalt principle of perceptual organization?",
    "signal detection theory": "When Jason practices the drums, he tends not ot hear the phone. Today he is expecting a call from a record producer and answers the phone each time it rings even when he is practicing the drums. Which of the following explains why Jason hears the phone today?"
}

term_definitions = pd.DataFrame(sample, index=[0])
term_definitions = term_definitions.transpose()
term_definitions = term_definitions.reset_index()
term_definitions.columns = ['Term', 'Definition']

st.set_page_config(
    page_title="Generate Flash Cards",
    page_icon="🧊",
)

st.subheader("Generate Flash Cards")

# temporary code to simulate the process of generating quiz questions
# st.session_state.processed_video = True

if st.session_state.processed_video is None:
    st.markdown("""Simply press the generate button below to generate some flashcards 
    from the processed video.""")
    if st.button("Generate Flashcards"):
        st.session_state.flashcards = True
        # this should somehow submit an api call with the processed video table to generate terms and definitions\
    if st.session_state.flashcards:
        st.markdown("""Flashcards have been generated! You can now view the terms and definitions below. 
        If you want to change the format of the questions you are asked, you can flip the terms and definitions. 
        You can also play a game that asks you to fill in a term or a definition, depending on your choice.""")

        flash_tab, game_tab = st.tabs(["Flashcards", "Game"])

        definitions = term_definitions["Definition"]

        term_definitions.insert(0, 'Show Definitions', False)


        term_definitions["Definition"] = ""

        with flash_tab:
            if st.checkbox("Flip Terms and Definitions"):
                term_definitions = term_definitions.rename(columns={"Term": "Definition", "Definition": "Term"})
                term_definitions["Term"] = definitions
                definitions = term_definitions["Definition"]

            reveal_definitions = st.checkbox("Reveal Definitions")
            if reveal_definitions:
                st.session_state["Show Definitions"] = True
                term_definitions["Show Definitions"] = True

            flashcard_container = st.container(height=400)

            # Display all terms with checkboxes and definitions
            for index, row in term_definitions.iterrows():
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
            flashcards_game(term_definitions, definitions)


else:
    st.error("Please go to video processing, and process a video before generating flashcards. ")

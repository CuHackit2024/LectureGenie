import streamlit as st
import hashlib

AVAILABLE_QUESTIONS = ["Multiple Choice", "True/False"]


class QuizQuestion:
    def __init__(self, question, answer, options, question_type):
        self.question = question
        self.answer = answer
        self.options = options
        self.question_type = question_type

        self.id = hashlib.sha256(self.question.encode()).hexdigest()
        self.given_answer = None

    def set_given_answer(self, given_answer):
        """
        Sets the given answer for the question
        :param given_answer: The answer given by the user
        """
        self.given_answer = given_answer
        print(f"Given answer: {self.given_answer}")

    def render_multiple_choice(self):
        """
        Renders a multiple choice question on streamlit
        """
        st.write(self.question)
        chosen = st.radio("Select One", self.options)
        if st.form_submit_button("Submit"):
            self.set_given_answer(chosen)

    def render_true_false(self):
        """
        Renders a true/false question on streamlit
        """
        st.write(self.question)
        chosen = st.radio("True/False", ["True", "False"])
        if st.form_submit_button("Submit"):
            self.set_given_answer(chosen)

    def handle(self):
        """
        Draws and handles the question on streamlit
        """
        with st.form(key=self.id):
            if self.question_type == "Multiple Choice":
                self.render_multiple_choice()
            elif self.question_type == "True/False":
                self.render_true_false()
            else:
                raise ValueError(f"Question type must be one of {AVAILABLE_QUESTIONS}")

    def __str__(self):
        return f"Question: {self.question}\nAnswer: {self.answer}\nOptions: {self.options}"


class QuizQuestionMaker:

    def __init__(self, start_timestamp, end_timestamp, processed_video, question_type):
        """
        Generates a quiz question based on info from the video.
        :param start_timestamp: The start time of the info the question is based on
        :param end_timestamp: The end time of the info the question is based on
        :param processed_video: The processed video object
        """
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.processed_video = processed_video
        if question_type not in AVAILABLE_QUESTIONS:
            raise ValueError(f"Question type must be one of {AVAILABLE_QUESTIONS}")
        self.question_type = question_type

    def ask_gemini(self):
        """
        Ask a question based on the Gemini video.
        """
        raise NotImplementedError("This method has not been implemented yet.")


# Testing
if __name__ == "__main__":
    # Setting up a Streamlit app
    st.title("Quiz Question Handler")
    st.write("This is a simple Streamlit app to handle quiz questions.")

    # Creating a mc quiz question
    question_mc = QuizQuestion("What is the capital of France?", "Paris",
                            ["Paris", "London", "Berlin", "Madrid"], "Multiple Choice")
    question_mc.handle()

    # Creating a tf quiz question
    question_tf = QuizQuestion("The capital of France is Paris.", "True", None, "True/False")
    question_tf.handle()

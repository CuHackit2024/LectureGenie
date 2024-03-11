from .utils import AVAILABLE_QUESTIONS
import streamlit as st
import hashlib


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

    def render_multiple_choice(self):
        """
        Renders a multiple choice question on streamlit
        """
        st.write(self.question)
        chosen = st.radio("Select One", self.options)
        if st.form_submit_button("Submit"):
            print("Chosen:", chosen)
            # Get index of chosen option
            chosen_index = self.options.index(chosen)
            chosen = ["A", "B", "C", "D"][chosen_index]
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

        if self.given_answer is not None:
            print("Given answer  :", self.given_answer)
            print("Correct answer:", self.answer)
            if self.given_answer == self.answer:
                st.success("Correct!")
            else:
                st.error("Incorrect!")

    def __str__(self):
        return f"Question: {self.question}\nAnswer: {self.answer}\nOptions: {self.options}"


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

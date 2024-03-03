from .utils import AVAILABLE_QUESTIONS
import google.generativeai as genai
import toml
from processed_video import ProcessedVideo
import random


class QuizQuestionMaker:

    def __init__(self, start_timestamp: int, end_timestamp: int, processed_video: ProcessedVideo):
        """
        Generates a quiz question based on info from the video.
        :param start_timestamp: The start time of the info the question is based on
        :param end_timestamp: The end time of the info the question is based on
        :param processed_video: The processed video object
        """
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.processed_video = processed_video

        keys = toml.load("keys.toml")["gemini"]['keys']
        key = random.choice(keys)
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel('gemini-pro')

    def gen_info(self) -> str:
        """
        Comes up with what info to provide in the prompt for the question create.
        :return: string to insert into the prompt
        """

        # Find the segment with the end time closest to the start time of the question
        relevant_segment = None
        for segment in self.processed_video.segments:
            if float(segment.start) <= self.start_timestamp <= float(segment.end):
                relevant_segment = segment
                break
        if relevant_segment is None:
            print("No relevant segment found, using first segment")
            relevant_segment = self.processed_video.segments[0]

        info = relevant_segment.text + " " + relevant_segment.frame_description
        return info

    @staticmethod
    def parse_mcq(response_text: str) -> tuple:
        """
        Parses the response from the model for a multiple choice question
        :param response_text: The response from the model
        :return: A tuple of the question, answer, and options
        """
        # Grab section between "<start>" and "<end>"
        start = response_text.find("<start>")
        end = response_text.find("<end>")
        response_text = response_text[start + 7:end].strip()

        lines = response_text.split("\n")
        options = []
        letters = ["A", "B", "C", "D"]

        question = None
        answer = None
        explanation = None

        for line in lines:
            if line.startswith("Question:"):
                question = line[9:].strip()
                continue

            elif line.startswith("Correct Answer:"):
                answer = line[15:].strip()
                if answer[-1] == ")":
                    answer = answer[:-1]
                continue

            elif line.startswith("Explanation:"):
                explanation = line[12:].strip()

            for letter in letters:
                if line.startswith(f"{letter}) "):
                    options.append(line[3:].strip())

        if question is None:
            raise ValueError("Question not found in response: " + response_text)
        assert answer is not None
        assert len(options) == 4

        return question, answer, options, explanation

    @staticmethod
    def parse_tf(response_text: str) -> tuple:
        """
        Parses the response from the model for a true/false question
        :param response_text: The response from the model
        :return: A tuple of the question and answer
        """
        # Grab section between "<start>" and "<end>"
        start = response_text.find("<start>")
        end = response_text.find("<end>")
        response_text = response_text[start + 7:end].strip()

        lines = response_text.split("\n")

        question = None
        answer = None
        explanation = None

        for line in lines:
            if line.startswith("Question:"):
                question = line[9:].strip()
                continue

            elif line.startswith("IsTrue:"):
                answer = line[7:].strip()

            elif line.startswith("Explanation:"):
                explanation = line[12:].strip()

        assert question is not None
        assert answer is not None
        assert explanation is not None

        return question, answer, explanation

    def get_question(self, question_type):
        """
        Ask a question based on the Gemini video.
        """
        if question_type == "Multiple Choice":
            prompt = open("quiz_questions/prompts/mq_prompt.txt", "r").read().strip()
        elif question_type == "True/False":
            prompt = open("quiz_questions/prompts/tf_prompt.txt", "r").read().strip()
        else:
            raise ValueError(f"Question type must be one of {AVAILABLE_QUESTIONS}")

        prompt = prompt.replace("$INFO", self.gen_info())

        response = self.model.generate_content([prompt])
        response_text = response.text
        if question_type == "Multiple Choice":
            question, answer, options, explanation = self.parse_mcq(response_text)
        elif question_type == "True/False":
            question, answer, explanation = self.parse_tf(response_text)
            options = ["True", "False"]
        else:
            raise ValueError(f"Question type must be one of {AVAILABLE_QUESTIONS}")

        # make a dict
        question_dict = {
            "question": question,
            "answer": answer,
            "options": options,
            "question_type": question_type
        }
        return question_dict


# Testing
if __name__ == "__main__":
    pass


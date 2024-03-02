from .utils import AVAILABLE_QUESTIONS
import google.generativeai as genai
import toml


class QuizQuestionMaker:

    def __init__(self, start_timestamp: int, end_timestamp: int, processed_video, question_type: str):
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

        key = toml.load("keys.toml")["gemini"]['key']
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel('gemini-pro')

    def gen_info(self) -> str:
        """
        Comes up with what info to provide in the prompt for the question create.
        :return: string to insert into the prompt
        """

        info = open("quiz_questions/exampleInfo.txt", "r").read().strip()
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

        for line in lines:
            if line.startswith("Question:"):
                question = line[10:].strip()
                continue

            elif line.startswith("Correct Answer:"):
                answer = line[8:].strip()
                continue

            for letter in letters:
                if line.startswith(f"{letter}) "):
                    options.append(line[3:].strip())

        assert question is not None
        assert answer is not None
        assert len(options) == 4

        return question, answer, options

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

        for line in lines:
            if line.startswith("Question:"):
                question = line[10:].strip()
                continue

            elif line.startswith("IsTrue:"):
                answer = line[7:].strip()

        assert question is not None
        assert answer is not None

        return question, answer

    def ask_gemini(self):
        """
        Ask a question based on the Gemini video.
        """
        if self.question_type == "Multiple Choice":
            prompt = open("quiz_questions/prompts/mq_prompt.txt", "r").read().strip()
        elif self.question_type == "True/False":
            prompt = open("quiz_questions/prompts/tf_prompt.txt", "r").read().strip()
        else:
            raise ValueError(f"Question type must be one of {AVAILABLE_QUESTIONS}")

        prompt = prompt.replace("$INFO", self.gen_info())

        response = self.model.generate_content([prompt])
        response_text = response.text
        if self.question_type == "Multiple Choice":
            question, answer, options = self.parse_mcq(response_text)
        elif self.question_type == "True/False":
            question, answer = self.parse_tf(response_text)
            options = ["True", "False"]
        else:
            raise ValueError(f"Question type must be one of {AVAILABLE_QUESTIONS}")

        print(f"Question: {question}\nAnswer: {answer}\nOptions: {options}")


# Testing
if __name__ == "__main__":
    maker = QuizQuestionMaker(0, 10, "video", "Multiple Choice")
    maker.ask_gemini()

    # TF
    maker = QuizQuestionMaker(0, 10, "video", "True/False")
    maker.ask_gemini()


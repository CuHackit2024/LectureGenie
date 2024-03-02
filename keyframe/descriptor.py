import google.generativeai as genai
import toml
from PIL import Image
import PIL
from multiprocessing import Pool
from tqdm import tqdm
import random


def generate_description(data) -> str:
    """
    Generates a description of the image
    :param data: A tuple with the image, key, and prompt
    :return: A description of the image
    """
    i, image, key, prompt = data
    model = genai.GenerativeModel('gemini-pro-vision')

    print(f"{i} - using key: {key}")
    genai.configure(api_key=key)
    response = model.generate_content([prompt, image])
    try:
        response_text = response.text
    except ValueError:
        print(f"\t{i} - Error")
        return ""

    # print(f"{i} - Returning response")

    return response_text


class Descriptor:
    def __init__(self):
        self.keys = toml.load("keys.toml")["gemini"]['keys']
        random.shuffle(self.keys)
        self.key = self.keys[0]
        self.key_index = 0

    def cycle_key(self):
        self.key_index += 1
        self.key_index %= len(self.keys)
        self.key = self.keys[self.key_index]

    def generate_descriptions(self, images: list[Image]) -> list[str]:
        """
        Generates a description of the images
        :param images: The images to describe
        :return: A list of descriptions of the images
        """
        prompt = open("keyframe/prompts/description_prompt.txt", "r").read().strip()
        data = []
        for i, image in enumerate(images):
            data.append((i, image, self.key, prompt))
            self.cycle_key()

        # What is the max number of processes?
        # Can there be more than the number of core?
        # A: Yes, but it will not be faster

        with Pool(8) as p:
            descriptions = list(tqdm(p.imap(generate_description, data), total=len(data)))

        return descriptions



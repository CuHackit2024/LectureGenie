"""
This application runs completly separate from the main application.
It hosts a multiprocessing setup for getting the frame descriptions quickly
"""

import multiprocessing
from multiprocessing import Pool
import queue
import google.generativeai as genai
from toml import load
from PIL import Image
from PIL import PngImagePlugin  # Can't remove this import
from tqdm import tqdm
import random
from flask import Flask, request, jsonify
from io import BytesIO
import numpy as np

app = Flask(__name__)  # Create a Flask app

def generate_description(data):
    i, image, key, prompt = data
    # convert image to PIL
    image = Image.fromarray(image)
    model = genai.GenerativeModel('gemini-pro-vision')

    print(f"{i} - using key: {key}")
    genai.configure(api_key=key)
    print(f"{i} - Configured")
    response = model.generate_content([prompt, image])
    print(f"{i} - Generated")
    try:
        response_text = response.text
    except ValueError:
        print(f"\t{i} - Error")
        return ""

    return response_text


class Descriptor:
    def __init__(self):
        self.keys = load("keys.toml")["gemini"]['keys']
        random.shuffle(self.keys)
        self.key_index = 0
        self.key = self.keys[self.key_index]
        genai.configure(api_key=self.key)

    def cycle_key(self):
        self.key_index += 1
        self.key_index %= len(self.keys)
        self.key = self.keys[self.key_index]

    def generate_descriptions(self, images):
        """
        Generates a description of the images using multiprocessing
        :param images: The images to describe
        :return: A list of descriptions of the images
        """
        prompt = open("video_processing/keyframe/prompts/description_prompt.txt", "r").read().strip()
        data = []
        for i, image in enumerate(images):
            # Convert the PIL image to ndarray
            array_image = np.array(image)
            data.append((i, array_image, self.key, prompt))
            self.cycle_key()

        with Pool(12) as p:
            descriptions = list(tqdm(p.imap(generate_description, data), total=len(data)))

        return descriptions

@app.route('/generate_descriptions', methods=['POST'])
def handle_api_request():
    # Print everything that was sent in the request to help with debugging
    image_file_tuples = request.files.items()
    # Composed of tuples of (filename, file) the file is <FileStorage: 'image_0' (None)>

    images = [Image.open(BytesIO(i[1].read())) for i in image_file_tuples]
    print("images: ", images)
    descriptor = Descriptor()
    descriptions = descriptor.generate_descriptions(images)

    return jsonify({'descriptions': descriptions})  # Return list of descriptions as JSON

if __name__ == '__main__':
    app.run(host='localhost', port=5000)  # Start the Flask app (adjust host/port as needed)
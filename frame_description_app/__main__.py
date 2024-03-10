"""
This application runs completly separate from the main application.
It hosts a multiprocessing setup for getting the frame descriptions quickly
"""

from multiprocessing import Pool
from toml import load
from PIL import Image
from PIL import PngImagePlugin  # Can't remove this import
from tqdm import tqdm
import random
from flask import Flask, request, jsonify
from io import BytesIO
import numpy as np
from .desciption_generator import generate_description
import base64

app = Flask(__name__)  # Create a Flask app





class Descriptor:
    def __init__(self):
        self.keys = load("keys.toml")["gemini"]['keys']
        random.shuffle(self.keys)
        self.key_index = 0
        self.key = self.keys[self.key_index]

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
            data.append((i, image, self.key, prompt))
            self.cycle_key()

        with Pool(8) as p:
            descriptions = list(tqdm(p.imap(generate_description, data), total=len(data)))

        return descriptions


@app.route('/generate_descriptions', methods=['POST'])
def handle_api_request():
    with open("../progress.txt", "w") as file:
        file.write("0")

    # Print everything that was sent in the request to help with debugging
    image_file_tuples = request.files.items()
    # Composed of tuples of (filename, file) the file is <FileStorage: 'image_0' (None)>

    images = [base64.b64encode(i[1].read()).decode('utf-8') for i in image_file_tuples]

    print(f"Received {len(images)} images.")
    descriptor = Descriptor()
    descriptions = descriptor.generate_descriptions(images)

    return jsonify({'descriptions': descriptions})  # Return list of descriptions as JSON


if __name__ == '__main__':
    app.run(host='localhost', port=5000)  # Start the Flask app (adjust host/port as needed)

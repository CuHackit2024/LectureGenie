from .gemini import describe_image


def generate_description(data):
    i, image, key, prompt = data
    return describe_image(prompt, image, key)

from PIL import Image
from . import descriptor
from . import graber
import time

if __name__ == "__main__":
    start_time = time.time()
    frames = graber.timed_frames("sample_video/data_science.mp4", number_frames=50)
    time_to_get_frames = time.time() - start_time
    print(f"Time to get frames: {time_to_get_frames}")

    get_descriptions_start_time = time.time()
    my_descriptor = descriptor.Descriptor()
    descriptions = my_descriptor.generate_descriptions([Image.fromarray(f[1]) for f in frames])
    time_to_get_descriptions = time.time() - get_descriptions_start_time
    print(f"Time to get descriptions: {time_to_get_descriptions}")
    for i, description in enumerate(descriptions):
        head_index = min(50, len(description))
        print(f"Frame {i + 1}: {description[:head_index]}...")

    print(f"Total time: {time.time() - start_time}")

from . import descriptor
from . import graber
import time
from matplotlib import pyplot as plt

if __name__ == "__main__":
    start_time = time.time()
    frames = graber.timed_frames("sample_video/data_science.mp4", number_frames=5)
    time_to_get_frames = time.time() - start_time
    print(f"Time to get frames: {time_to_get_frames}")

    get_descriptions_start_time = time.time()

    descriptions = descriptor.get_descriptions([f[1] for f in frames])
    time_to_get_descriptions = time.time() - get_descriptions_start_time
    print(f"Time to get descriptions: {time_to_get_descriptions}")

    for i, description in enumerate(descriptions):
        head_index = min(50, len(description))
        print(f"Frame {i + 1}: {description[:head_index]}...")

    # Rendering description, key pairs
    for i, (frame, description) in enumerate(zip(frames, descriptions)):
        plt.imshow(frame[1])
        plt.title(description)
        plt.show()



    print(f"Total time: {time.time() - start_time}")

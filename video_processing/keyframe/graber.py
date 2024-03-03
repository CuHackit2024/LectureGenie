import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import time
import math


class Segment:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = end - start


def timed_frames(video_path: str, timestamps: list[int] = None, number_frames=None) -> list[tuple[int, np.ndarray]]:
    """
    Returns a list of frames from the video at the given timestamps
    :param video_path: The path to the video
    :param timestamps: The timestamps to get the frames from
    :param number_frames: The number of frames to get from the video, will be evenly spaced
    :return: A list of frames from the video at the given timestamps
    """
    assert (timestamps is None) != (number_frames is None), "Either timestamps or number_frames must be provided"
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if timestamps is None:
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_counts = np.linspace(0, total_frames - 1, number_frames, dtype=int)
        timestamps = [i / fps for i in frame_counts]

    frames = []
    for timestamp in timestamps:
        cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
        ret, frame = cap.read()
        if ret:
            frames.append((timestamp, frame))
    cap.release()
    return frames


if __name__ == "__main__":
    frame_count = 30
    frames_full = timed_frames("sample_video/data_science.mp4", number_frames=frame_count)
    frames = [f[1] for f in frames_full]
    print(len(frames))
    rows = int(math.sqrt(frame_count))
    cols = int(math.ceil(frame_count / rows))

    fig, ax = plt.subplots(rows, cols, figsize=(20, 10))
    for i, frame in enumerate(frames):
        ax[i // cols, i % cols].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        ax[i // cols, i % cols].axis("off")
    plt.show()

"""
This runs as its own process and is used to delete videos older than 24 hours from the user_data folder
"""

import os
import shutil
import time
from datetime import datetime

delete_time = 24 * 60 * 60  # 24 hours

# If the user_data folder doesn't exist, create it
if not os.path.exists("user_data"):
    os.mkdir("user_data")

while True:
    print(datetime.now(), "| Start a collection cycle")
    # Get all the user folders
    user_folders = os.listdir("user_data")
    for user_folder in user_folders:
        # Get all the video folders
        video_folders = os.listdir(f"user_data/{user_folder}")
        for video_folder in video_folders:
            if not os.path.isdir(f"user_data/{user_folder}/{video_folder}"):
                continue
            # Get the time the video was created
            video_folder_path = f"user_data/{user_folder}/{video_folder}"
            video_time = os.path.getctime(video_folder_path)
            # If the video is older than 24 hours, delete it
            age = time.time() - video_time
            if age > delete_time:
                print(f"Deleting {video_folder_path}, it was created at {datetime.fromtimestamp(video_time)}"
                      f" and is {age // 60} minutes old.")
                shutil.rmtree(video_folder_path)

            else:
                # Getting age in hours, minutes
                str_age = f"{age // 3600} hours, {(age % 3600) // 60} minutes"
                print(f"{video_folder_path} is {str_age} old, not deleting it yet")
    time.sleep(60 * 60)  # Check every hour
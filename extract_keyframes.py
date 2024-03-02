from moviepy.editor import VideoFileClip
from moviepy.editor import ImageClip
import os
import numpy as np

def save_keyframe(output_folder, timestamp, diff, frame):
    keyframe_path = os.path.join(output_folder, f"keyframe_{timestamp:.2f}_{diff:.2f}.jpg")
    img_clip = ImageClip(frame)
    img_clip.save_frame(keyframe_path)
    print(f"Keyframe at {timestamp:.2f} seconds saved.")

def extract_keyframes(video_path, output_folder, threshold=100):
    video = VideoFileClip(video_path)
    frame_count = 0
    prev_key_frame = None
    prev_frame_timestamp = 0
    last_checked_timestamp = 0

    print(threshold)
    # Iterate through video frames
    for timestamp, frame in video.iter_frames(with_times=True):
        # if the difference between the current frame timestamp and the last checked frame timestamp is greater than .5 seconds
        if (timestamp - last_checked_timestamp) > .5:
            if prev_key_frame is not None:

                diff = np.sum(np.abs(prev_key_frame - frame))
                last_checked_timestamp = timestamp
                print(timestamp, diff)

                # If difference exceeds threshold, consider it a keyframe
                if diff > threshold:
                    print(timestamp, diff)
                    save_keyframe(output_folder, timestamp, diff, frame)
                    prev_key_frame = frame
                    prev_frame_timestamp = timestamp
                    frame_count += 1

            else:
                # Save the first frame as a keyframe 
                save_keyframe(output_folder, timestamp, 0, frame)
                prev_key_frame = frame
                prev_frame_timestamp = timestamp
                frame_count += 1
                

            
            

    video.close()

# Example usage
video_path = "C:/Users/conno/lecturegenie/GMT20231020-103151_Recording_2736x1824.mp4"
output_folder = "C:/Users/conno/lecturegenie/output"
extract_keyframes(video_path, output_folder, threshold=5e8)


# import moviepy.editor as mpy
# import os
# import numpy as np
# from skimage.metrics import structural_similarity as ssim

# def extract_keyframes(video_path, output_folder, threshold=100, adaptive_thresholding=True, min_scene_length=5):
#     video = mpy.VideoFileClip(video_path)
#     frame_count = 0
#     prev_frame = None
#     scene_start_frame = None

#     for timestamp, frame in video.iter_frames(with_times=True):
#         if prev_frame is not None:
#             # Calculate difference using structural similarity (SSIM) or adaptive thresholding
#             if adaptive_thresholding:
#                 diff = adaptive_threshold(prev_frame, frame)  # Implement your adaptive thresholding logic
#             else:
#                 diff = ssim(prev_frame, frame, multichannel=True)  # SSIM for color videos
#                 # Handle potential None value from ssim (optional)
#                 if diff is None:
#                     diff = 0  # Assign a default value (adjust as needed)

#             # Adjust threshold based on video resolution and content
#             adjusted_threshold = threshold * (frame.shape[0] * frame.shape[1])

#             if diff > adjusted_threshold:
#                 keyframe_path = os.path.join(output_folder, f"keyframe_{timestamp:.2f}.jpg")
#                 mpy.ImageClip(frame).save_frame(keyframe_path)
#                 print(f"Keyframe at {timestamp:.2f} seconds saved.")
#                 scene_start_frame = None  # Reset scene start

#             else:
#                 # If within a scene, capture a keyframe every few seconds
#                 if scene_start_frame is not None and timestamp - scene_start_frame >= min_scene_length:
#                     keyframe_path = os.path.join(output_folder, f"keyframe_{timestamp:.2f}.jpg")
#                     mpy.ImageClip(frame).save_frame(keyframe_path)
#                     print(f"Keyframe within scene at {timestamp:.2f} seconds saved.")
#                     scene_start_frame = timestamp  # Update scene start
#                 else:
#                     scene_start_frame = scene_start_frame or timestamp  # Initiate scene start

#         prev_frame = frame
#         frame_count += 1

#     video.close()

# # Define adaptive thresholding function (replace with your preferred method)
# def adaptive_threshold(prev_frame, frame):
#     # Implement your adaptive thresholding logic here
#     # Consider local variations, noise levels, etc.
#     # Here's a basic example using local mean and standard deviation:
#     mean_diff = np.mean(np.abs(prev_frame - frame))
#     std_dev_diff = np.std(np.abs(prev_frame - frame))
#     return mean_diff + 2 * std_dev_diff  # Adjust coefficients as needed

# # Example usage
# video_path = "C:/Users/conno/lecturegenie/GMT20231020-103151_Recording_2736x1824.mp4"
# output_folder = "C:/Users/conno/lecturegenie/output"
# extract_keyframes(video_path, output_folder, threshold=20000, adaptive_thresholding=True, min_scene_length=2)





# import cv2
# import os
# from moviepy.editor import VideoFileClip

# def extract_keyframes(video_path, output_folder, interval_sec=1):
#     # Use moviepy for frame skipping to reduce processing steps
#     clip = VideoFileClip(video_path)
#     all_frames = clip.iter_frames()

#     # Process only target frames for desired interval (1 fps in this case)
#     fps = clip.fps
#     target_frames = [frame for idx, frame in enumerate(all_frames) if idx % (int(fps * interval_sec)) == 0]

#     frame_count = 0
#     prev_frame = None
#     prev_gray = None
#     prev_shot = None

#     for frame in target_frames:
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         if prev_frame is not None:
#             diff = cv2.absdiff(prev_gray, gray)
#             _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
#             if thresh.mean() > 10:
#                 if prev_shot is None or frame_count - prev_shot >= interval_sec * fps:
#                     timestamp = frame_count / fps
#                     keyframe_path = os.path.join(output_folder, f"keyframe_{timestamp:.2f}.jpg")
#                     cv2.imwrite(keyframe_path, frame)
#                     print(f"Keyframe at {timestamp:.2f} seconds saved.")
#                     prev_shot = frame_count

#         prev_frame = frame.copy()
#         prev_gray = gray.copy()
#         frame_count += 1

# # Example usage
# video_path = "C:/Users/conno/lecturegenie/GMT20231020-103151_Recording_2736x1824.mp4"
# output_folder = "C:/Users/conno/lecturegenie/output"
# extract_keyframes(video_path, output_folder, interval_sec=1)

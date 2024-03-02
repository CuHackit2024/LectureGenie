import cv2
import os
from moviepy.editor import VideoFileClip

def extract_keyframes(video_path, output_folder, interval_sec=1):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    prev_frame = None
    prev_gray = None
    prev_shot = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_frame is not None:
            diff = cv2.absdiff(prev_gray, gray)
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            if thresh.mean() > 10:
                if prev_shot is None or frame_count - prev_shot >= interval_sec * fps:
                    timestamp = frame_count / fps
                    keyframe_path = os.path.join(output_folder, f"keyframe_{timestamp:.2f}.jpg")
                    cv2.imwrite(keyframe_path, frame)
                    print(f"Keyframe at {timestamp:.2f} seconds saved.")
                    prev_shot = frame_count

        prev_frame = frame.copy()
        prev_gray = gray.copy()
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

# Example usage
video_path = "C:/Users/conno/lecturegenie/GMT20231020-103151_Recording_2736x1824.mp4"
# "C:\Users\conno\lecturegenie\GMT20231020-103151_Recording_2736x1824.mp4"

output_folder = "C:/Users/conno/lecturegenie/output"
# "C:\Users\conno\lecturegenie\output"

new_video_path = "C:/Users/conno/lecturegenie/lowerFPS.mp4"


# open the video clip
clip = VideoFileClip(video_path)

# set the desired frame rate
clip = clip.set_fps(1)

# write the modified clip to a new file
clip.write_videofile(new_video_path)


extract_keyframes(new_video_path, output_folder, interval_sec=1)

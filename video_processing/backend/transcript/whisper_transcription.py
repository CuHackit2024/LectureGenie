import whisper
import warnings
from pydub import AudioSegment
from utils import ProgressUpdate
from video_processing.processed_video import Segment

model = whisper.load_model("tiny")

warnings.filterwarnings("ignore", category=UserWarning, module="whisper.transcribe")


def transcribe(video_path):
    """
    Transcribes the audio file at the given path
    :param video_path: The path to the video file
    :return: The transcript
    """
    try:
        audio = AudioSegment.from_file(video_path)
    except IndexError:
        return []

    audio_length = len(audio)
    segment_length = 60 * 1000
    segments = []
    for i in range(0, audio_length, segment_length):
        segments.append(audio[i:i + segment_length])

    # Transcribing each segment
    transcript_segments = []
    end_time_of_last_segment = 0
    for i, segment in enumerate(segments):
        progress = (i + 1) / len(segments)
        message = "Transcribing"
        yield ProgressUpdate(progress, message)
        # Temporarily saving the segment to a file
        segment_path = "segment.wav"
        segment.export(segment_path, format="wav")

        output = model.transcribe(segment_path)

        for transcript_segment in output["segments"]:
            transcript_segments.append(Segment(transcript_segment['start'] + end_time_of_last_segment,
                                               transcript_segment['end'] + end_time_of_last_segment,
                                               transcript_segment['text']))
        if len(output['segments']) > 0:
            end_time_of_last_segment = output['segments'][-1]["end"] + end_time_of_last_segment

    yield transcript_segments


if __name__ == "__main__":
    for update in transcribe("sample_video/shorter.mp4"):
        print(update)
        if isinstance(update, list):
            for segment in update:
                print(segment)

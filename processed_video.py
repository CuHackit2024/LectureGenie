import json


class ProcessedVideo:
    def __init__(self):
        self.segments = []
        self.path_to_video = None

    def create(self, transcript: list[dict], frame_descriptions: list[str]):
        print("Transcript len: ", len(transcript))
        print("frame desciritpn len: ", len(frame_descriptions))
        assert (len(transcript) == len(frame_descriptions))
        self.segments = []
        for i, segment in enumerate(transcript):
            start = segment["start_time"]
            end = segment["end_time"]
            text = segment["transcript"]
            frame_description = frame_descriptions[i]
            self.segments.append(Segment(start, end, text, frame_description))

    def load_from_json(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            self.segments = [Segment(**segment) for segment in data["segments"]]

    def save_to_json(self, file_path):
        data = {
            "segments": [segment.__dict__ for segment in self.segments]
        }
        with open(file_path, "w") as file:
            json.dump(data, file)


class Segment:
    def __init__(self, start, end, text, frame_description=None):
        self.start = start
        self.end = end
        self.text = text
        self.frame_description = frame_description

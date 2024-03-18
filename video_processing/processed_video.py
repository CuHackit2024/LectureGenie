import json


class ProcessedVideo:
    def __init__(self):
        self.segments = []
        self.path_to_video = None
        self.video_name = "N/A"

    def check_all_good(self):
        assert self.segments is not None, "Segments is None"
        assert self.path_to_video is not None, "Path to video is None"
        assert self.video_name != "N/A", "Video name is N/A"
        assert len(self.segments) > 0, "Segments is empty"

    def add_descriptions(self, descriptions: list[str]):
        for i, description in enumerate(descriptions):
            self.segments[i].frame_description = description

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

    def get_path_to_keyframes(self):
        keyframe_folder = self.path_to_video.split("/")
        keyframe_folder = "/".join(keyframe_folder[:-1]) + "/keyframes"
        return keyframe_folder

    def get_shortest_pair(self):
        """
        Returns the two shortest adjacent segments
        :return: The two shortest segments
        """
        shortest_segments = [self.segments[0], self.segments[1]]
        shortest_length = shortest_segments[1].end - shortest_segments[0].start
        for i in range(len(self.segments) - 1):
            length = self.segments[i + 1].end - self.segments[i].start
            if length < shortest_length:
                shortest_length = length
                shortest_segments = [self.segments[i], self.segments[i + 1]]
        return shortest_segments

    def reduce_seg_count(self, count):
        """
        Iteratively combines the two shortest adjacent segments until the number of segments is equal to the count
        :param count: The number of segments to reduce to
        """

        while len(self.segments) > count:
            # Find the two shortest adjacent segments
            shortest_segments = self.get_shortest_pair()
            # Combine them
            combined_segment = Segment(shortest_segments[0].start, shortest_segments[1].end,
                                       shortest_segments[0].text + " " + shortest_segments[1].text)
            # Remove the two shortest segments
            self.segments.remove(shortest_segments[0])
            self.segments.remove(shortest_segments[1])

            # Add the combined segment
            self.segments.append(combined_segment)
            # Sort the segments by start time
            self.segments = sorted(self.segments, key=lambda x: x.start)


class Segment:
    def __init__(self, start, end, text, frame_description=None):
        self.start = start
        self.end = end
        self.text = text
        self.frame_description = frame_description

    def __str__(self):
        return f"Start: {round(self.start, 2)}, End: {round(self.end, 2)}, Text: {self.text}, Frame Description: {self.frame_description}"

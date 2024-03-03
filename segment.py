class Segment:
    def __init__(self, start, end, text):
        self.start = start
        self.end = end
        self.text = text
        self.frame_description = None

    def add_keyframe_description(self, description):
        self.frame_description = description
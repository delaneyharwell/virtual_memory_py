class FreeFrameNode:
    def __init__(self, framenumber):
        self.next = None
        self.framenumber = framenumber

class FreeFrames:
    def __init__(self, total_frames=1024):
        self.head = None
        self.create_list(total_frames)

    def create_list(self, total_frames):
        self.head = FreeFrameNode(0)
        current = self.head
        for i in range(1, total_frames):
            current.next = FreeFrameNode(i)
            current = current.next

    def allocate_frame(self):
        if self.head is None:
            return -1
        new_frame = self.head.frame_number
        self.head = self.head.next
        return new_frame

    def free_frame(self, frame_number):
        new_frame = FreeFrameNode(frame_number)
        new_frame.next = self.head
        self.head = new_frame



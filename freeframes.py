class FreeFrameNode:
    def __init__(self, framenumber):
        self.next = None
        self.framenumber = framenumber

class FreeFrames:
    def __init__(self, total_frames=1024, reserved_frames=None):
        if reserved_frames is None:
            reserved_frames = set()
        self.head = None
        self.create_list(total_frames, reserved_frames)

    def create_list(self, total_frames, reserved_frames):
        # Create a linked list of free frames excluding reserved ones.
        first = None
        current = None
        for i in range(total_frames):
            if i in reserved_frames:
                continue
            node = FreeFrameNode(i)
            if first is None:
                first = node
                current = node
            else:
                current.next = node
                current = current.next
        self.head = first

    def allocate_frame(self):
        if self.head is None:
            return -1
        new_frame = self.head.framenumber
        self.head = self.head.next
        return new_frame

    def free_frame(self, frame_number):
        new_frame = FreeFrameNode(frame_number)
        new_frame.next = self.head
        self.head = new_frame

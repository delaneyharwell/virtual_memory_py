import sys
from freeframes import FreeFrames

PM = [-1]*524288
DISK = [[0 for _ in range(512)] for _ in range(1024)]
SIZE_BIT = 9
USED_FRAMES = set()
FREE_FRAMES = FreeFrames()


def vm_manager(input_file):
    try:
        with open(input_file, 'rb') as f:
            lines = f.readlines()
            if len(lines) < 2:
                print("Initialization file must have at least two lines")
                return
            init_st(lines[0])
            init_pt(lines[1])
    except FileNotFoundError:
        print("File not found")
        return

def init_st(line):
    #(segmentnumber baseaddress size)
    items = line.decode().strip().split()
    for i in range(0, len(items), 3):
        seg = int(items[i])
        seg_limit = int(items[i+1])
        pt_base = int(items[i+2])
        PM[2*seg] = seg_limit
        PM[2*seg+1] = pt_base
        if pt_base >= 0:
            USED_FRAMES.add(pt_base)

def init_pt(line):
    #(virtualsegmentnumber, virtualpagenumber, offset)
    items = line.decode().strip().split()
    for i in range(0, len(items), 3):
        seg = int(items[i])
        page = int(items[i+1])
        pte = int(items[i+2])
        pt_base = PM[2*seg+1]
        if pt_base >= 0:
            PM[pt_base*512+page] = pte
            if pte >= 0:
                USED_FRAMES.add(pte)
        else:
            disk_block = abs(pt_base)
            DISK[disk_block][page] = pte
            if pte >= 0:
                USED_FRAMES.add(pte)

def mark_used_frames():
    global USED_FRAMES
    USED_FRAMES.add(0)
    USED_FRAMES.add(1)
    return USED_FRAMES

def extract_input(input_file):
    try:
        with open(input_file, 'rb') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    for va in line.split():
                        pa = translate_va(va)
                        if pa == -1:
                            print(-1)
    except FileNotFoundError:
        print("File not found")
        return

def translate_va(line):
    #Segment number (s) VA >> 18
    #page number (p) (VA >> 9) & 0x1FF
    #offset (w) VA & 0x1FF
    #pw (VA && 0x3FFFF
    # PA = (Framenumber * framesize) +offset
    line = int(line)
    s = line >> 18
    p = (line >> 9) & 0x1FF
    w = line & 0x1FF
    pw = line & 0x3FFFF
    segment_limit = PM[2*s]
    page_table_base = PM[2*s+1]
    if segment_limit == -1 or pw >= segment_limit:
        print("Segment limit exceeded")
        return
    #page table does not exist, allocate frame with page demanding (hopefully..)
    if page_table_base < 0:
        new_frame = allocate_new_frame()
        if new_frame == -1:
            print("No free frame available")
            return -1
        load_page_table_from_disk(new_frame, abs(page_table_base))
        if PM[2 * s + 1] < 0:
            PM[2 * s + 1] = new_frame
        page_table_base = PM[2 * s + 1]

    pte_index = page_table_base * 512 + p
    page_frame = PM[pte_index]
    #page not in memory, perform demand paging!!!
    if page_frame < 0:
        new_frame = allocate_new_frame()
        if new_frame == -1:
            print("No free frame available for page")
            return -1
        load_page_from_disk(new_frame, abs(page_frame))
        PM[pte_index] = new_frame
        page_frame = new_frame
    pa = page_frame * 512 + w
    print(pa)
    return pa

def allocate_new_frame():
    frame = FREE_FRAMES.allocate_frame()
    if frame == -1:
        print("No free frame available")
    return frame

def read_block(b, m):
    start_address = m * 512
    PM[start_address:start_address+512] = DISK[b][:]

def load_page_table_from_disk(frame, disk_block):
    PM[frame * 512: (frame + 1) * 512] = DISK[disk_block][:]

def load_page_from_disk(frame, disk_block):
    PM[frame * 512 : (frame + 1) * 512] = DISK[disk_block][:]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: need input file")
        exit(1)
    print(sys.argv[1])
    init_file = sys.argv[1]
    vm_manager(init_file)
    reserved = mark_used_frames()
    FREE_FRAMES = FreeFrames(1024, reserved_frames=reserved)
    input_file = sys.argv[2]
    extract_input(input_file)


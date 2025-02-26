import sys
from freeframes import FreeFrames

PM = [-1]*524288
DISK = [[0 for _ in range(512)] for _ in range(1024)]
SIZE_BIT = 9
FREE_FRAMES = FreeFrames(1024)


def vm_manager(input_file):
    try:
        with open(input_file, 'rb') as f:
            for i in range(2):
                line = f.readline()
                if i == 0:
                    init_st(line)
                elif i == 1:
                    init_pt(line)
    except FileNotFoundError:
        print("File not found")
        return

def init_st(line):
    #(segmentnumber baseaddress size)
    items = line.split()
    for i in range(0, len(items), 3):
        chunk = int(items[i:i+3])



def init_pt(line):
    #(virtualsegmentnumber, virtualpagenumber, offset)
    items = line.split()
    for i in range(0, len(items), 3):
        chunk = items[i:i + 3]


def extract_input(input_file):
    try:
        with open(input_file, 'rb') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                translate_va(line.strip())
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
    if w >= segment_limit:
        print("Segment limit exceeded")
        return
    #page table does not exist, allocate frame
    if page_table_base < 0:
        #todo
    page_table_base = PM[2*s+1]
    page_frame_entry = PM[page_table_base * 512 + p]
    if page_frame_entry < 0:
        #todo
    PA = PM[page_table_base * 512 + p] * 512 + w
    return PA

def allocate_new_frame():
    #todo / use linked list

def read_block(b, m):
    start_address = m * 512
    PM[start_address:start_address+512] = DISK[b][:]

def load_page_table_from_disk(frame, segment):
    PM[frame*512 : (frame+1)*512] = DISK[segment][:]

def load_page_from_disk(frame, segment, page):
    PM[frame*512 : (frame+1)*512] = DISK[segment * 512 + page][:]







if "__name__" == "__main__":
    if sys.argv.__len__() < 4:
        print("Error: need input file")
        exit(1)
    init_file = sys.argv[2]
    vm_manager(init_file)
    input_file = sys.argv[3]
    extract_input(input_file)


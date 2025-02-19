import sys

PM = [0]*524288
DISK = [[0 for _ in range(512)] for _ in range(1024)]
SIZE_BIT = 9

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
    for item, index in enumerate(line.split()):



def init_pt(line):
    for item,index in enumerate(line.split()):

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






if "__name__" == "__main__":
    if sys.argv.__len__() < 4:
        print("Error: need input file")
        exit(1)
    init_file = sys.argv[2]
    vm_manager(init_file)
    input_file = sys.argv[3]
    extract_input(input_file)


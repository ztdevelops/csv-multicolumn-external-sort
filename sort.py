import os
import uuid
import heapq

def generate_tmp_filename(filepath):
    id = uuid.uuid4()
    base, ext = os.path.splitext(os.path.basename(filepath))
    original_filename = base.split("-")[0]

    return os.path.join("tmp", f"{original_filename}-{id}{ext}")

def merge(file1_name, file2_name, output_name, header):
    output = open(output_name, "w")

    if header:
        output.write(header)
    
    file1 = None if file1_name is None else open(file1_name, "r")
    file2 = None if file2_name is None else open(file2_name, "r")
    if file1 is None and file2 is None:
        return

    file1_iter = iter([] if file1 is None else file1)
    file2_iter = iter([] if file2 is None else file2)

    merged = heapq.merge(file1_iter, file2_iter)
    for line in merged:
        output.write(line)

    if file1_name:
        file1.close()
        os.remove(file1_name)

    if file2_name:
        file2.close()
        os.remove(file2_name)
    
    output.close()

def split_half(file_to_sort, has_header=False, is_root=False, specified_output=None):
    file_to_read = open(file_to_sort, "r")
    header = None
    if has_header:
        header = file_to_read.readline()

    file1_name = None
    file2_name = None

    file1 = None
    file2 = None

    last_idx = 0
    for idx, line in enumerate(file_to_read):
        if line.strip() == "": continue

        last_idx = idx
        if idx % 2 == 0:
            if file1 is None:
                file1_name = generate_tmp_filename(file_to_sort)
                file1 = open(file1_name, "w")

            file1.write(line)
        else:
            if file2 is None:
                file2_name = generate_tmp_filename(file_to_sort)
                file2 = open(file2_name, "w")

            file2.write(line)

    file_to_read.close()
    if file1 is not None: file1.close()
    if file2 is not None: file2.close()

    if last_idx > 1:
        split_half(file1_name)
        split_half(file2_name)

    merge(file1_name, file2_name, specified_output if is_root else file_to_sort, header)

def sort_large_csv_file(file_to_sort, output_file):
    split_half(file_to_sort, has_header=True, is_root=True, specified_output=output_file)

if __name__ == "__main__":
    sort_large_csv_file("src/original.csv", "src/original-sorted.csv")
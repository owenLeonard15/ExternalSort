# my first attempt, not effective for large N, 
# see notes.txt for more details

import struct
import heapq
import os

# version 1: 2 passes
def external_sort(input_file, output_file, m):
    temp_files = []

    # first pass: read m integers from input file, sort them and write them to a temp file
    # repeat until all integers in the input file have been read
    # Number of files = N/m
    with open(input_file, 'rb') as f:
        chunk = f.read(4*m)
        print("memory size (integers): ", m)
        while chunk:
            # struct.unpack() converts the bytes to numbers
            # 'i' is for 4-byte signed integer
            # len(chunk) // 4 is the number of integers in the chunk
            # 'i' * (len(chunk) // 4) is a string of 'i's of length (len(chunk) // 4)
            numbers = list(struct.unpack('i' * (len(chunk) // 4), chunk))
            numbers.sort()

            temp_file = f'temp_file_{len(temp_files)}.dat'
            with open(temp_file, 'wb') as temp_f:
                # struct.pack() converts the numbers to bytes
                # *numbers unpacks the numbers list
                temp_f.write(struct.pack('i'*len(numbers), *numbers))
            temp_files.append(temp_file)
            chunk = f.read(4*m)

    # Open all temporary files and prepare to read them.
    # if N >> M and N/M > M (a very large number of files) and we open all of them at once we will run out of memory
    # so... might need to do more than 2 passes if N >> M and N/M > M
    open_files = []
    for temp_file in temp_files:
        open_files.append(open(temp_file, 'rb'))

    if(len(open_files) > m):
        print("number of open files > m: ", len(open_files))
    else:
        print("number of open files <= m: ", len(open_files))

    # Create an iterator for each file that reads 4 bytes at a time and converts them to integers.
    iterators = []

    for open_file in open_files:
        iterators.append(struct.iter_unpack('i', open_file.read()))
    print("size of all iterators in memory (integers): ", len(iterators))


    # Use a priority queue to merge the integers from the iterators and write them to the output file.
    with open(output_file, 'wb') as f:
        for number in heapq.merge(*iterators):
            f.write(struct.pack('i', number[0]))


    # Close all temporary files.
    for open_file in open_files:
        open_file.close()

    # Cleanup
    for temp_file in temp_files:
        os.remove(temp_file)    


# SOURCES:
# https://www.w3resource.com/python-exercises/heap-queue-algorithm/python-heapq-exercise-11.php
# https://docs.python.org/3/library/struct.html#struct.iter_unpack
# https://fulmicoton.com/posts/lazy/
# https://pieriantraining.com/iterate-over-files-in-directory-using-python/

import itertools
import random
import struct
import heapq
import os
import pstats
from io import StringIO

N = 40000000  # Number of random integers
M = 100000 # In-memory capacity


# Function to generate N random integers and write them to a file
def generate_random_integers(filename, n):
    # 'wb' is for writing in binary mode
    with open(filename, 'wb') as f:
        for _ in range(n):
            # 'i' is for 4-byte signed integer
            # random.randint() returns a random integer N such that a <= N <= b
            # struct.pack converts the number to bytes
            random_num = random.randint(-2**31, 2**31 - 1)
            f.write(struct.pack('i', random_num))



# Function to sort the integers in the input file and write them to the output file using external sort
def external_sort(input_file, output_file, m):
    temp_files = []

    # first pass: read m integers from input file, sort them and write them to a temp file
    # repeat until all integers in the input file have been read
    # Number of files = N/m
    with open(input_file, 'rb') as f:
        # read m integers at a time into a chunk
        chunk = f.read(4*m)
        while chunk:
            # len(chunk) // 4 is the number of integers in the chunk
            # unpacking chunk the number of times that there are integers in the chunk
            numbers = list(struct.unpack('i' * (len(chunk) // 4), chunk))
            numbers.sort()
            # print sorted numbers
            temp_file = f'temp_file_{len(temp_files)}.dat'
            with open(temp_file, 'wb') as temp_f:
                # struct.pack() converts the numbers to bytes
                # *numbers unpacks the numbers list
                temp_f.write(struct.pack('i'*len(numbers), *numbers))
            temp_files.append(temp_file)
            chunk = f.read(4*m)
   
    # remaining passes
    # merge the temp files until there is only one temp file left

    # limiting the temp file to one less than the memory size so that 
    # we always have an output buffer of size >= 1
    temp_file_limit = m - 1

    while len(temp_files) > 1:
        new_temp_files = []

        for i in range(0, len(temp_files), temp_file_limit):
            # chunk_temp_files is a list of temp files of length temp_file_limit
            # except for the last chunk which may be less than temp_file_limit
            chunk_temp_files = temp_files[i:i+temp_file_limit]

            # Open each temp file and create an iterator for each one
            iterators = []
            for temp_file in chunk_temp_files:
                opened_temp_file = open(temp_file, 'rb')
                iterators.append(struct.iter_unpack('i', opened_temp_file.read()))

            new_temp_file = f'temp_file_{len(temp_files)+len(new_temp_files)}.dat'
            # The buffer size is the number of integers that can fit in the remaining memory.
            buffer_size = m - len(iterators)
            
            # Merge the integers from the iterators and write them to the new temp file.
            with open(new_temp_file, 'wb') as f:
                
                while True:
                    next_iterator = heapq.merge(*iterators)
                    buffer = [tup[0] for tup in itertools.islice(next_iterator, buffer_size)]
                    if len(buffer) == 0:
                        break
                    f.write(struct.pack('i'*len(buffer), *buffer))

                buffer = []

            new_temp_files.append(new_temp_file)

            # Close and delete old temp files
            for file in chunk_temp_files:
                os.remove(file)

        temp_files = new_temp_files

    # Rename the last temporary file to the output file
    os.rename(temp_files[0], output_file)



# Function to verify if the numbers in the output file are sorted
def verify_sorted(filename):
    with open(filename, 'rb') as f:
        last_num = None
        for num in struct.iter_unpack('i', f.read()):
            if last_num is not None and last_num > num[0]:
                return False
            last_num = num[0]
    return True



    

if __name__ == '__main__':
    import cProfile
    filename = 'random_numbers.dat'
    sorted_filename = 'sorted_numbers.dat'

    generate_random_integers(filename, N)

    # profile the external sort function
    s = StringIO()
    sortby = 'cumulative'
    pr = cProfile.Profile()
    pr.enable()
    external_sort('random_numbers.dat', 'sorted_numbers.dat', M)
    pr.disable()
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

    print("sorted: ", verify_sorted(sorted_filename))   

    # generate_random_integers('test_numbers.dat', 15)

    # buffer_size = 10
    # with open('new_temp_file', 'wb') as f:
    #     opened_temp_file = open('test_numbers.dat', 'rb')
    #     for _ in range(2):
    #         iterators = []
    #         iterators.append(struct.iter_unpack('i', opened_temp_file.read()))     
    #         print(len(iterators))
    #         # Merge the integers from the iterators and write them to the new temp file.
    #         list_buffer = [tup[0] for tup in list(itertools.islice(heapq.merge(*iterators), buffer_size))]

    #         # buffer = [next(next_iterator)[0] for _ in range(buffer_size) ]
    #         f.write(struct.pack('i'*len(list_buffer), *list_buffer))
    #         buffer = []


    
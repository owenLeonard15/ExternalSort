# tests for main.py
import os
import struct
from src.external_sort import external_sort, generate_random_integers, verify_sorted

# unit tests for generate_random_integers()
def test_generate_random_integers():
    N = 100
    generate_random_integers('test_random_numbers.dat', N)
    with open('test_random_numbers.dat', 'rb') as f:
        assert len(f.read()) == 4*N

    assert verify_sorted('test_random_numbers.dat') == False
    
    os.remove('test_random_numbers.dat')
    
# unit tests for external_sort()
def test_external_sort():
    N = 100
    M = 10

    generate_random_integers('test_random_numbers.dat', N)
    external_sort('test_random_numbers.dat', 'test_sorted_numbers.dat', M)

    assert verify_sorted('test_sorted_numbers.dat') == True

    os.remove('test_random_numbers.dat')
    os.remove('test_sorted_numbers.dat')

# unit tests for verify_sorted()
def test_verify_sorted():
    
    # generate a file with correctly sorted numbers
    sorted_integers = [i for i in range(100)]
    with open('correctly_sorted_numbers.dat', 'wb') as f:
        f.write(struct.pack('i'*len(sorted_integers), *sorted_integers))

    # generate a file with incorrectly sorted numbers
    incorrectly_sorted_integers = [i for i in range(100)]
    incorrectly_sorted_integers[0], incorrectly_sorted_integers[1] = incorrectly_sorted_integers[1], incorrectly_sorted_integers[0]
    with open('incorrectly_sorted_numbers.dat', 'wb') as f:
        f.write(struct.pack('i'*len(incorrectly_sorted_integers), *incorrectly_sorted_integers))

    assert verify_sorted('correctly_sorted_numbers.dat') == True
    assert verify_sorted('incorrectly_sorted_numbers.dat') == False

    os.remove('correctly_sorted_numbers.dat')
    os.remove('incorrectly_sorted_numbers.dat')
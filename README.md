# External Sort
This project contains a program for
* generating a file with N random 4-byte integers
* writing a sorted version of the file with only M integers of in-memory capacity
* reading and verifying the file is sorted

Each of these steps is defined as a function within the [external_sort.py](src/external_sort.py) file. N and M can be modified via the constants at the beginning of the file. The program can be run with the following commands:
* install dependencies:
    - `pip install -r requirements.txt` 
    - OR using pipenv `pipenv install`
* `python src/external_sort.py`

Unit tests for this program are included in [test_external_sort.py](src/test/test_external_sort.py) and can be run via `pytest`

 I've also kept my first attempted solution in [v1_external_sort.py](src/v1_external_sort.py). This solution is not effective for all M, N but was helpful in developing my final solution.

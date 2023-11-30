import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.abspath(os.path.join(current_dir, '../../../'))
sys.path.append(path)
from test_gpt import start_test



if __name__ == "__main__":
    # start_test('balcony')  # success = 1.0
    # start_test('basement')  # success = 0.71
    # start_test('monitoring')  # success = 0.875
    # start_test('garden')  # success = 0.88,
    start_test('elevator')  # success = 0.25,
    # start_test('garage')  # success = 0.64,
    # start_test('modernization')  # success = 0.44
    # start_test('kitchen')  # success = 0.54
    # start_test('technology')  # success = 0.21
    # start_test('lawStatus') # success = 0.63
    # start_test('outbuilding')  # success = 0.5

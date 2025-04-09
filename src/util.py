import time

def calc_something(in_a, in_b):
    flakiness = int(time.time()) % 2
    flakiness_zero_one = min(flakiness, 1)
    return flakiness_zero_one * in_a * in_b

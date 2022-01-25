"""This is a template for multiprocessing.Pool usage.
"""
import time
# import json
# import os
import warnings
from multiprocessing import Pool

###############################################################################
# Setup global variables
INPUT_PATH = ''
OUTPUT_PATH = ''
PROCESSES = 40
PRINT_FREQ = 1000
CNT = 0
###############################################################################
# Setup the global handle to load inputs and save result.
inputs = [i for i in range(100)]  # Usually from INPUT_PATH
results = []

###############################################################################
# Define main function for multiprocessing work.


def func_(input_):
    return input_


###############################################################################
# Define callback function for *Only*-1 process to deal with the output of func


def callback_(output_):
    """
    When each func_ is processed, this function is called to handle the output_
       one by one.
    """
    global results
    global CNT
    global PRINT_FREQ

    CNT += 1

    if CNT % PRINT_FREQ == 0:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              f"Handled {CNT}.")

    results.append(output_)

    if len(results) % (PRINT_FREQ * 5) == 0:
        print(output_)


if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    print(f"===> Start  working with {PROCESSES} processes...")
    pool = Pool(PROCESSES)
    """ Method No.1: if no need for callback."""
    # pool.map_async(func_, inputs, chunksize=PROCESSES, callback=callback_)
    """ Method No.2: if need for callback and load progress bar."""

    for input_ in inputs:
        pool.apply_async(func_, (input_, ), callback=callback_)

    pool.close()
    pool.join()

    # Save results.
    with open(OUTPUT_PATH, 'w') as f_w:
        f_w.writelines(results)  # results is list type.

    print(f"===> Done. Result is saved at '{OUTPUT_PATH}'.")

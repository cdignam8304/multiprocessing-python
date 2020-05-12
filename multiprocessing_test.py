import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import time
import multiprocessing


def oddeven(x):
    if x == 0:
        return 0
    elif x%2 == 0:
        return "Even"
    return "Odd"

def squared(x):
    return x**2

def multiprocessing_func(x):
    y = x**2
    time.sleep(2)
    print(f"{x} squared results in an {oddeven(y)} number.")

if __name__ == "__main__":
    
    # Without multiprocessing
    # -----------------------
    # starttime = time.time()
    # for i in range(10):
    #     print(f"{i} squared results in an {oddeven(squared(i))} number.")
    #     time.sleep(2)
    # endtime = time.time()
    # print(f"That took {endtime-starttime} seconds.")
    # That took 20.02057933807373 seconds.

    
    # With multiprocessing
    # --------------------
    starttime = time.time()
    processes = []
    for i in range(10):
        p = multiprocessing.Process(target=multiprocessing_func, args=(i,))
        processes.append(p)
        p.start()
    
    for process in processes:
        process.join()
    
    endtime = time.time()
    print(f"That took {endtime-starttime} seconds.")
    # That took 2.0890350341796875 seconds.




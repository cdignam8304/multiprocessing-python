import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import time
import multiprocessing
import numpy as np

# Multiprocessing tutorial:
# https://stackoverflow.com/questions/10415028/how-can-i-recover-the-return-value-of-a-function-passed-to-multiprocessing-proce


def func1(x):
    pass

def func2(x):
    pass

def multiprocessing_func(x, send_end):
    x_squared = x**2
    time.sleep(0.1)
    # print(f"{x_squared}")
    send_end.send(x_squared)


if __name__ == "__main__":
    
    # New example with Pandas
    # =======================
    df = pd.DataFrame(np.arange(start=0, stop=1, step=0.01), columns=list("A"))
    # print(df)
    idx_list = list(range(len(df)))
    # print(idx_list)
    
    
    # Without multiprocessing
    # -----------------------
    # result_list = []
    # starttime = time.time()
    # for i in idx_list:
    #     result = df.loc[i]["A"]**2
    #     # print(result)
    #     result_list.append(result)
    #     time.sleep(0.1)
    # print(result_list)
    # print(sum(result_list))
    # endtime = time.time()
    # print(f"That took {endtime-starttime} seconds.")
    # That took 5.051215887069702 seconds.
    # Total: 32.835

    
    # With multiprocessing
    # --------------------
    
    starttime = time.time()
    summary_results = []
    for run in range(3):
        
        print(f"Starting run: {run}")
        
        jobs = []
        pipe_list = []
        for i in idx_list:
            recv_end, send_end = multiprocessing.Pipe(False)
            p = multiprocessing.Process(target=multiprocessing_func, args=(df.loc[i]["A"], send_end))
            jobs.append(p)
            pipe_list.append(recv_end)
            p.start()
        
        for proc in jobs:
            proc.join()
        result_list = [x.recv() for x in pipe_list]
        # print(result_list)
        # summary_results.append(sum(result_list)) # sum of all squared values
        summary_results.append(result_list[42]) # arbitrarily take 10th value to check order
        # print(sum(result_list))
    
    print(summary_results)
    endtime = time.time()
    print(f"That took {endtime-starttime} seconds.")
    # That took 0.6258430480957031 seconds.
    # Total: 32.835




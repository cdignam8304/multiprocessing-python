import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import time
import multiprocessing
import numpy as np

# Multiprocessing tutorial:
# https://stackoverflow.com/questions/10415028/how-can-i-recover-the-return-value-of-a-function-passed-to-multiprocessing-proce


def multiprocessing_func(x, send_end):
    stringlength = len(x)
    # print(f"{stringlength}")
    send_end.send(stringlength)


def without_multi_loop(df, idx_list):
    """Get length of entityname field"""
    start = time.time()
    for i in idx_list:
        df.loc[i]["length"] = len(df.loc[i]["entityname"])
    end = time.time()
    print(f"That took {end-start} seconds.")
    print(df.head())


def without_multi_vectorized(df):
    """Get length of entityname field"""
    start = time.time()
    df["length"] = df["entityname"].apply(lambda x: len(x))
    end = time.time()
    print(f"That took {end-start} seconds.")
    print(df.head())


def with_multi(df):
    """Get length of entityname field"""
    starttime = time.time()
    
    jobs = []
    pipe_list = []
    for i in idx_list:
        recv_end, send_end = multiprocessing.Pipe(False)
        p = multiprocessing.Process(target=multiprocessing_func, args=(df.loc[i]["entityname"], send_end))
        jobs.append(p)
        pipe_list.append(recv_end)
        p.start()
    
    for proc in jobs:
        proc.join()
    result_list = [x.recv() for x in pipe_list]
    endtime = time.time()
    df["length"] = result_list
    
    print(f"That took {endtime-starttime} seconds.")
    print(df.head())
    # # That took 0.6258430480957031 seconds.
    # # Total: 32.835



if __name__ == "__main__":
    
    # New example with Pandas
    # =======================
    file = "./../editdist-dedup-experiment/affiliationstrings/affiliationstrings_ids.csv"
    df = pd.read_csv(file, index_col=0)
    df.columns=["entityname"]
    df["length"] = None
    # print(df.shape)
    # print(df.head())
    # print(df)
    idx_list = list(df.index)
    # print(idx_list)
    
    # without_multi_vectorized(df=df)
    # That took 0.09401822090148926 seconds.
    
    # without_multi_loop(df=df, idx_list=idx_list)
    # That took 0.5792522430419922 seconds.

    with_multi(df=df)
    # That took 12.262673616409302 seconds.





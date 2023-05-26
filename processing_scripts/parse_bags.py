import csv
import pandas as pd
import time
import datetime
import sys
import os
import glob

OFFSET = 0.2

def get_time(t_df, index, should_print=False):
    time_sec = int(t_df['.header.stamp.secs'].iloc[index])
    time_nsec = int(t_df['.header.stamp.nsecs'].iloc[index])* 1e-9
    if should_print:
        print(str(time_sec) + " : " + str(time_nsec))
    return time_sec + time_nsec

if len(sys.argv) != 2:
    print("ERROR EXPECT /path/to/checker/root/dir")
    exit(0)

for sample in glob.glob(sys.argv[1] + "/*/*"):
    checker_path = os.path.join(sample, "checkers")
    df = pd.read_csv(os.path.join(sample, "current_task_status.csv"))
    start_time = get_time(df, 0)
    print(start_time)

    end_time = get_time(df, -1)
    print(end_time)

    duration = end_time - start_time
    duration = duration + OFFSET

    current_task_index = 0
    current_time = 0

    time_intervals = []
    tasks = []
    status_updates = []

    #BUG: If task takes less than interval time
    while current_time < duration:
        next_task_time = get_time(df, current_task_index + 1)


        next_task_time = next_task_time - start_time
        if(current_time > next_task_time):
            current_task_index = current_task_index + 1

        current_task = df['.task'][current_task_index]
        current_status = df['.status'][current_task_index]    

        time_intervals.append(current_time)
        tasks.append(current_task)
        status_updates.append(current_status)

        current_time = current_time + OFFSET


    res_df = pd.DataFrame()
    res_df['time'] = time_intervals
    res_df['task'] = tasks
    res_df['status'] = status_updates


    for checker in os.listdir(checker_path):
        checker_file = os.path.join(checker_path, checker)
        checker_df = pd.read_csv(checker_file)
        checker_name = os.path.basename(checker_file)
        checker_name = os.path.splitext(checker_name)[0]

        i = 0
        column = []

        previous_status = 0
        updated = False
        for time_range in res_df['time']:
            status = 0

            if i < len(checker_df.index):
                checker_time = get_time(checker_df, i)
                checker_time = checker_time - start_time

                while checker_time < res_df['time'][0]:
                    checker_time = get_time(checker_df, i)
                    checker_time = checker_time - start_time

                    i = i + 1            

                while checker_time <= time_range and i < len(checker_df.index):
                    if checker_df['.result'][i] == 1 and status == 0:
                        status = 1
                    elif checker_df['.result'][i] == -1 and status != -1:
                        status = -1
                    checker_time = get_time(checker_df, i)
                    checker_time = checker_time - start_time
                    updated = True
                    

                    i = i + 1

            if status == 0 and previous_status != 0 and i < len(checker_df.index) and not updated:
                column.append(previous_status)
            else:
                column.append(status)
                previous_status = status
                updated = False


        res_df[checker_name] = column

    out_path = os.path.join(sys.argv[1], "data")
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    res_df.to_csv(os.path.join(out_path, os.path.basename(sample)+".csv"))

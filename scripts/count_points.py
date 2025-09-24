# Count points per time unit (minute, 30s, second) for each participant

import pandas as pd
import glob
import csv
import os

file_path = '..\\data\\'
file_params = 'prototype_data\\after1min_'

test_files = glob.glob(file_path + file_params + '*.csv')
output_csv = file_path + 'stats\\points_stats.csv'

results = []

for file in test_files:
    df = pd.read_csv(file)
    participant = file.replace(file_path + file_params, '').replace('.csv', '')
    if 'Timestamp' in df.columns:
        t0 = df['Timestamp'].min()
        tmax = df['Timestamp'].max()
        if tmax - t0 > 10000:
            df['t_sec'] = (df['Timestamp'] - t0) / 1000
        else:
            df['t_sec'] = df['Timestamp'] - t0
        duration = df['t_sec'].max()
    else:
        df['t_sec'] = 0
        duration = 60

    # All minutes
    total_minutes = int(df['t_sec'].max() // 60) + 1
    for m in range(total_minutes):
        df_minute = df[(df['t_sec'] >= m*60) & (df['t_sec'] < (m+1)*60)]
        count = len(df_minute)
        dur = df_minute['t_sec'].max() - df_minute['t_sec'].min() if count > 1 else 0
        points_per_sec = count / dur if dur > 0 else 0
        points_per_30s = points_per_sec * 30
        points_per_min = points_per_sec * 60
        results.append([participant, f"minute_{m+1}", count, dur, points_per_sec, points_per_30s, points_per_min])

    # All 30s windows
    # total_30s = int(df['t_sec'].max() // 30) + 1
    # for s in range(total_30s):
    #     df_30s = df[(df['t_sec'] >= s*30) & (df['t_sec'] < (s+1)*30)]
    #     count = len(df_30s)
    #     dur = df_30s['t_sec'].max() - df_30s['t_sec'].min() if count > 1 else 0
    #     points_per_sec = count / dur if dur > 0 else 0
    #     points_per_30s = points_per_sec * 30
    #     points_per_min = points_per_sec * 60
    #     results.append([participant, f"30s_{s+1}", count, dur, points_per_sec, points_per_30s, points_per_min])

    # All seconds
    # total_sec = int(df['t_sec'].max()) + 1
    # for sec in range(total_sec):
    #     df_sec = df[(df['t_sec'] >= sec) & (df['t_sec'] < sec+1)]
    #     count = len(df_sec)
    #     dur = df_sec['t_sec'].max() - df_sec['t_sec'].min() if count > 1 else 0
    #     points_per_sec = count / dur if dur > 0 else 0
    #     points_per_30s = points_per_sec * 30
    #     points_per_min = points_per_sec * 60
    #     results.append([participant, f"sec_{sec+1}", count, dur, points_per_sec, points_per_30s, points_per_min])

os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['participant', 'window', 'count', 'duration', 'points_per_sec', 'points_per_30s', 'points_per_min'])
    writer.writerows(results)
print(f"\nResults have been saved to {output_csv}")

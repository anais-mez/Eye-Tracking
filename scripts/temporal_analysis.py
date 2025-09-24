import pandas as pd
import numpy as np
import glob
import csv


time_window = 15_000  
num_windows = 4       

file_path = '..\\data\\'
file_params = 'prototype_data\\after1min_'

test_files = glob.glob(file_path + file_params + '*.csv')

results = []


for file in test_files:
    df = pd.read_csv(file)
    participant = file.replace(file_path + file_params, '').replace('.csv', '')
    start_time = df['Timestamp'].min()
    end_time = df['Timestamp'].max()
    duration_sec = int((end_time - start_time) / 1000)

    # All minutes in the file
    total_minutes = int((end_time - start_time) / 60_000) + 1
    for m in range(total_minutes):
        minute_start = start_time + m * 60_000
        minute_end = minute_start + 60_000
        df_minute = df[(df['Timestamp'] >= minute_start) & (df['Timestamp'] < minute_end)]
        n_points = len(df_minute)
        if n_points > 1:
            std_x = df_minute['X'].std()
            std_y = df_minute['Y'].std()
            dx = df_minute['X'].diff()
            dy = df_minute['Y'].diff()
            dt = df_minute['Timestamp'].diff() / 1000.0
            distance = np.sqrt(dx**2 + dy**2)
            speed = distance / dt
            mean_speed = speed[1:].mean()
            results.append([participant, f"minute_{m+1}", n_points, std_x, std_y, mean_speed])
        else:
            results.append([participant, f"minute_{m+1}", n_points, None, None, None])

    # Every 30 seconds
    # for start in range(0, duration_sec+1, 30):
    #     window_start = start_time + start * 1000
    #     window_end = window_start + 30_000
    #     window_df = df[(df['Timestamp'] >= window_start) & (df['Timestamp'] < window_end)]
    #     n_points = len(window_df)
    #     if n_points > 1:
    #         std_x = window_df['X'].std()
    #         std_y = window_df['Y'].std()
    #         dx = window_df['X'].diff()
    #         dy = window_df['Y'].diff()
    #         dt = window_df['Timestamp'].diff() / 1000.0
    #         distance = np.sqrt(dx**2 + dy**2)
    #         speed = distance / dt
    #         mean_speed = speed[1:].mean()
    #         results.append([participant, f"{start}-{start+30}s", n_points, std_x, std_y, mean_speed])
    #     else:
    #         results.append([participant, f"{start}-{start+30}s", n_points, None, None, None])

    # Every second
    # for sec in range(0, duration_sec+1):
    #     window_start = start_time + sec * 1000
    #     window_end = window_start + 1000
    #     window_df = df[(df['Timestamp'] >= window_start) & (df['Timestamp'] < window_end)]
    #     n_points = len(window_df)
    #     if n_points > 1:

    #         std_x = window_df['X'].std()
    #         std_y = window_df['Y'].std()

    #         dx = window_df['X'].diff()
    #         dy = window_df['Y'].diff()
    #         dt = window_df['Timestamp'].diff() / 1000.0
    #         distance = np.sqrt(dx**2 + dy**2)
    #         speed = distance / dt
    #         mean_speed = speed[1:].mean()
    #         results.append([participant, f"{sec}-{sec+1}s", n_points, std_x, std_y, mean_speed])
    #     else:
    #         results.append([participant, f"{sec}-{sec+1}s", n_points, None, None, None])

# Save to CSV
output_csv = file_path + 'stats\\temporal_analysis_stats.csv'
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Participant', 'Window', 'Num_Points', 'Std_X', 'Std_Y', 'Mean_Speed'])
    writer.writerows(results)
print(f"\nTemporal analysis results have been saved in {output_csv}")

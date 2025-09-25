import pandas as pd
import numpy as np
import glob
import csv

file_path = '..\\data\\'
file_params = 'prototype_data\\diff'

test_files = glob.glob(file_path + file_params + '*.csv')

results = []

for file in test_files:
    df = pd.read_csv(file)
    if 'Timestamp' in df.columns:
        t0 = df['Timestamp'].min()
        tmax = df['Timestamp'].max()
        if tmax - t0 > 10000:
            df['t_sec'] = (df['Timestamp'] - t0) / 1000
        else:
            df['t_sec'] = df['Timestamp'] - t0
    else:
        df['t_sec'] = 0

    for participant, group in df.groupby('Participant') if 'Participant' in df.columns else [(file.replace(file_path + file_params, '').replace('.csv', ''), df)]:
        # total_minutes = int(group['t_sec'].max() // 60) + 1
        # for m in range(total_minutes):
        #     df_minute = group[(group['t_sec'] >= m*60) & (group['t_sec'] < (m+1)*60)]
        #     if len(df_minute) > 1:
        #         dx = df_minute['X'].diff()
        #         dy = df_minute['Y'].diff()
        #         dt = df_minute['Timestamp'].diff() / 1000.0
        #         distance = np.sqrt(dx**2 + dy**2)
        #         speed = distance / dt
        #         mean_speed = speed[1:].mean()
        #         results.append([participant, f"minute_{m+1}", m*60, mean_speed])

    # All 30s windows
        total_30s = int(df['t_sec'].max() // 30) + 1
        for s in range(total_30s):
            df_30s = df[(df['t_sec'] >= s*30) & (df['t_sec'] < (s+1)*30)]
            if len(df_30s) > 1:
                dx_30 = df_30s['X'].diff()
                dy_30 = df_30s['Y'].diff()
                dt_30 = df_30s['Timestamp'].diff() / 1000.0
                distance_30 = np.sqrt(dx_30**2 + dy_30**2)
                speed_30 = distance_30 / dt_30
                mean_speed_30 = speed_30[1:].mean()
                results.append([participant, f"30s_{s+1}", s*30, mean_speed_30])

    # All seconds
    # total_sec = int(df['t_sec'].max()) + 1
    # for sec in range(total_sec):
    #     df_sec = df[(df['t_sec'] >= sec) & (df['t_sec'] < sec+1)]
    #     if len(df_sec) > 1:
    #         dx_s = df_sec['X'].diff()
    #         dy_s = df_sec['Y'].diff()
    #         dt_s = df_sec['Timestamp'].diff() / 1000.0
    #         distance_s = np.sqrt(dx_s**2 + dy_s**2)
    #         speed_s = distance_s / dt_s
    #         mean_speed_s = speed_s[1:].mean()
    #         results.append([participant, f"sec_{sec+1}", sec, mean_speed_s])

# Save to CSV
output_csv = file_path + 'stats\\mean_speed_stats-diff.csv'
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Participant', 'Window', 'Start', 'Mean_Speed'])
    writer.writerows(results)
print(f"\nMean speeds have been saved to {output_csv}")

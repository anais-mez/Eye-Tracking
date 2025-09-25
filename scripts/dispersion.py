import pandas as pd
import glob
import csv

file_path = '..\\data\\'
file_params = 'prototype_data\\diff'

test_files = glob.glob(file_path + file_params + '*.csv')

results = []

for file in test_files:
    df = pd.read_csv(file)
    if 'Timestamp' not in df.columns:
        continue
    timestamps = df['Timestamp']
    t0 = timestamps.min()
    tmax = timestamps.max()
    # If timestamps are in ms, convert to seconds
    if tmax - t0 > 10000:
        df['t_sec'] = (df['Timestamp'] - t0) / 1000
    else:
        df['t_sec'] = df['Timestamp'] - t0

    for participant, group in df.groupby('Participant') if 'Participant' in df.columns else [(file.replace(file_path + file_params, '').replace('.csv', ''), df)]:
        # total_minutes = int(group['t_sec'].max() // 60) + 1
        # for m in range(total_minutes):
        #     df_minute = group[(group['t_sec'] >= m*60) & (group['t_sec'] < (m+1)*60)]
        #     if not df_minute.empty:
        #         mean_x = df_minute['X'].mean()
        #         std_x = df_minute['X'].std()
        #         mean_y = df_minute['Y'].mean()
        #         std_y = df_minute['Y'].std()
        #         results.append([participant, f"minute_{m+1}", m*60, mean_x, std_x, mean_y, std_y])

    # All 30s windows
        total_30s = int(df['t_sec'].max() // 30) + 1
        for s in range(total_30s):
            df_30s = df[(df['t_sec'] >= s*30) & (df['t_sec'] < (s+1)*30)]
            if not df_30s.empty:
                mean_x_30 = df_30s['X'].mean()
                std_x_30 = df_30s['X'].std()
                mean_y_30 = df_30s['Y'].mean()
                std_y_30 = df_30s['Y'].std()
                results.append([participant, f"30s_{s+1}", s*30, mean_x_30, std_x_30, mean_y_30, std_y_30])

    # All seconds
    # total_sec = int(df['t_sec'].max()) + 1
    # for sec in range(total_sec):
    #     df_sec = df[(df['t_sec'] >= sec) & (df['t_sec'] < sec+1)]
    #     if not df_sec.empty:
    #         mean_x_s = df_sec['X'].mean()
    #         std_x_s = df_sec['X'].std()
    #         mean_y_s = df_sec['Y'].mean()
    #         std_y_s = df_sec['Y'].std()
    #         results.append([participant, f"sec_{sec+1}", sec, mean_x_s, std_x_s, mean_y_s, std_y_s])

# Save to CSV
output_csv = file_path + 'stats\\dispersion_stats-diff.csv'
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Participant', 'Window', 'Start', 'Mean_X', 'Std_X', 'Mean_Y', 'Std_Y'])
    writer.writerows(results)

print(f"\nResults have been saved to {output_csv}")

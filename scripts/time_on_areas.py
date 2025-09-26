import pandas as pd
import cv2
import os
import glob
import csv
import re

image_file = '../Screenshot.png'
output_csv = '..\\data\\stats\\time_on_areas-1min.csv'

file_path = '..\\data\\'
file_params = 'prototype_data\\all_participants'


df = pd.read_csv(file_path + file_params + '.csv')
df = df.sort_values(['Participant', 'Timestamp'])
df['dt'] = df.groupby('Participant')['Timestamp'].diff()

img = cv2.imread(image_file)
if img is None:
    print(f"Could not load image: {image_file}")
    exit(1)
height, width, _ = img.shape
area1_max_x = width * 0.4222
area2_min_x = width * (1 - 0.5278)

for participant, part_group in df.groupby('Participant'):
    if len(part_group) > 1:
        median_dt = part_group['dt'].iloc[1:].median()
        df.loc[part_group.index[0], 'dt'] = median_dt
    else:
        df.loc[part_group.index[0], 'dt'] = 0


df['t_sec'] = (df['Timestamp'] - df['Timestamp'].min()) / 1000 if df['Timestamp'].max() > 10000 else df['Timestamp'] - df['Timestamp'].min()
total_60s = int(df['t_sec'].max() // 60) + 1
results = []
participants = df['Participant'].unique()
for participant in participants:
    df_part = df[df['Participant'] == participant]
    for s in range(total_60s):
        df_60s = df_part[(df_part['t_sec'] >= s*60) & (df_part['t_sec'] < (s+1)*60)]
        if not df_60s.empty:
            time_area1 = df_60s[df_60s['X'] <= area1_max_x]['dt'].sum()
            time_area2 = df_60s[df_60s['X'] >= area2_min_x]['dt'].sum()
            time_middle = df_60s[(df_60s['X'] > area1_max_x) & (df_60s['X'] < area2_min_x)]['dt'].sum()
            total_time = df_60s['dt'].sum()
            pct_area1 = 100 * time_area1 / total_time if total_time > 0 else 0
            pct_area2 = 100 * time_area2 / total_time if total_time > 0 else 0
            pct_middle = 100 * time_middle / total_time if total_time > 0 else 0
            results.append([participant, f'window_{s+1}', s*60, total_time/1000, pct_area1, pct_area2, pct_middle])


with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Participant', 'Window', 'Start', 'Total_time_s', 'Pct_area1', 'Pct_area2', 'Pct_middle'])
    writer.writerows(results)

print(f"Results saved to {output_csv}")
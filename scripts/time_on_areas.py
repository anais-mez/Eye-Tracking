import pandas as pd
import cv2
import os
import glob
import csv
import re

image_file = '../Screenshot.png'
output_csv = '..\\data\\stats\\time_on_areas-diff.csv'

file_path = '..\\data\\'
file_params = 'prototype_data\\diff'

csv_files = glob.glob(file_path + file_params + '*.csv')

img = cv2.imread(image_file)
if img is None:
    print(f"Could not load image: {image_file}")
    exit(1)
height, width, _ = img.shape

area1_max_x = width * 0.4222
area2_min_x = width * (1 - 0.5278)

results = []

for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    df = df[(df['X'] != 0.0) & (df['Y'] != 0.0)]
    df = df.sort_values('Timestamp')
    df['dt'] = df['Timestamp'].diff().fillna(0)

    for participant, group in df.groupby('Participant'):
        time_area1 = group[group['X'] <= area1_max_x]['dt'].sum()
        time_area2 = group[group['X'] >= area2_min_x]['dt'].sum()
        time_middle = group[(group['X'] > area1_max_x) & (group['X'] < area2_min_x)]['dt'].sum()
        total_time = group['dt'].sum()
        pct_area1 = 100 * time_area1 / total_time if total_time > 0 else 0
        pct_area2 = 100 * time_area2 / total_time if total_time > 0 else 0
        pct_middle = 100 * time_middle / total_time if total_time > 0 else 0
        results.append([participant, total_time/1000, pct_area1, pct_area2, pct_middle])

with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Participant', 'Total_time_s', 'Pct_area1', 'Pct_area2', 'Pct_middle'])
    writer.writerows(results)

    df_results = pd.DataFrame(results, columns=['Participant', 'Total_time_s', 'Pct_area1', 'Pct_area2', 'Pct_middle'])
    mean_all = df_results[['Total_time_s', 'Pct_area1', 'Pct_area2', 'Pct_middle']].mean()
    writer.writerow(['MEAN_ALL', *mean_all])

    for group_name in df_results['Participant'].unique():
        df_group = df_results[df_results['Participant'] == group_name]
        mean_group = df_group[['Total_time_s', 'Pct_area1', 'Pct_area2', 'Pct_middle']].mean()
        writer.writerow([f'MEAN_{group_name.upper()}', *mean_group])

print(f"Results saved to {output_csv}")
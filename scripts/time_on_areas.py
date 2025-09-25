import pandas as pd
import cv2
import os
import glob
import csv
import re

image_file = '../Screenshot.png'
output_csv = '..\\data\\stats\\time_on_areas-diff.csv'

file_path = '..\\data\\'
file_params = 'prototype_data\\all_participants'


# Read the single file containing all participants
df = pd.read_csv(file_path + file_params + '.csv')
df = df.sort_values(['Participant', 'Timestamp'])
df['dt'] = df.groupby('Participant')['Timestamp'].diff()

# Define participant to group mapping
enriched_ids = {'P1', 'P3', 'P5'}
simplified_ids = {'P2', 'P4'}
df['Group'] = df['Participant'].map(lambda x: 'enriched' if x in enriched_ids else ('simplified' if x in simplified_ids else 'other'))


# Restore area boundaries
img = cv2.imread(image_file)
if img is None:
    print(f"Could not load image: {image_file}")
    exit(1)
height, width, _ = img.shape
area1_max_x = width * 0.4222
area2_min_x = width * (1 - 0.5278)

# Fix dt for each participant
for participant, part_group in df.groupby('Participant'):
    if len(part_group) > 1:
        median_dt = part_group['dt'].iloc[1:].median()
        df.loc[part_group.index[0], 'dt'] = median_dt
    else:
        df.loc[part_group.index[0], 'dt'] = 0

# Aggregate by group
results = []
for group_label, group in df.groupby('Group'):
    if group_label not in ['enriched', 'simplified']:
        continue
    time_area1 = group[group['X'] <= area1_max_x]['dt'].sum()
    time_area2 = group[group['X'] >= area2_min_x]['dt'].sum()
    time_middle = group[(group['X'] > area1_max_x) & (group['X'] < area2_min_x)]['dt'].sum()
    total_time = group['dt'].sum()
    pct_area1 = 100 * time_area1 / total_time if total_time > 0 else 0
    pct_area2 = 100 * time_area2 / total_time if total_time > 0 else 0
    pct_middle = 100 * time_middle / total_time if total_time > 0 else 0
    results.append([group_label, total_time/1000, pct_area1, pct_area2, pct_middle])

# Write results to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Group', 'Total_time_s', 'Pct_area1', 'Pct_area2', 'Pct_middle'])
    writer.writerows(results)

    df_results = pd.DataFrame(results, columns=['Group', 'Total_time_s', 'Pct_area1', 'Pct_area2', 'Pct_middle'])
    mean_all = df_results[['Total_time_s', 'Pct_area1', 'Pct_area2', 'Pct_middle']].mean()
    writer.writerow(['MEAN_ALL', *mean_all])

    for group_name in df_results['Group'].unique():
        df_group = df_results[df_results['Group'] == group_name]
        mean_group = df_group[['Total_time_s', 'Pct_area1', 'Pct_area2', 'Pct_middle']].mean()
        writer.writerow([f'MEAN_{group_name.upper()}', *mean_group])

print(f"Results saved to {output_csv}")
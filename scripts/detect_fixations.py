# Count fixations and saccades using a dispersion-based algorithm for each participant

import pandas as pd
import numpy as np
import glob
import csv
import os

MAX_DISTANCE = 50  # Dispersion threshold (pixels)
MIN_DURATION = 100  # Duration threshold (ms)

file_path = '..\\data\\'
file_params = 'prototype_data\\after1min_'

test_files = glob.glob(file_path + file_params + '*.csv')

results = []

def detect_fixations_in_window(df_window):
    fixations = []
    current_fixation = []

    for i in range(len(df_window)):
        point = df_window.iloc[i]
        if len(current_fixation) == 0:
            current_fixation.append(point)
        else:
            current_max_x = max([p['X'] for p in current_fixation])
            current_min_x = min([p['X'] for p in current_fixation])
            current_max_y = max([p['Y'] for p in current_fixation])
            current_min_y = min([p['Y'] for p in current_fixation])

            dispersion_x = current_max_x - current_min_x
            dispersion_y = current_max_y - current_min_y
            dispersion = np.sqrt(dispersion_x ** 2 + dispersion_y ** 2)

            if dispersion <= MAX_DISTANCE:
                current_fixation.append(point)
            else:
                duration = current_fixation[-1]['Timestamp'] - current_fixation[0]['Timestamp']
                if duration >= MIN_DURATION:
                    mean_x = np.mean([p['X'] for p in current_fixation])
                    mean_y = np.mean([p['Y'] for p in current_fixation])
                    fixations.append({
                        'start': current_fixation[0]['Timestamp'],
                        'end': current_fixation[-1]['Timestamp'],
                        'duration': duration,
                        'X': mean_x,
                        'Y': mean_y
                    })
                current_fixation = [point]

    # Check last fixation
    if len(current_fixation) > 1:
        duration = current_fixation[-1]['Timestamp'] - current_fixation[0]['Timestamp']
        if duration >= MIN_DURATION:
            mean_x = np.mean([p['X'] for p in current_fixation])
            mean_y = np.mean([p['Y'] for p in current_fixation])
            fixations.append({
                'start': current_fixation[0]['Timestamp'],
                'end': current_fixation[-1]['Timestamp'],
                'duration': duration,
                'X': mean_x,
                'Y': mean_y
            })
    return fixations

for file in test_files:
    df = pd.read_csv(file)
    df = df[(df['X'] != 0.0) & (df['Y'] != 0.0)]
    participant = file.replace(file_path + file_params, '').replace('.csv', '')
    if 'Timestamp' in df.columns:
        t0 = df['Timestamp'].min()
        tmax = df['Timestamp'].max()
        if tmax - t0 > 10000:
            df['t_sec'] = (df['Timestamp'] - t0) / 1000
        else:
            df['t_sec'] = df['Timestamp'] - t0
    else:
        df['t_sec'] = 0

    # All minutes
    total_minutes = int(df['t_sec'].max() // 60) + 1
    for m in range(total_minutes):
        df_minute = df[(df['t_sec'] >= m*60) & (df['t_sec'] < (m+1)*60)]
        fixations = detect_fixations_in_window(df_minute)
        fixation_durations = [f['duration'] for f in fixations]
        if fixation_durations:
            mean_fixation = sum(fixation_durations) / len(fixation_durations)
            results.append([participant, f"minute_{m+1}", m*60, len(fixations), mean_fixation])
        else:
            results.append([participant, f"minute_{m+1}", m*60, 0, 0])

# Save fixations to CSV
output_csv = os.path.join(file_path, 'stats', 'fixations_stats.csv')
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Participant', 'Window', 'Start', 'Nb_Fixations', 'Mean_Duration_ms'])
    writer.writerows(results)
print(f"\nSaved in {output_csv}")

# --- SACCADES ---
saccades_window_results = []

for file in test_files:
    df = pd.read_csv(file)
    df = df[(df['X'] != 0.0) & (df['Y'] != 0.0)]
    participant = file.replace(file_path + file_params, '').replace('.csv', '')
    if 'Timestamp' in df.columns:
        t0 = df['Timestamp'].min()
        tmax = df['Timestamp'].max()
        if tmax - t0 > 10000:
            df['t_sec'] = (df['Timestamp'] - t0) / 1000
        else:
            df['t_sec'] = df['Timestamp'] - t0
    else:
        df['t_sec'] = 0

    # Par minute
    total_minutes = int(df['t_sec'].max() // 60) + 1
    for m in range(total_minutes):
        df_minute = df[(df['t_sec'] >= m*60) & (df['t_sec'] < (m+1)*60)]
        fixations = detect_fixations_in_window(df_minute)
        nb_saccades = max(0, len(fixations) - 1)
        saccades_window_results.append([participant, f"minute_{m+1}", m*60, nb_saccades])

# Save saccades per window to CSV
output_saccades_window = os.path.join(file_path, 'stats', 'saccades_stats.csv')
os.makedirs(os.path.dirname(output_saccades_window), exist_ok=True)
with open(output_saccades_window, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Participant', 'Window', 'Start', 'Nb_Saccades'])
    writer.writerows(saccades_window_results)
print(f"Saccades per window saved in {output_saccades_window}")
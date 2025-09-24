# Convert txt file into csv file for have x and y values

import csv
import os

def extract_tobii_data(file_path):
    data = []
    base = os.path.basename(file_path)
    participant = base.split('_')[0] if '_' in base else base.split('.')[0]
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("TobiiStream"):
                parts = line.strip().split()
                # parts[0] = 'TobiiStream', parts[1]=timestamp, parts[2]=x, parts[3]=y
                if len(parts) == 4:
                    try:
                        timestamp = float(parts[1])
                        x = float(parts[2])
                        y = float(parts[3])
                        data.append((participant, timestamp, x, y))
                    except Exception as e:
                        print(f"Error parsing in {file_path} : {line.strip()} => {e}")
    return data

def process_all_files(file_names):
    all_data = []
    for file_name in file_names:
        if not os.path.isfile(file_name):
            print(f"File {file_name} does not exist.")
            continue
        data = extract_tobii_data(file_name)
        all_data.extend(data)
    output_csv = os.path.join(os.path.dirname(file_names[0]), 'all_participants.csv')
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Participant', 'Timestamp', 'X', 'Y'])
        csvwriter.writerows(all_data)
    print(f"All data has been written to {output_csv}")

files = [
    'datasets\\P1_OncologyXAI.txt',
    'datasets\\P2_OncologyXAI.txt',
    'datasets\\P3_OncologyXAI.txt',
    'datasets\\P4_OncologyXAI.txt',
    'datasets\\P5_OncologyXAI.txt',
]

process_all_files(files)
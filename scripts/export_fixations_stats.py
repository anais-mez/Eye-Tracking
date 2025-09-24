import pandas as pd
import glob
import os
import sys

# Usage: python export_fixations_stats.py <fixations_csv> [participant]
if len(sys.argv) < 2:
    print('Usage: python export_fixations_stats.py <fixations_csv> [participant]')
    sys.exit(1)

fix_csv = sys.argv[1]
participant = sys.argv[2] if len(sys.argv) > 2 else 'P?'  # Optionnel

# Lecture du fichier de fixations
fix_df = pd.read_csv(fix_csv)
if 'Timestamp' not in fix_df.columns or 'Duration' not in fix_df.columns:
    print('Le fichier doit contenir les colonnes Timestamp et Duration.')
    sys.exit(1)

# Calcul du temps de référence
t0 = fix_df['Timestamp'].min()
fix_df['t_sec'] = (fix_df['Timestamp'] - t0) / 1000

# Ajout de la fenêtre minute
fix_df['minute'] = (fix_df['t_sec'] // 60).astype(int)

results = []
for m, group in fix_df.groupby('minute'):
    start = m * 60
    nb_fix = len(group)
    mean_dur = group['Duration'].mean() if nb_fix > 0 else 0
    results.append([participant, f'minute_{m+1}', start, nb_fix, mean_dur])

output_dir = os.path.join(os.path.dirname(__file__), '../data/', 'stats')
os.makedirs(output_dir, exist_ok=True)
filename = os.path.splitext(os.path.basename(fix_csv))[0]
output_csv = os.path.join(output_dir, f'{filename}_fixations_stats.csv')

with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    f.write('Participant,Window,Start,Nb_Fixations,Mean_Duration_ms\n')
    for row in results:
        f.write(','.join([str(x) for x in row]) + '\n')

print(f"CSV exporté : {output_csv}")

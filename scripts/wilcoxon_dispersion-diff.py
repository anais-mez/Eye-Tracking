import pandas as pd
from scipy.stats import mannwhitneyu
import os

input_csv = '../data/stats/dispersion_stats-diff.csv'
output_csv = '../data/stats/wilcoxon_dispersion-diff.csv'

df = pd.read_csv(input_csv)
groups = ['simplified', 'enriched']
measures = ['Mean_X', 'Std_X', 'Mean_Y', 'Std_Y']

results = []
for measure in measures:
    vals1 = df[df['Participant'] == groups[0]][measure].dropna().values
    vals2 = df[df['Participant'] == groups[1]][measure].dropna().values
    if len(vals1) > 0 and len(vals2) > 0:
        stat, p = mannwhitneyu(vals1, vals2, alternative='two-sided')
    else:
        stat, p = float('nan'), float('nan')
    results.append([measure, stat, p, vals1.mean() if len(vals1) > 0 else float('nan'), vals2.mean() if len(vals2) > 0 else float('nan')])

os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    f.write('Measure,Wilcoxon_statistic,P_value,Mean_simplified,Mean_enriched\n')
    for row in results:
        f.write(','.join([str(x) for x in row]) + '\n')
print(f"Wilcoxon test results exported to {output_csv}")

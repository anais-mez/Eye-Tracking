import pandas as pd
from scipy.stats import mannwhitneyu
import os

input_csv = '../data/stats/mean_speed_stats-diff.csv'
output_csv = '../data/stats/wilcoxon_mean_speed-diff_second.csv'

df = pd.read_csv(input_csv)
groups = ['simplified', 'enriched']
measure = 'Mean_Speed'

vals1 = df[df['Participant'] == groups[0]][measure].dropna().values
vals2 = df[df['Participant'] == groups[1]][measure].dropna().values
if len(vals1) > 0 and len(vals2) > 0:
    stat, p = mannwhitneyu(vals1, vals2, alternative='two-sided')
else:
    stat, p = float('nan'), float('nan')

os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    f.write('Measure,MannWhitneyU_statistic,P_value,Mean_simplified,Mean_enriched\n')
    f.write(f'{measure},{stat},{p},{vals1.mean() if len(vals1) > 0 else float("nan")},{vals2.mean() if len(vals2) > 0 else float("nan")}\n')
print(f"Mann-Whitney U test results exported to {output_csv}")

import pandas as pd
from scipy.stats import ttest_ind
import os

input_csv = '../data/stats/dispersion_stats.csv'
output_csv = '../data/stats/ttest_dispersion.csv'

df = pd.read_csv(input_csv)
measures = ['Mean_X', 'Std_X', 'Mean_Y', 'Std_Y']

# Extract minute number
# Assumes Window column like 'minute_1', 'minute_2', ...
df['minute_num'] = df['Window'].str.extract(r'minute_(\d+)').astype(int)

first_minute = df[df['minute_num'] == df['minute_num'].min()]
last_minute = df[df['minute_num'] == df['minute_num'].max()]

results = []
for measure in measures:
    vals1 = first_minute[measure].dropna()
    vals2 = last_minute[measure].dropna()
    stat, p = ttest_ind(vals1, vals2, nan_policy='omit')
    results.append([measure, stat, p, vals1.mean(), vals2.mean()])

os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    f.write('Measure,T_statistic,P_value,Mean_first_minute,Mean_last_minute\n')
    for row in results:
        f.write(','.join([str(x) for x in row]) + '\n')
print(f"T-test results (first vs last minute) exported to {output_csv}")

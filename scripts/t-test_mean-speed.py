import pandas as pd
from scipy.stats import ttest_ind
import os

input_csv = '../data/stats/mean_speed_stats.csv'
output_csv = '../data/stats/ttest_mean_speed.csv'

df = pd.read_csv(input_csv)
measure = 'Mean_Speed'

df['minute_num'] = df['Window'].str.extract(r'minute_(\d+)').astype(int)

first_minute = df[df['minute_num'] == df['minute_num'].min()]
last_minute = df[df['minute_num'] == df['minute_num'].max()]

vals1 = first_minute[measure].dropna()
vals2 = last_minute[measure].dropna()
stat, p = ttest_ind(vals1, vals2, nan_policy='omit')

os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    f.write('Measure,T_statistic,P_value,Mean_first_minute,Mean_last_minute\n')
    f.write(f'{measure},{stat},{p},{vals1.mean()},{vals2.mean()}\n')
print(f"T-test results (first vs last minute) exported to {output_csv}")

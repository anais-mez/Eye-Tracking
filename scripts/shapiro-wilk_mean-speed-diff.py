import pandas as pd
from scipy.stats import shapiro
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

input_csv_speed = '../data/stats/mean_speed_stats-diff.csv'
output_csv_speed = '../data/stats/shapiro_mean_speed-diff.csv'

df_speed = pd.read_csv(input_csv_speed)

def safe_shapiro(data):
    if len(data) < 3:
        return float('nan'), float('nan')
    stat, p = shapiro(data)
    return stat, p

def which_test(p):
    return "t-test" if p > 0.05 else "wilcoxon"

os.makedirs(os.path.dirname(output_csv_speed), exist_ok=True)
with open(output_csv_speed, 'w', newline='', encoding='utf-8') as f:
    f.write('Group,Shapiro_stat,Shapiro_p,Mean,SD,Test_to_use\n')
    for group_name, group in df_speed.groupby('Participant'):
        vals = group['Mean_Speed'].dropna()
        stat, p = safe_shapiro(vals)
        mean = vals.mean()
        std = vals.std()
        test = which_test(p)
        f.write(f'{group_name},{stat},{p},{mean},{std},{test}\n')

print(f"Grouped Shapiro-Wilk results saved to {output_csv_speed}")
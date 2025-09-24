import pandas as pd
from scipy.stats import shapiro
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

input_csv_speed = '../data/stats/mean_speed_stats-diff.csv'
output_csv_speed = '../data/stats/shapiro_mean_speed-diff.csv'

df_speed = pd.read_csv(input_csv_speed)
df_speed['minute_num'] = df_speed['Window'].str.extract(r'minute_(\d+)').astype(int)

first_mean_speed = []
last_mean_speed = []

for participant, group in df_speed.groupby('Participant'):
    group = group.sort_values('minute_num')
    first_row = group.iloc[0]
    last_row = group.iloc[-1]
    first_mean_speed.append(first_row['Mean_Speed'])
    last_mean_speed.append(last_row['Mean_Speed'])

def safe_shapiro(data):
    if len(data) < 3:
        return float('nan'), float('nan')
    stat, p = shapiro(data)
    return stat, p

def which_test(p_value):
    return "t-test" if p_value > 0.05 else "wilcoxon"

shap_first_speed_stat, shap_first_speed_p = safe_shapiro(first_mean_speed)
shap_last_speed_stat, shap_last_speed_p = safe_shapiro(last_mean_speed)

os.makedirs(os.path.dirname(output_csv_speed), exist_ok=True)
with open(output_csv_speed, 'w', newline='', encoding='utf-8') as f:
    f.write('Group,Shapiro_stat,Shapiro_p,Mean,SD,Test_to_use\n')
    f.write(f'First_minute_MeanSpeed,{shap_first_speed_stat},{shap_first_speed_p},{pd.Series(first_mean_speed).mean()},{pd.Series(first_mean_speed).std()},{which_test(shap_first_speed_p)}\n')
    f.write(f'Last_minute_MeanSpeed,{shap_last_speed_stat},{shap_last_speed_p},{pd.Series(last_mean_speed).mean()},{pd.Series(last_mean_speed).std()},{which_test(shap_last_speed_p)}\n')

print(f"Grouped Shapiro-Wilk results saved to {output_csv_speed}")

input_csv = '../data/stats/mean_speed_stats.csv'
output_csv = '../data/stats/shapiro_mean_speed_groups.csv'

df = pd.read_csv(input_csv)

groups = ['simplified', 'enriched']
measure = 'Mean_Speed'

results = []

vals1 = df[df['Participant'] == groups[0]][measure].dropna()
vals2 = df[df['Participant'] == groups[1]][measure].dropna()
shap1_stat, shap1_p = safe_shapiro(vals1)
shap2_stat, shap2_p = safe_shapiro(vals2)
test_type = which_test(shap1_p, shap2_p)
results.append([measure, shap1_stat, shap1_p, shap2_stat, shap2_p, test_type, vals1.mean(), vals2.mean()])

os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    f.write('Measure,Shapiro_stat_simplified,Shapiro_p_simplified,Shapiro_stat_enriched,Shapiro_p_enriched,Test_to_use,Mean_simplified,Mean_enriched\n')
    for row in results:
        f.write(','.join([str(x) for x in row]) + '\n')
print(f"Shapiro-Wilk groupes exported in {output_csv}")
import pandas as pd
from scipy.stats import shapiro
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

input_csv = '../data/stats/fixations_stats.csv'
output_csv = '../data/stats/shapiro_fixations.csv'

df = pd.read_csv(input_csv)
df = df[df['Nb_Fixations'] > 0]

df['minute_num'] = df['Window'].str.extract(r'minute_(\d+)').astype(int)

first_minute_fix = []
last_minute_fix = []
first_minute_dur = []
last_minute_dur = []

for participant, group in df.groupby('Participant'):
    group = group.sort_values('minute_num')
    first_row = group.iloc[0]
    last_row = group.iloc[-1]
    first_minute_fix.append(first_row['Nb_Fixations'])
    last_minute_fix.append(last_row['Nb_Fixations'])
    first_minute_dur.append(first_row['Mean_Duration_ms'])
    last_minute_dur.append(last_row['Mean_Duration_ms'])

def safe_shapiro(data):
    if len(data) < 3:
        return float('nan'), float('nan')
    stat, p = shapiro(data)
    return stat, p

shap_first_fix_stat, shap_first_fix_p = safe_shapiro(first_minute_fix)
shap_last_fix_stat, shap_last_fix_p = safe_shapiro(last_minute_fix)
shap_first_dur_stat, shap_first_dur_p = safe_shapiro(first_minute_dur)
shap_last_dur_stat, shap_last_dur_p = safe_shapiro(last_minute_dur)

def which_test(p_value):
    return "t-test" if p_value > 0.05 else "wilcoxon"

os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    f.write('Group,Shapiro_stat,Shapiro_p,Mean,SD,Test_to_use\n')
    f.write(f'First_minute_NbFix,{shap_first_fix_stat},{shap_first_fix_p},{pd.Series(first_minute_fix).mean()},{pd.Series(first_minute_fix).std()},{which_test(shap_first_fix_p)}\n')
    f.write(f'Last_minute_NbFix,{shap_last_fix_stat},{shap_last_fix_p},{pd.Series(last_minute_fix).mean()},{pd.Series(last_minute_fix).std()},{which_test(shap_last_fix_p)}\n')
    f.write(f'First_minute_MeanDur,{shap_first_dur_stat},{shap_first_dur_p},{pd.Series(first_minute_dur).mean()},{pd.Series(first_minute_dur).std()},{which_test(shap_first_dur_p)}\n')
    f.write(f'Last_minute_MeanDur,{shap_last_dur_stat},{shap_last_dur_p},{pd.Series(last_minute_dur).mean()},{pd.Series(last_minute_dur).std()},{which_test(shap_last_dur_p)}\n')

print(f"Grouped Shapiro-Wilk results saved to {output_csv}")

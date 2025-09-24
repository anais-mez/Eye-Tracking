import pandas as pd
import os
from scipy.stats import shapiro
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

input_csv = '../data/stats/saccades_stats.csv'
output_csv = '../data/stats/shapiro_saccades.csv'

df = pd.read_csv(input_csv)
df = df[df['Nb_Saccades'] > 0]

df['minute_num'] = df['Window'].str.extract(r'minute_(\d+)').astype(int)

first_minute_saccades = []
last_minute_saccades = []

for participant, group in df.groupby('Participant'):
    group = group.sort_values('minute_num')
    first_row = group.iloc[0]
    last_row = group.iloc[-1]
    first_minute_saccades.append(first_row['Nb_Saccades'])
    last_minute_saccades.append(last_row['Nb_Saccades'])

def safe_shapiro(data):
    if len(data) < 3:
        return float('nan'), float('nan')
    stat, p = shapiro(data)
    return stat, p

shap_first_stat, shap_first_p = safe_shapiro(first_minute_saccades)
shap_last_stat, shap_last_p = safe_shapiro(last_minute_saccades)

def which_test(p_value):
    return "t-test" if p_value > 0.05 else "wilcoxon"

os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    f.write('Group,Shapiro_stat,Shapiro_p,Mean,SD,Test_to_use\n')
    f.write(f'First_minute,{shap_first_stat},{shap_first_p},{pd.Series(first_minute_saccades).mean()},{pd.Series(first_minute_saccades).std()},{which_test(shap_first_p)}\n')
    f.write(f'Last_minute,{shap_last_stat},{shap_last_p},{pd.Series(last_minute_saccades).mean()},{pd.Series(last_minute_saccades).std()},{which_test(shap_last_p)}\n')

print(f"Grouped Shapiro-Wilk results saved to {output_csv}")
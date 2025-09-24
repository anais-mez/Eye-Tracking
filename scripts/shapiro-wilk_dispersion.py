import pandas as pd
from scipy.stats import shapiro
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

input_csv = '../data/stats/dispersion_stats.csv'
output_csv = '../data/stats/shapiro_dispersion.csv'

df = pd.read_csv(input_csv)

df['minute_num'] = df['Window'].str.extract(r'minute_(\d+)').astype(int)


disp_df = pd.read_csv(input_csv)

disp_df['minute_num'] = disp_df['Window'].str.extract(r'minute_(\d+)').astype(int)

first_mean_x = []
last_mean_x = []
first_std_x = []
last_std_x = []
first_mean_y = []
last_mean_y = []
first_std_y = []
last_std_y = []

for participant, group in disp_df.groupby('Participant'):
    group = group.sort_values('minute_num')
    
    first_row = group.iloc[0]
    last_row = group.iloc[-1]
    
    first_mean_x.append(first_row['Mean_X'])
    last_mean_x.append(last_row['Mean_X'])
    
    first_std_x.append(first_row['Std_X'])
    last_std_x.append(last_row['Std_X'])
    
    first_mean_y.append(first_row['Mean_Y'])
    last_mean_y.append(last_row['Mean_Y'])
    
    first_std_y.append(first_row['Std_Y'])
    last_std_y.append(last_row['Std_Y'])
    
def safe_shapiro(data):
    if len(data) < 3:
        return float('nan'), float('nan')
    stat, p = shapiro(data)
    return stat, p

def which_test(p_value):
    return "t-test" if p_value > 0.05 else "wilcoxon"

shap_first_mean_x_stat, shap_first_mean_x_p = safe_shapiro(first_mean_x)
shap_last_mean_x_stat, shap_last_mean_x_p = safe_shapiro(last_mean_x)

shap_first_std_x_stat, shap_first_std_x_p = safe_shapiro(first_std_x)
shap_last_std_x_stat, shap_last_std_x_p = safe_shapiro(last_std_x)

shap_first_mean_y_stat, shap_first_mean_y_p = safe_shapiro(first_mean_y)
shap_last_mean_y_stat, shap_last_mean_y_p = safe_shapiro(last_mean_y)

shap_first_std_y_stat, shap_first_std_y_p = safe_shapiro(first_std_y)
shap_last_std_y_stat, shap_last_std_y_p = safe_shapiro(last_std_y)

os.makedirs(os.path.dirname(output_csv), exist_ok=True)
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    f.write('Group,Shapiro_stat,Shapiro_p,Mean,SD,Test_to_use\n')
    f.write(f'First_minute_Mean_X,{shap_first_mean_x_stat},{shap_first_mean_x_p},{pd.Series(first_mean_x).mean()},{pd.Series(first_mean_x).std()},{which_test(shap_first_mean_x_p)}\n')
    f.write(f'Last_minute_Mean_X,{shap_last_mean_x_stat},{shap_last_mean_x_p},{pd.Series(last_mean_x).mean()},{pd.Series(last_mean_x).std()},{which_test(shap_last_mean_x_p)}\n')
    f.write(f'First_minute_Std_X,{shap_first_std_x_stat},{shap_first_std_x_p},{pd.Series(first_std_x).mean()},{pd.Series(first_std_x).std()},{which_test(shap_first_std_x_p)}\n')
    f.write(f'Last_minute_Std_X,{shap_last_std_x_stat},{shap_last_std_x_p},{pd.Series(last_std_x).mean()},{pd.Series(last_std_x).std()},{which_test(shap_last_std_x_p)}\n')
    f.write(f'First_minute_Mean_Y,{shap_first_mean_y_stat},{shap_first_mean_y_p},{pd.Series(first_mean_y).mean()},{pd.Series(first_mean_y).std()},{which_test(shap_first_mean_y_p)}\n')
    f.write(f'Last_minute_Mean_Y,{shap_last_mean_y_stat},{shap_last_mean_y_p},{pd.Series(last_mean_y).mean()},{pd.Series(last_mean_y).std()},{which_test(shap_last_mean_y_p)}\n')
    f.write(f'First_minute_Std_Y,{shap_first_std_y_stat},{shap_first_std_y_p},{pd.Series(first_std_y).mean()},{pd.Series(first_std_y).std()},{which_test(shap_first_std_y_p)}\n')
    f.write(f'Last_minute_Std_Y,{shap_last_std_y_stat},{shap_last_std_y_p},{pd.Series(last_std_y).mean()},{pd.Series(last_std_y).std()},{which_test(shap_last_std_y_p)}\n')

print(f"Shapiro-Wilk pour les dispersions ajouté à {output_csv}")
import pandas as pd
from scipy.stats import shapiro
import os

input_csv = '../data/stats/dispersion_stats-diff.csv'
output_csv = '../data/stats/shapiro_dispersion-diff.csv'

df = pd.read_csv(input_csv)

groups = ['simplified', 'enriched']
measures = ['Mean_X', 'Std_X', 'Mean_Y', 'Std_Y']

results = []

def safe_shapiro(data):
    if len(data) < 3:
        return float('nan'), float('nan')
    stat, p = shapiro(data)
    return stat, p

def which_test(p1, p2):
    return "t-test" if p1 > 0.05 and p2 > 0.05 else "wilcoxon"

for measure in measures:
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
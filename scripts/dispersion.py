import pandas as pd
import numpy as np

def compute_dispersion(std_x, std_y):
    return np.sqrt(std_x**2 + std_y**2)


df = pd.read_csv('../data/prototype_data/diff.csv')
if 'Participant' not in df.columns:
    raise ValueError('The column Participant is missing in diff.csv')

participants_enriched = ['P1', 'P3', 'P5']
participants_simplified = ['P2', 'P4']
def get_group(participant):
    if participant in participants_enriched:
        return 'enriched'
    elif participant in participants_simplified:
        return 'simplified'
    else:
        return participant  

if not set(df['Participant'].unique()).issubset({'enriched', 'simplified'}):
    df['Participant'] = df['Participant'].apply(get_group)
else:
    df['Participant'] = df['Participant']

if df['Timestamp'].max() > 10000:
    df['t_sec'] = (df['Timestamp'] - df['Timestamp'].min()) / 1000
else:
    df['t_sec'] = df['Timestamp'] - df['Timestamp'].min()

results = []

for participant, group_df in df.groupby('Participant'):
    total_30s = int(group_df['t_sec'].max() // 30) + 1
    for s in range(total_30s):
        df_30s = group_df[(group_df['t_sec'] >= s*30) & (group_df['t_sec'] < (s+1)*30)]
        if not df_30s.empty:
            mean_x_30 = df_30s['X'].mean()
            std_x_30 = df_30s['X'].std()
            mean_y_30 = df_30s['Y'].mean()
            std_y_30 = df_30s['Y'].std()
            dispersion_30 = compute_dispersion(std_x_30, std_y_30)
            results.append({
                'Participant': participant,
                'Window': f'30s_{s+1}',
                'Start': s*30,
                'Mean_X': mean_x_30,
                'Std_X': std_x_30,
                'Mean_Y': mean_y_30,
                'Std_Y': std_y_30,
                'Dispersion': dispersion_30
            })

results_df = pd.DataFrame(results)
mean_dispersion = results_df.groupby('Participant')['Dispersion'].mean()
print('Mean Dispersion by Participant:')
print(mean_dispersion)
results_df.to_csv('../data/stats/dispersion_stats-diff.csv', index=False)
print('\nSaved in ../data/stats/dispersion_stats-diff.csv')

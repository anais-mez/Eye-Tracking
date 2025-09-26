
import pandas as pd
import numpy as np

df = pd.read_csv('../data/prototype_data/diff.csv')
if 'Participant' not in df.columns:
	raise ValueError('The column Participant is missing in diff.csv')

if df['Timestamp'].max() > 10000:
	df['t_sec'] = (df['Timestamp'] - df['Timestamp'].min()) / 1000
else:
	df['t_sec'] = df['Timestamp'] - df['Timestamp'].min()

results = []
for participant, group_df in df.groupby('Participant'):
	total_30s = int(group_df['t_sec'].max() // 30) + 1
	for s in range(total_30s):
		df_30s = group_df[(group_df['t_sec'] >= s*30) & (group_df['t_sec'] < (s+1)*30)]
		if len(df_30s) > 1:
			dx = df_30s['X'].diff()
			dy = df_30s['Y'].diff()
			dt = df_30s['t_sec'].diff()
			speed = np.sqrt(dx**2 + dy**2) / dt
			mean_speed = speed[1:].mean()  
			results.append({
				'Participant': participant,
				'Window': f'30s_{s+1}',
				'Start': s*30,
				'Mean_Speed': mean_speed
			})

results_df = pd.DataFrame(results)
print(results_df)
results_df.to_csv('../data/stats/mean_speed_stats-diff.csv', index=False)
print('\nSaved in ../data/stats/mean_speed_stats-diff.csv')

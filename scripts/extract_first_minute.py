# --- Extract the first minute of data for each participant from the merged CSV file
import pandas as pd

df = pd.read_csv('..\\datasets\\all_participants.csv')

groups = df.groupby('Participant')
for participant, group in groups:
    start_time = group['Timestamp'].min()
    mask = group['Timestamp'] <= (start_time + 60000)  
    test0 = group[mask]
    test0.to_csv(f'..\\data\\first_minute\\test0_{participant}.csv', index=False)

# --- Remove the first minute of data for each participant and save to separate files

# def remove_first_minute_to_files(df):
#     groups = df.groupby('Participant')
#     for participant, group in groups:
#         start_time = group['Timestamp'].min()
#         mask = group['Timestamp'] > (start_time + 60000)
#         rest = group[mask]
#         output_path = f'..\\data\\prototype_data\\after1min_{participant}.csv'
#         rest.to_csv(output_path, index=False)
#     print('First minute removed and saved to one file per participant in prototype_data/')

# remove_first_minute_to_files(df)


# --- Extract all data after the first minute for each participant and save to a single CSV file

# import pandas as pd

# df = pd.read_csv('data\\all_participants.csv')

# groups = df.groupby('Participant')
# after_first_minute = []

# for participant, group in groups:
#     start_time = group['Timestamp'].min()
#     mask = group['Timestamp'] > (start_time + 60000)
#     rest = group[mask]
#     after_first_minute.append(rest)

# Concatenate all participants' data after the first minute
# result_df = pd.concat(after_first_minute, ignore_index=True)
# output_path = 'data\\prototype_data\\all_participants.csv'
# result_df.to_csv(output_path, index=False)
# print(f'All data after the first minute saved to {output_path}')
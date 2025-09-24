import pandas as pd
import sys
import os

# Usage: python test.py <input_csv1> <input_csv2> <output_csv>
if len(sys.argv) < 4:
    print('Usage: python test.py <input_csv1> <input_csv2> <output_csv>')
    sys.exit(1)

input_csv1 = sys.argv[1]
input_csv2 = sys.argv[2]
output_csv = sys.argv[3]

df1 = pd.read_csv(input_csv1)
df2 = pd.read_csv(input_csv2)

# Fusionne les deux DataFrames
merged_df = pd.concat([df1, df2], ignore_index=True)
merged_df.to_csv(output_csv, index=False)
print(f"File exported : {output_csv}")


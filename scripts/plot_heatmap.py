import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import sys
import os

BACKGROUND_IMG = os.path.join(os.path.dirname(__file__), '..', 'Screenshot.png')

if len(sys.argv) < 2:
    print('Usage: python plot_heatmap.py <csv_file1>')
    sys.exit(1)

csv_file1 = sys.argv[1]
df = pd.read_csv(csv_file1)
img = cv2.imread(BACKGROUND_IMG)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

output_dir = os.path.join(os.path.dirname(__file__), '../data/', 'heatmaps', 'P3')
os.makedirs(output_dir, exist_ok=True)

# --- For each minute, plot heatmap ---

# t0 = df['Timestamp'].min()
# tmax = df['Timestamp'].max()
# if tmax - t0 > 10000:  
#     df['t_sec'] = (df['Timestamp'] - t0) / 1000
# else:  
#     df['t_sec'] = df['Timestamp'] - t0
# total_minutes = int(df['t_sec'].max() // 60) + 1

# for m in range(total_minutes):
#     df_minute = df[(df['t_sec'] >= m*60) & (df['t_sec'] < (m+1)*60)]
#     if df_minute.empty:
#         continue
#     fig, ax = plt.subplots(figsize=(10, 8))
#     ax.imshow(img)
#     sns.kdeplot(
#         x=df_minute['X'], y=df_minute['Y'],
#         cmap='spring', fill=True, alpha=0.4, thresh=0.05, levels=100, ax=ax
#     )
#     ax.set_title(f'Gaze Heatmap - Minute {m+1}')
#     ax.axis('off')
#     plt.tight_layout()
#     filename = os.path.splitext(os.path.basename(csv_file1))[0]
#     plt.savefig(os.path.join(output_dir, f'{filename}_minute_{m+1}.png'))
#     plt.close(fig)

# print(f"Heatmaps exported to {output_dir}")


# --- For all timestamps ---

if not df.empty:
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(img)
    sns.kdeplot(
        x=df['X'], y=df['Y'],
        cmap='spring', fill=True, alpha=0.4, thresh=0.05, levels=100, ax=ax
    )
    ax.set_title('Gaze Heatmap - P3')
    ax.axis('off')
    plt.tight_layout()
    
    filename = os.path.splitext(os.path.basename(csv_file1))[0]
    plt.savefig(os.path.join(output_dir, f'heatmap_P3.png'))
    plt.close(fig)
    
    print(f"Heatmap saved in {output_dir}")

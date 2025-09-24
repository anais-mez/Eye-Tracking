import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2
import sys
import os

# Usage: python plot_trajectories.py <csv_file> [participant]
# Example: python plot_trajectories.py ../data/first_minute/test0_P1.csv

BACKGROUND_IMG = os.path.join(os.path.dirname(__file__), '..', 'Screenshot.png')
WINDOW_SIZE = 10  

if len(sys.argv) < 2:
    print('Usage: python plot_trajectories.py <csv_file> [participant]')
    sys.exit(1)

csv_file = sys.argv[1]
participant = sys.argv[2] if len(sys.argv) > 2 else None

df = pd.read_csv(csv_file)
if participant and 'Participant' in df.columns:
    df = df[df['Participant'] == participant]

img = cv2.imread(BACKGROUND_IMG)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

fig, ax = plt.subplots(figsize=(10, 8))
ax.imshow(img)
ax.set_title('Gaze Trajectory (sliding window)')
ax.axis('off')

line, = ax.plot([], [], color='lime', linewidth=2, marker='o', markersize=6)

def init():
    line.set_data([], [])
    return line,

def update(i):
    start = max(0, i - WINDOW_SIZE + 1)
    x = df['X'].iloc[start:i+1]
    y = df['Y'].iloc[start:i+1]
    line.set_data(x, y)
    return line,

ani = animation.FuncAnimation(
    fig, update, frames=len(df), init_func=init, blit=True, interval=60, repeat=False
)

plt.tight_layout()
plt.show()

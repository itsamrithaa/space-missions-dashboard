import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Read mission launches as data frame
df = pd.read_csv("Project-Template/data/raw/mission_launches.csv")

# Rocket Status vs Mission Status - heatmap
pivot_heatmap = pd.crosstab(df['Rocket_Status'], df['Mission_Status'])
plt.figure(figsize=(8, 6))
sns.heatmap(pivot_heatmap, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Rocket Status vs Mission Status")
plt.ylabel("Rocket Status")
plt.xlabel("Mission Status")
plt.tight_layout()
plt.savefig('Project-Template/data/status.png', dpi=300, bbox_inches='tight')
plt.show()





import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64
from dash import html

# Read mission launches as data frame
df = pd.read_csv("Project-Template/data/raw/mission_launches.csv")

# Mission Frequency by Location - bar chart
location_counts = df['Location'].value_counts().head(20)  # Top 20 locations for readability
plt.figure(figsize=(10, 6))
sns.barplot(x=location_counts.values, y=location_counts.index,
            hue=location_counts.index, palette="viridis", legend=False)
plt.title("Top 20 Mission Frequencies by Launch Location")
plt.xlabel("Number of Missions")
plt.ylabel("Launch Location")
plt.tight_layout()
plt.savefig('Project-Template/data/location_data.png', dpi=300, bbox_inches='tight')

plt.show()





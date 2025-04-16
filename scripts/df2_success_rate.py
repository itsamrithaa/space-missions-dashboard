from tqdm import tqdm
import requests
import pandas as pd
import time
import folium
import matplotlib.pyplot as plt
import seaborn as sns



# Read mission launches as data frame
df = pd.read_csv("Project-Template/data/raw/mission_launches.csv")


# Count mission outcomes per organization
mission_counts = df.groupby(['Organisation', 'Mission_Status']).size().unstack(fill_value=0)

# Select top 20 organisations by total number of missions
top_10_orgs = mission_counts.sum(axis=1).sort_values(ascending=False).head(10).index
top_10_data = mission_counts.loc[top_10_orgs]

# Plot
top_10_data.plot(kind='bar', stacked=True, figsize=(14, 6))
plt.title('Top 20 Organisations: Mission Success vs Failure')
plt.xlabel('Organisation')
plt.ylabel('Number of Missions')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Mission Status')
plt.tight_layout()
plt.savefig('Project-Template/data/success_rate.png', dpi=300, bbox_inches='tight')
plt.show()
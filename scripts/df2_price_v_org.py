from tqdm import tqdm
import requests
import pandas as pd
import time
import folium
import matplotlib.pyplot as plt
import seaborn as sns



# Read mission launches as data frame
df = pd.read_csv("Project-Template/data/raw/mission_launches.csv")

# Convert launch date to datetime with UTC
df['Date'] = pd.to_datetime(df['Date'],format = "mixed")

# Convert 'Price' column to numeric, coercing errors to NaN
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Drop missing values
df_clean = df.dropna(subset=['Price', 'Date'])
top_orgs = df_clean['Organisation'].value_counts().nlargest(5).index
filtered = df_clean[df_clean['Organisation'].isin(top_orgs)]

plt.figure(figsize=(12, 6))
sns.violinplot(data=filtered, x='Organisation', y='Price')
plt.title('Launch Price Distribution by Top 5 Organisations')
plt.ylabel('Price (in million USD)')
plt.tight_layout()
plt.savefig('Project-Template/data/price_vs_org.png', dpi=300, bbox_inches='tight')
plt.show()
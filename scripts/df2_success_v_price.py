import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Read mission launches as data frame
df = pd.read_csv("Project-Template/data/raw/mission_launches.csv")

# Convert launch date to datetime
df['Date'] = pd.to_datetime(df['Date'], format="mixed")

# Convert 'Price' column to numeric, coercing errors to NaN
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Drop rows where 'Price' is NaN
df_clean = df.dropna(subset=['Price'])

# Drop missing values
df_clean = df.dropna(subset=['Price', 'Mission_Status'])

# Create the plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='Mission_Status', y='Price', data=df_clean)

plt.title('Launch Price Distribution by Mission Status')
plt.ylabel('Launch Price (in millions USD)')
plt.xlabel('Mission Status')
plt.tight_layout()
plt.savefig('Project-Template/data/success_vs_price.png', dpi=300, bbox_inches='tight')
plt.show()
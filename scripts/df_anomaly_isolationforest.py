import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns

# Load df
df = pd.read_csv("Project-Template/data/raw/spacex_df.csv")

# Extract features for anomaly detection
features = ['mass_kg', 'average_temp', 'average_wind_speed', 'average_humidity']
df_filtered = df[features].dropna() # Filter out invalid data points

# create Isolation Forest
iso_forest = IsolationForest(contamination=0.10, random_state=42)
df_filtered['anomaly'] = iso_forest.fit_predict(df_filtered)

# labels
df['anomaly'] = 1  # Default to normal
df.loc[df_filtered.index, 'anomaly'] = df_filtered['anomaly']

# Filter anomalies and compare to failures
df_anomalies = df[(df['anomaly'] == -1)][[
    'mission_name', 'date_utc', 'mass_kg', 'orbit',
    'average_temp', 'average_wind_speed', 'average_humidity', 'success'
]]


with open("Project-Template/data/output.html", "w") as f:

    f.write("<h2>Anomalous Launches</h2>")
    f.write(df_anomalies.to_html(index=False))

# Visualize and save
sns.pairplot(df_filtered, hue='anomaly', diag_kind='kde', palette={1: "green", -1: "red"})
plt.suptitle("Anomaly Detection with Isolation Forest", y=1.02)
plt.savefig('Project-Template/data/anomaly_plot.png', dpi=300, bbox_inches='tight')
plt.show()



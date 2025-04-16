import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Load df
df = pd.read_csv("Project-Template/data/raw/spacex_df.csv")

# Select features for clustering
features = ['mass_kg', 'average_temp', 'average_wind_speed', 'average_humidity']
df_clustering = df[features].dropna()

# Normalize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df_clustering)

# Apply K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
df_clustering['cluster'] = kmeans.fit_predict(scaled_features)

# Add clusters back to original df
df['cluster'] = -1  # default
df.loc[df_clustering.index, 'cluster'] = df_clustering['cluster']

# Visualize clusters using mass and temperature
plt.figure(figsize=(8, 6))
scatter = plt.scatter(df_clustering['mass_kg'], df_clustering['average_temp'], 
                      c=df_clustering['cluster'], cmap='viridis')
plt.xlabel("Payload Mass (kg)")
plt.ylabel("Average Temperature (°C)")
plt.title("K-Means Clustering of SpaceX Launches")
plt.colorbar(scatter, label='Cluster')
plt.grid(True)
plt.savefig("Project-Template/data/kmeans_clusters.png", dpi=300)
plt.show()

# Save clustered data
df.to_csv("Project-Template/data/spacex_clustered.csv", index=False)

# Assuming df already has the 'cluster' and 'success' columns

# Group by cluster and calculate counts
cluster_summary = df.groupby('cluster')['success'].value_counts(normalize=True).unstack()

# Print success rate per cluster
print("Success Rate by Cluster:")
print(cluster_summary)

cluster_summary.plot(kind='bar', stacked=True, colormap='viridis')
plt.title('Success Rate by Cluster')
plt.xlabel('Cluster')
plt.ylabel('Proportion')
plt.legend(title='Success')
plt.tight_layout()
plt.show()

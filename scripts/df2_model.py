import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE





# Read mission launches as data frame
df = pd.read_csv("Project-Template/data/raw/mission_launches.csv")



# Prepare data
df_model = df.copy()

# Clean the Price column
df_model['Price'] = df_model['Price'].astype(str).str.replace(',', '')
df_model['Price'] = pd.to_numeric(df_model['Price'], errors='coerce')

# Drop rows with missing values in key columns
df_model = df_model.dropna(subset=['Organisation', 'Rocket_Status', 'Price', 'Mission_Status'])

# Encode target variable
df_model['Mission_Status'] = df_model['Mission_Status'].apply(lambda x: 1 if x == 'Success' else 0)

# Encode categorical variables
label_cols = ['Organisation', 'Rocket_Status']
for col in label_cols:
    df_model[col] = LabelEncoder().fit_transform(df_model[col])

# Features and target
X = df_model[['Organisation', 'Rocket_Status', 'Price']]
y = df_model['Mission_Status']

# Split your original dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Apply SMOTE
sm = SMOTE(random_state=42)
X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

# Train Random Forest
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train_res, y_train_res)

# Predict and evaluate
y_pred = rf_model.predict(X_test)
print(classification_report(y_test, y_pred))
with open("Project-Template/data/classification_report.txt", "w") as f:
    f.write(classification_report(y_test, y_pred))
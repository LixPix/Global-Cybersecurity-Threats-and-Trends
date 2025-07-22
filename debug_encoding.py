import pandas as pd
from sklearn.preprocessing import LabelEncoder

# load data
df = pd.read_csv("clean_global_cybersecurity_threats.csv")
print("Original columns:")
print(df.columns.tolist())
print("\nString columns:")
print(df.select_dtypes(include='object').columns.tolist())

# encode data
df.fillna(method='ffill', inplace=True)

label_encoders = {}
for col in df.select_dtypes(include='object').columns:
    le = LabelEncoder()
    df[col + '_encoded'] = le.fit_transform(df[col])
    label_encoders[col] = le
    print(f"\nEncoded {col} -> {col}_encoded")
    print(f"Sample values: {df[col].unique()[:5]}")
    print(f"Encoded values: {df[col + '_encoded'].unique()[:5]}")

print("\nAll columns after encoding:")
print(df.columns.tolist())

print("\nFeature columns for ML:")
feature_cols = [
    'Country_encoded', 'Year', 'Attack Source_encoded', 
    'Security Vulnerability Type_encoded', 'Defense Mechanism Used_encoded',
    'Number of Affected Users', 'Incident Resolution Time (in Hours)'
]

for col in feature_cols:
    if col in df.columns:
        print(f"{col}: {df[col].dtype} - Sample: {df[col].iloc[0]}")
    else:
        print(f"MISSING: {col}")

print("\nTesting feature selection:")
try:
    features = df[feature_cols]
    print("Features shape:", features.shape)
    print("Features dtypes:")
    print(features.dtypes)
    print("Any string values in features:")
    for col in features.columns:
        if features[col].dtype == 'object':
            print(f"  {col}: {features[col].unique()[:5]}")
except Exception as e:
    print("Error selecting features:", e)

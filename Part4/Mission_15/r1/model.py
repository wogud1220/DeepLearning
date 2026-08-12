import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import numpy as np
import os


df = pd.read_csv("./mission15_train.csv")

# label encoding
df['Extracurricular Activities'] = df['Extracurricular Activities'].map({
    'Yes': 1,
    'No': 0
})

X = df[['Hours Studied', 'Previous Scores',
        'Extracurricular Activities',
        'Sleep Hours',
        'Sample Question Papers Practiced']]
y = df['Performance Index']

# split 8:2
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# standardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LinearRegression()
model.fit(X_train_scaled, y_train)

pred = model.predict(X_test_scaled)
rmse = np.sqrt(mean_squared_error(y_test, pred))
print(f"RMSE: {rmse:.4f}")
# 2.0103

OUTPUT_DIR = os.getenv("OUTPUT_DIR", './output')
os.makedirs(OUTPUT_DIR, exist_ok=True)
# /app/output

# test.csv도 같이 복사해서 저장
df_test = pd.read_csv("./mission15_test.csv")
df_test.to_csv(f"{OUTPUT_DIR}/mission15_test.csv", index=False)

with open(f"{OUTPUT_DIR}/model.pkl", "wb") as f:
    pickle.dump({
        "model": model,
        "scaler": scaler
    }, f)

print("model.pkl 저장 완료")
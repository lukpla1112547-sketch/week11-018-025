import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. โหลดข้อมูล Dataset (ปรับชื่อไฟล์ CSV ให้ตรงกับที่มีในเครื่อง)
df = pd.read_csv('train.csv')

# 2. จัดการข้อมูลเบื้องต้น (Clean Data)
# ลบคอลัมน์ที่ไม่จำเป็นออก
df = df.drop(columns=['Unnamed: 0', 'id'], errors='ignore')

# เติมค่าที่หายไป (Missing Values)
df['Arrival Delay in Minutes'] = df['Arrival Delay in Minutes'].fillna(df['Arrival Delay in Minutes'].median())

# แปลงข้อมูลตัวอักษร (Categorical) ให้เป็นตัวเลข
le = LabelEncoder()
categorical_cols = ['Gender', 'Customer Type', 'Type of Travel', 'Class', 'satisfaction']
for col in categorical_cols:
    if col in df.columns:
        df[col] = le.fit_transform(df[col])

# 3. แยก Features (X) และ Target (y)
X = df.drop(columns=['satisfaction'])
y = df['satisfaction']

# 4. สร้างและเทรนโมเดล
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 5. เซฟโมเดลเป็นไฟล์ .joblib
joblib.dump(model, 'airline_model.joblib')
print("เทรนและบันทึกโมเดลเรียบร้อยแล้ว: airline_model.joblib")
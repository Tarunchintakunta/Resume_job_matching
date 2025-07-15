import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load labeled data (CSV with features and match_score)
df = pd.read_csv('data/labeled_pairs.csv')
X = df.drop(['resume_id', 'job_id', 'match_score', 'predicted_score'], axis=1)
y = df['match_score']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, 'models/match_model.pkl')
print('Model trained and saved to models/match_model.pkl') 
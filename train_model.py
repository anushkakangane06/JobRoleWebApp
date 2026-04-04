import pandas as pd
import joblib
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("dataset/resume.csv")

print(df["Category"].value_counts())

# Check column names
print(df.columns)

# Usually Kaggle dataset columns are:
# Resume_str (resume text)
# Category (job role)

X = df["Resume_str"]
y = df["Category"]


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    return text

df["Resume_str"] = df["Resume_str"].apply(clean_text)
# TF-IDF Vectorizer (NLP)
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=10000,
    ngram_range=(1,2)
)

X_vectorized = vectorizer.fit_transform(X)

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model.pkl")

# Save vectorizer
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model trained successfully!")
print("✅ model.pkl and vectorizer.pkl created")

print("Model Accuracy:", model.score(X_test, y_test))
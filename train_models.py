import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.svm import LinearSVC
import pickle

# Load dataset
df = pd.read_csv('data/AI_Human.csv')

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(df['text'], df['generated'], test_size=0.2)

# Model pipelines
pipeMNB = Pipeline([('tfidf', TfidfVectorizer(stop_words='english')), ('clf', MultinomialNB())])
pipeCNB = Pipeline([('tfidf', TfidfVectorizer(stop_words='english')), ('clf', ComplementNB())])
pipeSVC = Pipeline([('tfidf', TfidfVectorizer(stop_words='english')), ('clf', LinearSVC())])

# Train models
pipeMNB.fit(x_train, y_train)
pipeCNB.fit(x_train, y_train)
pipeSVC.fit(x_train, y_train)

# Save models
model_dir = "models/"
pickle.dump(pipeMNB, open(f"{model_dir}/mnb_model.pkl", "wb"))
pickle.dump(pipeCNB, open(f"{model_dir}/cnb_model.pkl", "wb"))
pickle.dump(pipeSVC, open(f"{model_dir}/svc_model.pkl", "wb"))

print("✅ Models trained and saved successfully!")


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import pickle

data = pd.read_csv("dataset.csv")
data = data.iloc[:, 1:]

X = data['text']
y = data['emotions']

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2,
                                                    random_state=12,
                                                    stratify=data['emotions'])

vectorizer = TfidfVectorizer( max_df= 0.9).fit(X_train)
X_train = vectorizer.transform(X_train)
X_test = vectorizer.transform(X_test)
print(X_train.shape)

encoder = LabelEncoder().fit(y_train)
y_train = encoder.transform(y_train)
y_test = encoder.transform(y_test)

model = LogisticRegression(C=.1, class_weight='balanced')
model.fit(X_train, y_train)

file = open('model.pkl', 'wb')
pickle.dump(model, file)
file.close()

file = open('vectorizer.pkl', 'wb')
pickle.dump(vectorizer, file)
file.close()



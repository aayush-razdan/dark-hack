from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import pandas as pd
import math
from collections import Counter
import nltk
import pickle

## required nltk packages

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')


DETECTION_THRESHOLD = 0.03

lemmatizer = WordNetLemmatizer()
vectorizer = CountVectorizer(max_features=1500)
classifier = MultinomialNB(alpha=0.01)

def porn_score(text):
    data = re.sub('[^\w\s]', '', text)
    data = data.lower()
    data = word_tokenize(data)
    data = [lemmatizer.lemmatize(word) for word in data if word not in set(stopwords.words('english'))]

    """## Classification Pornography"""

    df_train=pd.read_csv('porn.csv')

    training_vectors = vectorizer.fit_transform(df_train.Contents)
    classifier.fit(training_vectors, df_train.Labels)

    test_vectors = vectorizer.transform(data)

    predict = classifier.predict(test_vectors)

    ratio = float(format((sum(predict)/len(predict)), ".2f"))

    detected = ratio >= DETECTION_THRESHOLD
    print("\nRatio:", ratio)
    print("Detected", detected)
    return str(ratio)

# def load_model():
#     global vectorizer
#     global classifier
#     vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
#     classifier = pickle.load(open('classifier.pkl', 'rb'))
# def save_model():
#     pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))
#     pickle.dump(classifier, open('classifier.pkl', 'wb'))
    
def drug_score():
    data = re.sub('[^\w\s]', '', text)
    data = data.lower()
    data = word_tokenize(data)
    data = [lemmatizer.lemmatize(word) for word in data if word not in set(stopwords.words('english'))]
    df_train=pd.read_csv('drugs.csv')
    training_vectors = vectorizer.fit_transform(df_train.text)
    classifier.fit(training_vectors, df_train.category)
    test_vectors = vectorizer.transform(data)
    predict = classifier.predict(test_vectors)

    ratio = float(format((sum(predict)/len(predict)), ".2f"))

    detected = ratio >= DETECTION_THRESHOLD
    print("\nRatio:", ratio)
    print("Detected", detected)
    return str(ratio)
    
if __name__ == "__main__":
    print("Loading model...")

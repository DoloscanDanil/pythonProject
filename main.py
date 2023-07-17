import pandas as pd
import numpy as np
import os
import re
import nltk

from sklearn import feature_extraction, model_selection, naive_bayes, pipeline, manifold, preprocessing, feature_selection
from sklearn.linear_model import LogisticRegressionCV
from sklearn import metrics, utils
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pickle
import sqlite3 as sq

from .feature_engineering import process_data, create_embeddings

MODEL_PATH = "models/n1p"
MODEL_EMBEDDINGS_PATH = os.path.join(MODEL_PATH, 'similarity_embeddings')
CUISINE_CLASSES = ['brazilian', 'british', 'cajun_creole', 'chinese', 'filipino', 'french', 'greek', 'indian', 'irish', 'italian', 'jamaican', 'japanese', 'korean', 'mexican', 'moroccan', 'russian', 'southern_us', 'spanish', 'thai', 'vietnamese']
os.makedirs(MODEL_PATH, exist_ok=True)
os.makedirs(MODEL_EMBEDDINGS_PATH, exist_ok=True)

# Save to file in the current working directory
def save_pkl(file, pkl_filename):
    with open(pkl_filename, 'wb') as pkl_file:
        pickle.dump(file, pkl_file)

def compute_performances(predicted, predicted_prob, y_test):
    classes = np.unique(y_test)
    y_test_array = pd.get_dummies(y_test, drop_first=False).values

    accuracy = metrics.accuracy_score(y_test, predicted)
    balance_accuracy = metrics.balanced_accuracy_score(y_test, predicted)
    auc = metrics.roc_auc_score(y_test, predicted_prob, multi_class="ovr")

    print("Balanced Accuracy:", round(balance_accuracy, 2))
    print("Accuracy:", round(accuracy, 2))
    print("Auc:", round(auc, 2))
    print("Detail:")
    print(metrics.classification_report(y_test, predicted))

def create_model_cuisine_predictions():
    dataset = process_data()

    # Create embeddings
    vectorizer = feature_extraction.text.TfidfVectorizer()  # create_embeddings(dataset)

    classifier = LogisticRegressionCV(
        cv=3,
        random_state=42,
        max_iter=300,
        n_jobs=-1,
        verbose=1
    )

    # pipeline
    model = pipeline.Pipeline([("vectorizer", vectorizer), ("classifier", classifier)])

    # Split the dataset
    X_train, X_test, y_train, y_test = model_selection.train_test_split(dataset['ingredients_query'], dataset['cuisine'], test_size=0.3, random_state=42)

    # train classifier
    model.fit(X_train, y_train)

    # test
    predicted = model.predict(X_test)
    predicted_prob = model.predict_proba(X_test)

    # Compute performance of the model
    compute_performances(predicted, predicted_prob, y_test)

    # Save model and vectorizer to disk
    save_pkl(model, os.path.join(MODEL_PATH, "pickle_model.pkl"))

def d2v_embeddings(data):
    data = data['ingredients_query'].tolist()
    tagged_data = [TaggedDocument(words=row.split(), tags=[str(index)]) for index, row in enumerate(data)]

    max_epochs = 20
    vec_size = 50
    alpha = 0.025

    model_embedding = Doc2Vec(vector_size=vec_size, alpha=alpha, min_alpha=0.00025, min_count=1, dm=1)

    model_embedding.build_vocab(tagged_data)

    for epoch in range(max_epochs):
        print('iteration {}'.format(epoch))
        model_embedding.train(tagged_data, total_examples=model_embedding.corpus_count, epochs=model_embedding.epochs)
        # decrease the learning rate
        model_embedding.alpha -= 0.0002
        # fix the learning rate, no decay
        model_embedding.min_alpha = model_embedding.alpha

    return model_embedding

def train_model_embeddings():
    db = sq.connect('recipes.db')
    cursor = db.cursor()

    for cuisine in CUISINE_CLASSES:
        sql_query = "SELECT title, instructions, ingredients, ingredients_query " \
                    "FROM main_recipes WHERE cuisine = ?"
        data = pd.read_sql(sql_query, db, params=(cuisine,))

        model_embedding = d2v_embeddings(data)
        save_pkl(model_embedding, os.path.join(MODEL_EMBEDDINGS_PATH, f'd2v_{cuisine}.pkl'))

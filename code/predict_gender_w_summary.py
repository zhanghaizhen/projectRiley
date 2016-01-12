from __future__ import division, print_function
import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, roc_curve, auc
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
import re
from nltk.corpus import stopwords
import sys

stopwords = set(stopwords.words('english'))
# Functions
def missing(df):
    if df.summary == 'missing' or df.num_tokens == 0:
        return 1
    else:
        return 0


def lenx(mystr):
    return len(mystr.split())


def avgchrs(mytokens):
    tw = len(mytokens)
    num_chars = 0
    for word in mytokens:
        num_chars += len(word)
    return num_chars/tw


def remove_digits(mystr):
    '''
    INPUT: list of tokens
    OUTPUT: list of tokens with digits removed
    '''
    return [word for word in mystr if not word.isdigit()]


stemmer = SnowballStemmer("english")
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tokenize(text):
    tokens = word_tokenize(text)
    row = remove_digits(tokens)
    stems = stem_tokens(row, stemmer)
    return stems


def tokenize_no_stem(text):
    tokens = word_tokenize(text)
    row = remove_digits(tokens)
    stems = stem_tokens(row, stemmer)
    return tokens


def preprocess_df(df):
    # Feature Engineering before running the prediction code
    df['class'] = np.ones(len(df))
    df['class'] = df['gender_forced'].apply(lambda x: 0 if x == 'female' else 1)

    df['summ_tokens'] = df['summary'].apply(lambda x: nltk.word_tokenize(str(x)))
    df['num_tokens'] = df['summ_tokens'].apply(lambda x: len(x))

    # Add feature for missing summary
    df['summ_missing'] = df.apply(missing, axis = 1)

    # Only include rows with summaries
    df = df[df['summ_missing'] == 0]

    # Some Nan rows refuse to go without this
    df = df[pd.notnull(df['summary'])]

    print ("Length of DF after removing rows with missing Summaries:\n")
    print (len(df))

    df['avg_len'] = df['summ_tokens'].apply(lambda x: avgchrs(x))

    # lexical diversity = number of unique tokens / total number of tokens
    df['lex_diversity'] = df['summ_tokens'].apply(lambda x: len(set(x))/len(x))

    return df


def model_predict(df, model):
# Train-test split

    X_train, X_test, y_train, y_test = train_test_split(df['summary'], df['class'], test_size=0.3, random_state=0)
    vectorizer = CountVectorizer(analyzer = 'word', tokenizer = tokenize, ngram_range=(1,4), stop_words = stopwords, max_df = 0.7, min_df = 5, max_features = 5000)
    train_fit = vectorizer.fit_transform(X_train)
    train_fit = train_fit.toarray()
    feature_names = vectorizer.get_feature_names()

    print ("Training the model...")

    model = model.fit(train_fit, y_train)

    # Testing
    # Get a bag of words for the test set, and convert to a numpy array
    test_features = vectorizer.transform(X_test)
    test_features = test_features.toarray()

    # Use the random forest to make sentiment label predictions
    yhat = model.predict(test_features)
    probX = model.predict_proba(test_features)

    print "Done! Accuracy Metrics below:\n"
    print ("Precision Score/Positive Predictive Value/TP|TP+FP: {:.2%}".format(precision_score(y_test, yhat)))
    print ("Recall Score/Sensitivity/TPR/TP|P: {:.2%}".format(recall_score(y_test, yhat)))
    print ("AUC Score: {:.2%}".format(roc_auc_score(y_test, yhat)))
    print ("Model Score:Accuracy: TP+TN|P+N: {:.2%}".format(model.score(test_features, y_test)))

    fpr, tpr, thresholds = roc_curve(y_test, probX[:,1])

    return model


def main():
    '''
    Predicts the gender, given an input file in the format that is at: /Users/lekha/galvanize/capstone/projectRiley/data/withindgroup/all2.txt
    '''
    infile = sys.argv[1]
    df = pd.read_csv(infile, sep="|")
    df = preprocess_df(df)
    model = RandomForestClassifier(n_estimators = 100)
    model = model_predict(df, model)


if __name__ == '__main__':
    error_message = "Usage: python predict_gender_w_summary.py <input_file>\n"
    if len(sys.argv) != 2:
        print (error_message)
        exit()
    main()

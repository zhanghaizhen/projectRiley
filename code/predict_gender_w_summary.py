from __future__ import division
from __future__ import print_function
import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, roc_curve, auc
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import *
from nltk import word_tokenize
import re


def stopwords():
    stopwords = ['10','100','1000','100000','11','12','13',\
    '14','15','150','16','17','18','19','1983',\
    '1986','1990','1991','1992','1993','1994',\
    '1995','1996','1997','1998','1999','1st',\
    '20','200','2000','2001','2002','2003','2004',\
    '2005','2006','2007','2008','2009','2010','2011',\
    '2012','2013','2014','2015','2016','21','22',\
    '23','24','25','250','26','27','2d','2nd','30',\
    '300','35','360','365','3d','3rd','40','400',\
    '45','4th','50','500','5000','60','70','75',\
    '80','90','ab','abc', 'an', 'the', 'and', \
    'of', 'in', 'to', 'for', 'with', 'my', 'as', \
    'on','at', 'have', 'is', 'am', 'has', 'have', \
    'that', 'from', 'was', 'by', 'it', 'also', 'or',\
     'who', 'you', 'can','their', 'i', 'a']
    return stopwords


stemmer = SnowballStemmer("english")
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tokenize(text):
    tokens = word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems


def tokenize_no_stem(text):
    tokens = word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return tokens


def missing_to_binary(x):
    if x == 'missing':
        return 1
    else:
        return 0


# add feature for num of words in the summary
def lenx(mystr):
    return len(mystr.split())


def rf_countv(X_train, X_test, y_train, y_test):
    print ("Creating bag of words, CountVectorizer...\n")
    countv = CountVectorizer(analyzer = "word",   \
                             tokenizer = tokenize,    \
                             preprocessor = None, \
                             stop_words = stopwords,   \
                             max_features = 5000)

    train_cv = countv.fit_transform(X_train)
    train_cv = train_cv.toarray()
    feature_names = countv.get_feature_names()
    print ("Training the random forest...")

    # Initialize a Random Forest classifier with 100 trees and train
    forest = RandomForestClassifier(n_estimators = 100)
    forest = forest.fit(train_cv, y_train)

    # Testing
    # Get a bag of words for the test set, and convert to a numpy array
    test_data_features = countv.transform(X_test)
    test_data_features = test_data_features.toarray()
    yhat = forest.predict(test_data_features)
    probX = forest.predict_proba(test_data_features)

    print ("Precision Score: {0}".format(precision_score(y_test, yhat)))
    print ("Recall Score: {0}".format(recall_score(y_test, yhat)))
    print ("AUC Score: {0}".format(roc_auc_score(y_test, yhat)))
    print ("Model Score:{0}".format(forest.score(test_data_features, y_test)))

    fpr, tpr, thresholds = roc_curve(y_test, probX[:,1])
    return yhat, probX


def rf_tfidf(X_train, X_test, y_train, y_test):
    print ("Creating bag of words, tfidf...\n")
    tfidf = TfidfVectorizer(analyzer = 'word', \
                    tokenizer = tokenize, \
                    stop_words = stopwords, \
                    max_features = 5000)

    train_tfidf = tfidf.fit_transform(X_train)
    train_tfidf = train_tfidf.toarray()
    feature_names = tfidf.get_feature_names()
    print ("Training the random forest...")

    # Initialize a Random Forest classifier with 100 trees and train
    forest = RandomForestClassifier(n_estimators = 100)
    forest = forest.fit(train_tfidf, y_train)

    # Testing
    # Get a bag of words for the test set, and convert to a numpy array
    test_data_features = tfidf.transform(X_test)
    test_data_features = test_data_features.toarray()
    yhat = forest.predict(test_data_features)
    probX = forest.predict_proba(test_data_features)

    print ("Precision Score: {0}".format(precision_score(y_test, yhat)))
    print ("Recall Score: {0}".format(recall_score(y_test, yhat)))
    print ("AUC Score: {0}".format(roc_auc_score(y_test, yhat)))
    print ("Model Score:{0}".format(forest.score(test_data_features, y_test)))

    fpr, tpr, thresholds = roc_curve(y_test, probX[:,1])
    return yhat, probX


def plot_roc_curve(fpr, tpr, label):
    # ROC Curve
    plt.plot(np.array(range(101))/100, np.array(range(101))/100, '--', color='black')
    plt.plot(fpr, tpr, label=label)
    plt.ylabel("True Positive Rate ")
    plt.xlabel("False Positive Rate")
    plt.title("ROC plot")
    plt.legend(loc='lower right')
    plt.show()


def main(input_file):
    '''
    INPUT:
    Text File for training and testing. Example file in ../data/cleandatagender1000.txt. This is the output of the predict_name function which includes the gender and has cleaned up the summary.
    Format of the Input file:
    0|full_name|html|summary|counter|first_name|gender
    counter is set to a default of 1.
    OUTPUT:
    - Prints the accuracy metrics for the test data set
    - Returns the predicted genders for the test set and the probabilities
    '''

    stopwords = stopwords()
    df = pd.read_csv(input_file, sep="|")
    df = df[['full_name', 'html','summary', 'first_name', 'gender', 'counter']]

    # In the notebook, there is a bunch of pre-processing for first_names that are really "nan". Keeping it simple for this. There were only 3 rows in the dataset with first_names that were "nan"
    df.dropna(axis=0, inplace=True)

    df_all['class'] = np.ones(len(df_all))
    df_all['class'] = df_all['gender'].apply(lambda x: 0 if x == 'female' else 1)

    # Add feature for missing summary
    df_all['summ_missing'] = df_all['summary'].apply(lambda x: missing_to_binary(x))

    df_all['summ_words'] = df_all['summary'].apply(lambda x: lenx(str(x)))

    # For each row, return the total count of first_names that are the same and create a column
    counts = df_all.groupby('first_name').size()
    counts.name = 'name_counts'
    df_all = df_all.set_index('first_name').join(counts).reset_index()

    df2 = df_all.query('summ_missing == 0')

    # setting the type to str, since RF breaks without this
    df2['summary'] = df2['summary'].astype(str)

    # Train and Test set
    X_train, X_test, y_train, y_test = train_test_split(df2['summary'], df2['class'], test_size=0.3, random_state=0)

    yhat_tf, probX_tf = rf_tfidf(X_train, X_test, y_train, y_test)

    yhat_cv, probX_cv = rf_countv(X_train, X_test, y_train, y_test)

if __name__ = '__main__':
    error_message = "Usage: python predict_gender.py <input_file>\n"
    if len(sys.argv) != 2:
        print error_message
        exit()
    main()

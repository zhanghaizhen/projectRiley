import nltk


def gender_classifier(first_name):
    # 7944 labeled names from nltk corpus
    labeled_names = ([(name, 'male') for name in names.words('male.txt')] +[(name, 'female') for name in names.words('female.txt')])

    # nltk's NaiveBayesClassifier takes featuresets to train that is a tuple of (features_dict, label)
    featuresets_train = [(gender_features(name), gender) for (name, gender) in labeled_names]
    classifier = nltk.NaiveBayesClassifier.train(featuresets_train)

    # get the features of the set to be classified
    name_features = gender_features(first_name)
    gender = classifier.classify(name_features)
    return gender


def main():
    # read in classifier model that is stored as a pickle file
    input_file = '/Users/lekha/galvanize/capstone/projectRiley/code/gender.pkl'
    with open(input_file, 'r') as f:
        gender_classifier = pickle.load(f)


if __name__=='__main__':
    main()

df['gender'] = df['first_name'].apply(lambda x: gender_classifier(x))

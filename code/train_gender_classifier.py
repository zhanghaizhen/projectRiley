import nltk
from nltk.corpus import names
import cPickle as pickle

def gender_features(word):
    '''
    Returns the following features given a word:
    - name
    - last letter
    - last 2 letters
    - boolean if last letter is vowel
    '''
    return {'name': word, 'last_letter': word[-1], 'last_2_letters': word[-2:], 'last_is_vowel': (word[-1] in 'aeiou')}


def gender_train():
    # 7944 labeled names from nltk corpus
    labeled_names = ([(name, 'male') for name in names.words('male.txt')] +[(name, 'female') for name in names.words('female.txt')])

    # nltk's NaiveBayesClassifier takes featuresets to train that is a tuple of (features_dict, label)
    featuresets_train = [(gender_features(name), gender) for (name, gender) in labeled_names]
    classifier = nltk.NaiveBayesClassifier.train(featuresets_train)

    return classifier


def main():
    out_file = '/Users/lekha/galvanize/capstone/projectRiley/code/gender.pkl'
    classifier = gender_train()
    with open('gender.pkl', 'w') as f:
        pickle.dump(classifier, f)


if __name__=='__main__':
    main()

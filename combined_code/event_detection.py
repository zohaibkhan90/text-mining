# Importing essential libraries
import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split, KFold
from sklearn import metrics
from sklearn.metrics import precision_score, recall_score
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
from collections import Counter
import matplotlib.pyplot as plt
import re

#Import Classifiers
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
import string



def lemmatize(word):
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word=word)

def stem(word):
    porter_stemmer = PorterStemmer()
    return porter_stemmer.stem(word=word)

def finalClean(tweet):
    #Convert to lower case
    tweet = tweet.lower()

    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)

    #Strip tweet
    tweet = tweet.strip('\'"')
    
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", tweet)

def pre():
    # Reading training and test files to list data structures
    data = pd.read_csv("../events_corpus.csv", sep = ",", index_col=False, encoding='latin-1', low_memory=False)
    df_old = DataFrame(data)

    # Take those datasets in which text is not null
    df = df_old[df_old['text'].notnull()]

    labelCount = df.groupby(df['event']).count()
    print(labelCount)

    # Replaces URLs (http/www) 
    x = df['text'].str.replace('http\S+|www.\S+', '', case=False)

    # Changes types in events column to string
    y = df['event'].astype(str)

    # Replaces words with special characters
    x = x.str.replace('[^a-zA-Z0-9-_.]', ' ')

    printable = set(string.printable)
    filter(lambda q: q in printable, x)

    # Lemmatize words
    x_lemma = [" ".join([lemmatize(word) for word in sentence.split(" ")]) for sentence in x]

    # x_stem = [" ".join([stem(word) for word in sentence.split(" ")]) for sentence in x_lemma]

    # Clean data per word
    x_clean = [finalClean(sentence) for sentence in x_lemma]
    #temp_df = [filter(lambda i: i not in string.punctuation,sentence) for sentence in x_clean]
    return x_clean, y

def labelEncoding(y):
    labelEncoder = LabelEncoder()
    y_encoded = labelEncoder.fit_transform(y)
    y_encoded
    return y_encoded

def countVectorizer(x):
    stopset = set(stopwords.words('English'))
    vect = CountVectorizer(analyzer='char_wb', encoding='utf-8', min_df = 0, ngram_range=(2, 2), lowercase = True, strip_accents='ascii', stop_words = stopset)
    X_vec = vect.fit_transform(x)
    return X_vec

def tfidfVectorizer(x):
    stopset = set(stopwords.words('English'))
    vect = TfidfVectorizer(analyzer='word', encoding='utf-8', min_df = 0, ngram_range=(1, 1), lowercase = True, strip_accents='ascii', stop_words = stopset)
    X_vec = vect.fit_transform(x)
    return X_vec

def splitTestTrain(X_vec, y_encoded):
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y_encoded, 
													test_size=0.2, random_state=0, shuffle=True)
    return X_train, X_test, y_train, y_test

def kFold(X_vec, y_encoded):
    kf = KFold(n_splits=2, random_state=None, shuffle=False)
    for train_index, test_index in kf.split(X_vec):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X_vec[train_index], X_vec[test_index]
        y_train, y_test = y_encoded[train_index], y_encoded[test_index]
        return X_train, X_test, y_train, y_test
    
def plotPreRec(naiveBayesRecall, naiveBayesPrecision, svmRecall, svmPrecision, randomForestRecall, randomForestPrecision, logisticRegressionRecall, logisticRegressionPrecision, sgdRecall, sgdPrecision):    
    plt.plot([naiveBayesRecall],[naiveBayesPrecision], 'ro')
    plt.plot([svmRecall],[svmPrecision], 'ms')
    plt.plot([randomForestRecall],[randomForestPrecision], 'yo')
    plt.plot([logisticRegressionRecall],[logisticRegressionPrecision], 'go')
    plt.plot([sgdRecall],[sgdPrecision], 'xb-')
    plt.axis([0, 1, 0, 1])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall comparison plot')
    plt.legend(['MNB', 'SVM', 'RF', 'LR', 'SGD'], loc='upper left')
    plt.show() 
    
def plotAcuuracyComaprisonGraph(naiveBayesFMeasure, svmFMeasure, randomForestFMeasure, logisticRegressionFMeasure, sgdFMeasure):
    # Accuracy Comparison Plot
    cl = ('MNB', 'SVC', 'RF', 'LR', 'SGD')
    y_pos = np.arange(len(cl))
    acc = [77.2682926829,79.0243902439,76.8780487805,80.6829268293,75.3170731707]
    plt.bar(y_pos, acc, align='center', alpha=0.5)
    plt.xticks(y_pos, cl)
    plt.title('Accuracy Comparison Plot')
    plt.show()
    cl = ('MNB', 'SVC', 'RF', 'LR', 'SGD')
    y_pos = np.arange(len(cl))
    acc = [naiveBayesFMeasure, svmFMeasure, randomForestFMeasure, logisticRegressionFMeasure, sgdFMeasure]
    plt.bar(y_pos, acc, align='center', alpha=1.0)
    plt.xticks(y_pos, cl)
    plt.title('F Measure Comparison Plot')
    plt.show()
 
def applyNaiveBayesClassifier(X_train, y_train, X_test, y_test):
    # Thanks to sklearn, let us quickly train some multinomial models
    # Model Training: Multinomial Naive Bayes
    mnb_classifier = MultinomialNB()
    mnb_classifier.fit(X_train, y_train)
    model_accuracies = cross_val_score(estimator=mnb_classifier, 
                                       X=X_train, y=y_train, cv=10)
    model_accuracies.mean()
    model_accuracies.std()
    # Model Testing: Multinomial Naive Bayes
    y_pred = mnb_classifier.predict(X_test)
    metrics.confusion_matrix(y_test, y_pred)
    test_accuracy = metrics.accuracy_score(y_test, y_pred)
    precision_mnb = precision_score(y_test, y_pred, average='macro')  
    recall_mnb = recall_score(y_test, y_pred, average='macro') 
    f_mnb = 2*(precision_mnb*recall_mnb)/(precision_mnb+recall_mnb)
    print("Multinomial Naive Bayes Classifier Test Accuracy: ", test_accuracy*100)
    print("Multinomial Naive Bayes Classifier Test Precision: ", precision_mnb*100)
    print("Multinomial Naive Bayes Classifier Test Recall: ", recall_mnb*100)
    print("Multinomial Naive Bayes Classifier Test F measure: ", f_mnb*100)
    return precision_mnb, recall_mnb, f_mnb
    
def applySVMClassifier(X_train, y_train, X_test, y_test):
    # Model Training: SVMs
    svc_classifier = SVC(kernel='linear', random_state=0)
    svc_classifier.fit(X_train, y_train)
    model_accuracies = cross_val_score(estimator=svc_classifier, 
                                   X=X_train, y=y_train, cv=10) 
    print("Model Accuracies Mean", model_accuracies.mean()*100)
    print("Model Accuracies Standard Devision", model_accuracies.std()*100)
    # Model Testing: SVMs
    y_pred = svc_classifier.predict(X_test)
    metrics.confusion_matrix(y_test, y_pred)
    test_accuracy = metrics.accuracy_score(y_test, y_pred)
    precision_SVC = precision_score(y_test, y_pred, average='macro')  
    recall_SVC = recall_score(y_test, y_pred, average='macro') 
    f_SVC = 2*(precision_SVC * recall_SVC) / (precision_SVC + recall_SVC)
    print("SVCs Test Accuracy: ", test_accuracy*100)
    print("SVCs Test Precision: ", precision_SVC*100)
    print("SVCs Test Recall: ", recall_SVC*100)
    print("SVCs Test F measure: ", f_SVC*100)
    return precision_SVC, recall_SVC, f_SVC
    
def applyRandomForestClassifier(X_train, y_train, X_test, y_test):
    # Model Training: Random Forests Classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, class_weight="balanced",
                                        criterion='entropy', random_state=1)
    rf_classifier.fit(X_train, y_train)
    model_accuracies = cross_val_score(estimator=rf_classifier, 
                                   X=X_train, y=y_train, cv=5) 
    print("Model Accuracies Mean", model_accuracies.mean()*100)
    print("Model Accuracies Standard Devision", model_accuracies.std()*100)
    # Model Testing: Random Forests Classifier
    y_pred = rf_classifier.predict(X_test)
    metrics.confusion_matrix(y_test, y_pred)
    test_accuracy = metrics.accuracy_score(y_test, y_pred)
    precision_RF = precision_score(y_test, y_pred, average='macro')  
    recall_RF = recall_score(y_test, y_pred, average='macro') 
    f_RF = 2*(precision_RF * recall_RF) / (precision_RF + recall_RF)
    print("Random Forests Test Accuracy: ", test_accuracy*100)
    print("Random Forests Test Precision: ", precision_RF*100)
    print("Random Forests Test Recall: ", recall_RF*100)
    print("Random Forests Test F measure: ", f_RF*100)
    return precision_RF, recall_RF, f_RF
    
def applyLogisticRegressionClassifier(X_train, y_train, X_test, y_test):
    #Apply Logistic Regression Classifier
    lr = LogisticRegression(penalty = 'l2', C = 1)
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    metrics.confusion_matrix(y_test, y_pred)
    test_accuracy = metrics.accuracy_score(y_test, y_pred)
    precision_LR = precision_score(y_test, y_pred, average='macro')  
    recall_LR = recall_score(y_test, y_pred, average='macro') 
    f_LR = 2*(precision_LR * recall_LR) / (precision_LR + recall_LR)
    print("LogisticRegression_classifier Accuracy percent:",test_accuracy *100)
    print("LogisticRegression_classifier Precision percent:",precision_LR *100)
    print("LogisticRegression_classifier Recall percent:",recall_LR *100)
    print("LogisticRegression_classifier F measure:",f_LR *100)
    return precision_LR, recall_LR, f_LR
    
def applySGDClassifier(X_train, y_train, X_test, y_test):
    #Apply SGD Classifier
    SGDClassifier_classifier = SGDClassifier()
    SGDClassifier_classifier.fit(X_train, y_train)
    y_pred = SGDClassifier_classifier.predict(X_test)
    metrics.confusion_matrix(y_test, y_pred)
    test_accuracy = metrics.accuracy_score(y_test, y_pred)
    precision_SGD = precision_score(y_test, y_pred, average='macro')  
    recall_SGD = recall_score(y_test, y_pred, average='macro')
    f_SGD = 2*(precision_SGD * recall_SGD) / (precision_SGD + recall_SGD)
    print("SGD_classifier Accuracy percent:",test_accuracy *100)
    print("SGD_classifier Precision percent:",precision_SGD *100)
    print("SGD_classifier Recall percent:",recall_SGD *100)
    print("SGD_classifier Recall F measure:",f_SGD *100)
    return precision_SGD, recall_SGD, f_SGD
    
def applyDecisionTreeClassifier(X_train, y_train, X_test, y_test):
    #Apply Decision Tree Classifier
    Decision_Tree_CLF = DecisionTreeClassifier(random_state=0)
    Decision_Tree_CLF.fit(X_train, y_train)
    y_pred = Decision_Tree_CLF.predict(X_test)
    metrics.confusion_matrix(y_test, y_pred)
    test_accuracy = metrics.accuracy_score(y_test, y_pred)
    precision_DT = precision_score(y_test, y_pred, average='macro')  
    recall_DT = recall_score(y_test, y_pred, average='macro')
    f_DT = 2*(precision_DT * recall_DT) / (precision_DT + recall_DT)
    print("SGD_classifier Accuracy percent:",test_accuracy *100)
    print("SGD_classifier Precision percent:",precision_DT *100)
    print("SGD_classifier Recall percent:",recall_DT *100)
    print("SGD_classifier Recall F measure:",f_DT *100)
    return precision_DT, recall_DT, f_DT
    
def resolveOverSampling(X_train, y_train, X_test, y_test):
    # Over Sampling
    sm = SMOTE(random_state=0, ratio = 1.0)
    x_train_res, y_train_res = sm.fit_sample(X_train, y_train)
    x_test_res, y_test_res = sm.fit_sample(X_test, y_test)
    
def resolveUnderSampling(X_train, y_train, X_test, y_test):
    # Under Sampling
    rus = RandomUnderSampler(random_state=42)
    x_train_res, y_train_res= rus.fit_sample(X_train, y_train)
    x_test_res, y_test_res = rus.fit_sample(X_test, y_test)
    
def plotLabels(y):
    #Encoding y
    y_encoded = labelEncoding(y)
    #Count Labels and plot them
    y_count = Counter(y_encoded)
    key = y_count.keys()
    df = pd.DataFrame(y_count,index=key)
    df.drop(df.columns[1:], inplace=True)
    df.plot(kind='bar')
    plt.show()
    

"""
x,y = pre()
# Let us consider CountVectorizer from sklearn
# CountVectorizer, TfidfVectorizer, Word Embeddings, Word2Vec
X_vec = countVectorizer(x)
y_encoded = labelEncoding(y)
# Now, the dataset should be split in to train and test sets
X_train, X_test, y_train, y_test = splitTestTrain(X_vec, y_encoded)
#kfold validation
#X_train, X_test, y_train, y_test = kFold(X_vec)
#plot Labels of Dataset
plotLabels()
#precison, recall and f-measure of all the six classifiers
naiveBayesPrecision, naiveBayesRecall, naiveBayesFMeasure = applyNaiveBayesClassifier()
svmPrecision, svmRecall, svmFMeasure = applySVMClassifier()
randomForestPrecision, randomForestRecall, randomForestFMeasure = applyRandomForestClassifier()
logisticRegressionPrecision, logisticRegressionRecall, logisticRegressionFMeasure = applyLogisticRegressionClassifier()
sgdPrecision, sgdRecall, sgdFMeasure = applySGDClassifier()
decisionTreePrecision, decisionTreeRecall, decisionTreeFMeasure = applyDecisionTreeClassifier()

#Plot Precision-Recall comparison graph
plotPreRec()

#plot FMeasure comparison graph
plotAcuuracyComaprisonGraph()
"""

"""
#c = Counter(df.event)
from sklearn.preprocessing import OneHotEncoder
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = y_encoded.reshape(len(y_encoded), 1)
#var = np.max(integer_encoded)+1
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

from sklearn.preprocessing import LabelBinarizer
lb = LabelBinarizer()
label = lb.fit_transform(onehot_encoded)
label = np.hstack((label, 1 - label))
label
"""













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
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
import string
import sys
# fname = str(sys.argv[1])
# fname = "events_corpus_500.csv"
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
    tweet = tweet.strip()
    
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", tweet)

def pre(fname):
    # Reading training and test files to list data structures
    data = pd.read_csv("Corpuses/" + fname , sep = ",", index_col=False, encoding='latin-1', low_memory=False)
    df_old = DataFrame(data)
    # print(df_old)

    # Take those datasets in which text is not null
    df = df_old[df_old['text'].notnull()]
    # print(df)


    labelCount = df.groupby(df['event']).count()
    print(labelCount)

    # Replaces URLs (http/www) 
    x = df['text'].str.replace('http\S+|www.\S+', '', case=False)

    # Changes types in events column to string
    y = df['event'].astype(str)
    timestamp = df['timestamp']

    # Replaces words with special characters
    x = x.str.replace('[^a-zA-Z0-9-_.]', ' ')

    # Replaces unreadable characters, further cleaning
    printable = set(string.printable)
    filter(lambda q: q in printable, x)

    # Lemmatize words
    x_lemma = [" ".join([lemmatize(word) for word in sentence.split(" ")]) for sentence in x]

    # x_stem = [" ".join([stem(word) for word in sentence.split(" ")]) for sentence in x_lemma]

    # Clean data per word
    x_clean = [finalClean(sentence) for sentence in x_lemma]
    #temp_df = [filter(lambda i: i not in string.punctuation,sentence) for sentence in x_clean]
    return x_clean, y, timestamp

def labelEncoding(y):
    labelEncoder = LabelEncoder()
    y_encoded = labelEncoder.fit_transform(y)
    y_encoded
    return y_encoded, labelEncoder

def countVectorizer(x):
    stopset = set(stopwords.words('English'))
    vect = CountVectorizer(analyzer='word', encoding='utf-8', min_df = 0, ngram_range=(2, 2), lowercase = True, strip_accents='ascii', stop_words = stopset)
    X_vec = vect.fit_transform(x)
    return X_vec

def tfidfVectorizer(x):
    stopset = set(stopwords.words('English'))
    vect = TfidfVectorizer(analyzer='word', encoding='utf-8', min_df = 0, ngram_range=(1, 1), lowercase = True, strip_accents='ascii', stop_words = stopset)
    X_vec = vect.fit_transform(x)
    return X_vec

def extractTimeFeatures(timestamp):
    maxTime = timestamp.max()
    minTime = timestamp.min()

    floatArr = []

    for index, item in enumerate(timestamp):
        floatArr.append( (item-minTime)/(maxTime-minTime) )

    normalized = pd.Series(floatArr)

    return normalized

def splitTestTrain(X_vec, y_encoded):
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y_encoded, 
													test_size=0.9, random_state=0, shuffle=True)
    return X_train, X_test, y_train, y_test

def kFold(X_vec, y_encoded):
    kf = KFold(n_splits=2, random_state=None, shuffle=False)
    for train_index, test_index in kf.split(X_vec):
        print("TRAIN:", train_index, "TEST:", test_index)
        X_train, X_test = X_vec[train_index], X_vec[test_index]
        y_train, y_test = y_encoded[train_index], y_encoded[test_index]
        return X_train, X_test, y_train, y_test
    
def plotPreRec(naiveBayesRecall, naiveBayesPrecision, svmRecall, svmPrecision, randomForestRecall, randomForestPrecision, logisticRegressionRecall, logisticRegressionPrecision, sgdRecall, sgdPrecision):    
    file = fname[:-4]
    plt.plot([naiveBayesRecall],[naiveBayesPrecision], 'ro')
    plt.plot([svmRecall],[svmPrecision], 'ms')
    plt.plot([randomForestRecall],[randomForestPrecision], 'yo')
    plt.plot([logisticRegressionRecall],[logisticRegressionPrecision], 'go')
    plt.plot([sgdRecall],[sgdPrecision], 'xb-')
    plt.axis([0.4, 1, 0.4, 1])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall comparison plot')
    plt.legend(['MNB', 'SVM', 'RF', 'LR', 'SGD'], loc='upper left')
    plt.savefig(file + "_Precision-Recall_comparison.jpg")
    # plt.show() 
    
def plotFmeasureComparisonGraph(naiveBayesFMeasure, svmFMeasure, randomForestFMeasure, nnFMeasure):
    cl = ('MNB', 'SVC', 'RF', 'NN')
    y_pos = np.arange(len(cl))
    acc = [naiveBayesFMeasure, svmFMeasure, randomForestFMeasure, nnFMeasure]
    plt.bar(y_pos, acc, align='center', alpha=1.0)
    plt.xticks(y_pos, cl)
    plt.title('F Measure Comparison Plot')
    plt.show()

def plotAcuuracyComparisonGraph(naiveBayesAccuracy, svmAccuracy, randomForestAccuracy, nnAccuracy):
    cl = ('MNB', 'SVC', 'RF', 'NN')
    y_pos = np.arange(len(cl))
    acc = [naiveBayesAccuracy, svmAccuracy, randomForestAccuracy, nnAccuracy]
    plt.bar(y_pos, acc, align='center', alpha=1.0)
    plt.xticks(y_pos, cl)
    plt.title('Accuracy Comparison Plot')
    plt.show()
 
def applyNaiveBayesClassifier(X_train, y_train, X_test, y_test):
    # Thanks to sklearn, let us quickly train some multinomial models
    # Model Training: Multinomial Naive Bayes
    mnb_classifier = MultinomialNB()
    mnb_classifier.fit(X_train, y_train)
    # model_accuracies = cross_val_score(estimator=mnb_classifier, 
    #                                    X=X_train, y=y_train, cv=10)

    # print("\n\nMultinomial Naive Bayes Accuracies Mean", model_accuracies.mean()*100)
    # print("Multinomial Naive Bayes Accuracies Standard Devision", model_accuracies.std()*100)
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
    return precision_mnb, recall_mnb, f_mnb, test_accuracy*100, mnb_classifier

def applyNeuralNetworkClassifier(X_train, y_train, X_test, y_test):
    # Model Training: Neural Network
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    nn_classifier = clf.fit(X_train, y_train)
    y_pred = nn_classifier.predict(X_test)

    metrics.confusion_matrix(y_test, y_pred)
    test_accuracy = metrics.accuracy_score(y_test, y_pred)
    precision_mnb = precision_score(y_test, y_pred, average='macro')  
    recall_mnb = recall_score(y_test, y_pred, average='macro') 
    f_mnb = 2*(precision_mnb*recall_mnb)/(precision_mnb+recall_mnb)
    print("\n\nNeural Network Classifier Test Accuracy: ", test_accuracy*100)
    print("Neural Network Classifier Test Precision: ", precision_mnb*100)
    print("Neural Network Classifier Test Recall: ", recall_mnb*100)
    print("Neural Network Classifier Test F measure: ", f_mnb*100)

    return precision_mnb, recall_mnb, f_mnb, test_accuracy*100, nn_classifier
    
def applySVMClassifier(X_train, y_train, X_test, y_test):
    # Model Training: SVMs
    svc_classifier = SVC(kernel='linear', random_state=1)
    svc_classifier.fit(X_train, y_train)
    # model_accuracies = cross_val_score(estimator=svc_classifier, 
    #                                X=X_train, y=y_train, cv=10) 
    # print("\n\nSVCs Accuracies Mean", model_accuracies.mean()*100)
    # print("SVCs Accuracies Standard Devision", model_accuracies.std()*100)
    # Model Testing: SVMs
    y_pred = svc_classifier.predict(X_test)
    metrics.confusion_matrix(y_test, y_pred)
    test_accuracy = metrics.accuracy_score(y_test, y_pred)
    precision_SVC = precision_score(y_test, y_pred, average='macro')  
    recall_SVC = recall_score(y_test, y_pred, average='macro') 
    f_SVC = 2*(precision_SVC * recall_SVC) / (precision_SVC + recall_SVC)
    print("\n\nSVCs Test Accuracy: ", test_accuracy*100)
    print("SVCs Test Precision: ", precision_SVC*100)
    print("SVCs Test Recall: ", recall_SVC*100)
    print("SVCs Test F measure: ", f_SVC*100)
    return precision_SVC, recall_SVC, f_SVC, test_accuracy*100, svc_classifier
    
def applyRandomForestClassifier(X_train, y_train, X_test, y_test):
    # Model Training: Random Forests Classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, class_weight="balanced",
                                        criterion='entropy', random_state=1)
    rf_classifier.fit(X_train, y_train)
    # model_accuracies = cross_val_score(estimator=rf_classifier, 
    #                                X=X_train, y=y_train, cv=5) 
    # print("\n\nRandom Forest's Accuracies Mean", model_accuracies.mean()*100)
    # print("Random Forest's Accuracies Standard Devision", model_accuracies.std()*100)
    # Model Testing: Random Forests Classifier
    y_pred = rf_classifier.predict(X_test)
    metrics.confusion_matrix(y_test, y_pred)
    test_accuracy = metrics.accuracy_score(y_test, y_pred)
    precision_RF = precision_score(y_test, y_pred, average='macro')  
    recall_RF = recall_score(y_test, y_pred, average='macro') 
    f_RF = 2*(precision_RF * recall_RF) / (precision_RF + recall_RF)
    print("\n\nRandom Forest's Test Accuracy: ", test_accuracy*100)
    print("Random Forest's Test Precision: ", precision_RF*100)
    print("Random Forest's Test Recall: ", recall_RF*100)
    print("Random Forest's Test F measure: ", f_RF*100)
    return precision_RF, recall_RF, f_RF, test_accuracy*100, rf_classifier
    
def applyLogisticRegressionClassifier(X_train, y_train, X_test, y_test):
    #Apply Logistic Regression Classifier
    lr = LogisticRegression(penalty = 'l2', C = 1)
    lr.fit(X_train, y_train)
    model_accuracies = cross_val_score(estimator=lr, 
                                   X=X_train, y=y_train, cv=5) 
    print("\n\nLogisticRegression_classifier Accuracies Mean", model_accuracies.mean()*100)
    print("LogisticRegression_classifier Accuracies Standard Devision", model_accuracies.std()*100)
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
    model_accuracies = cross_val_score(estimator=SGDClassifier_classifier, 
                                   X=X_train, y=y_train, cv=5) 
    print("\n\nSGD_classifier Accuracies Mean", model_accuracies.mean()*100)
    print("SGD_classifier Accuracies Standard Devision", model_accuracies.std()*100)
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
    model_accuracies = cross_val_score(estimator=Decision_Tree_CLF, 
                                   X=X_train, y=y_train, cv=5) 
    print("\n\nDecision Tree Classifier Accuracies Mean", model_accuracies.mean()*100)
    print("Decision Tree Classifier Accuracies Standard Devision", model_accuracies.std()*100)
    y_pred = Decision_Tree_CLF.predict(X_test)
    metrics.confusion_matrix(y_test, y_pred)
    test_accuracy = metrics.accuracy_score(y_test, y_pred)
    precision_DT = precision_score(y_test, y_pred, average='macro')  
    recall_DT = recall_score(y_test, y_pred, average='macro')
    f_DT = 2*(precision_DT * recall_DT) / (precision_DT + recall_DT)
    print("Decision Tree Classifier Accuracy percent:",test_accuracy *100)
    print("Decision Tree Classifier Precision percent:",precision_DT *100)
    print("Decision Tree Classifier Recall percent:",recall_DT *100)
    print("Decision Tree Classifier Recall F measure:",f_DT *100)
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













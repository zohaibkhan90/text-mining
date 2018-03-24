# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 15:49:47 2017

@author: mumar
"""
import twitter_sentiment as ts

x, y = ts.pre()
# Let us consider CountVectorizer from sklearn
# CountVectorizer, TfidfVectorizer, Word Embeddings, Word2Vec
X_vec = ts.countVectorizer(x)
y_encoded = ts.labelEncoding(y)
# Now, the dataset should be split in to train and test sets
X_train, X_test, y_train, y_test = ts.splitTestTrain(X_vec, y_encoded)

# print("x-train:")
# print(X_train)
# print("Y-train:")
# print(y_train)
#kfold validation
#X_train, X_test, y_train, y_test = kFold(X_vec, y_encoded)
#plot Labels of Dataset
ts.plotLabels(y)

# print("Start training")
#precison, recall and f-measure of all the six classifiers
# naiveBayesPrecision, naiveBayesRecall, naiveBayesFMeasure = ts.applyNaiveBayesClassifier(X_train, y_train, X_test, y_test)
# svmPrecision, svmRecall, svmFMeasure = ts.applySVMClassifier(X_train, y_train, X_test, y_test)
# randomForestPrecision, randomForestRecall, randomForestFMeasure = ts.applyRandomForestClassifier(X_train, y_train, X_test, y_test)
# logisticRegressionPrecision, logisticRegressionRecall, logisticRegressionFMeasure = ts.applyLogisticRegressionClassifier(X_train, y_train, X_test, y_test)
# sgdPrecision, sgdRecall, sgdFMeasure = ts.applySGDClassifier(X_train, y_train, X_test, y_test)
# decisionTreePrecision, decisionTreeRecall, decisionTreeFMeasure = ts.applyDecisionTreeClassifier(X_train, y_train, X_test, y_test)

#Plot Precision-Recall comparison graph
# ts.plotPreRec(naiveBayesRecall, naiveBayesPrecision, svmRecall, svmPrecision, randomForestRecall, randomForestPrecision, logisticRegressionRecall, logisticRegressionPrecision, sgdRecall, sgdPrecision)
#plot FMeasure comparison graph
# ts.plotAcuuracyComaprisonGraph(naiveBayesFMeasure, svmFMeasure, randomForestFMeasure, logisticRegressionFMeasure, sgdFMeasure)
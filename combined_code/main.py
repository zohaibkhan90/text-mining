# -*- coding: utf-8 -*-
from scipy import sparse
import event_detection as ts
import sys

fname = str(sys.argv[1])
x, y, timestamp = ts.pre()

timestamp = ts.extractTimeFeatures(timestamp)

# Let us consider CountVectorizer from sklearn
# CountVectorizer, TfidfVectorizer, Word Embeddings, Word2Vec
X_vec = ts.countVectorizer(x)
# X_vec = ts.tfidfVectorizer(x)

y_encoded = ts.labelEncoding(y)

# Add time stamp coulnm to X_vec
X_vec = sparse.hstack((X_vec,timestamp[:,None])).A


# Now, the dataset should be split in to train and test sets
X_train, X_test, y_train, y_test = ts.splitTestTrain(X_vec, y_encoded)

# ts.featureUnion(X_vec, timestamp)
# print(type(X_vec[0]))

# print("x-train:")
# print(X_train)
# print("Y-train:")
# print(y_train)
#kfold validation
# X_train, X_test, y_train, y_test = kFold(X_vec, y_encoded)
#plot Labels of Dataset
# ts.plotLabels(y)

print("Start training with " + fname[:-4])
#precison, recall and f-measure of all the six classifiers
naiveBayesPrecision, naiveBayesRecall, naiveBayesFMeasure = ts.applyNaiveBayesClassifier(X_train, y_train, X_test, y_test)
svmPrecision, svmRecall, svmFMeasure = ts.applySVMClassifier(X_train, y_train, X_test, y_test)
randomForestPrecision, randomForestRecall, randomForestFMeasure = ts.applyRandomForestClassifier(X_train, y_train, X_test, y_test)
logisticRegressionPrecision, logisticRegressionRecall, logisticRegressionFMeasure = ts.applyLogisticRegressionClassifier(X_train, y_train, X_test, y_test)
sgdPrecision, sgdRecall, sgdFMeasure = ts.applySGDClassifier(X_train, y_train, X_test, y_test)
decisionTreePrecision, decisionTreeRecall, decisionTreeFMeasure = ts.applyDecisionTreeClassifier(X_train, y_train, X_test, y_test)

# Plot Precision-Recall comparison graph
ts.plotPreRec(naiveBayesRecall, naiveBayesPrecision, svmRecall, svmPrecision, randomForestRecall, randomForestPrecision, logisticRegressionRecall, logisticRegressionPrecision, sgdRecall, sgdPrecision)
# plot FMeasure comparison graph
ts.plotAcuuracyComaprisonGraph(naiveBayesFMeasure, svmFMeasure, randomForestFMeasure, logisticRegressionFMeasure, sgdFMeasure)
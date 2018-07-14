from scipy import sparse
import event_detection as ed

fileName = 'events_corpus.csv'

x, y, timestamp = ed.pre(fileName)

X_vec = ed.tfidfVectorizer(x)

y_encoded, labelEncoder = ed.labelEncoding(y)

X_train, X_test, y_train, y_test = ed.splitTestTrain(X_vec, y_encoded)


naiveBayesPrecision, naiveBayesRecall, naiveBayesFMeasure, nbClassifier = ed.applyNaiveBayesClassifier(X_train, y_train, X_test, y_test)
svmPrecision, svmRecall, svmFMeasure, svcClassifier = ed.applySVMClassifier(X_train, y_train, X_test, y_test)
randomForestPrecision, randomForestRecall, randomForestFMeasure, rfClassifier = ed.applyRandomForestClassifier(X_train, y_train, X_test, y_test)
nnPrecision, nnRecall, nnFMeasure, nnClassifier = ed.applyNeuralNetworkClassifier(X_train, y_train, X_test, y_test)

out = nbClassifier.predict(X_test[2000])
print(out)
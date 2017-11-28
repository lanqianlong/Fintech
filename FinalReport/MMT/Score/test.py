# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 06:59:22 2016

@author: Administrator
"""

from sklearn import svm
from sklearn.externals import joblib
from sklearn import preprocessing
from sklearn import cross_validation


clf3 = joblib.load('Grade.pkl')

scaler3 = joblib.load('test.pkl')

X_test_transformed3 = scaler3.transform(X_test)
print clf3.score(X_test_transformed, y_test)
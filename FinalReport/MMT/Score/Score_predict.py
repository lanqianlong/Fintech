# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 13:18:55 2016

@author: Junxiao
"""
import numpy as np
import MySQLdb
#from sklearn.decomposition import PCA
from sklearn import svm
from sklearn.externals import joblib
import random
from sklearn import cross_validation
from sklearn import preprocessing


# 打开数据库连接
Database_ip = "172.25.31.146"
db = MySQLdb.connect(Database_ip,"root","123456789o","MMT" )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()


X = []
y = []
train_num = 70000
id_train = []
# 构建每个数据的特征向量
for grade_num in range(1,8):
    sql = """SELECT count(*) FROM  loandatabase WHERE grade = %d""" % grade_num
    cursor.execute(sql)
    num_grade = cursor.fetchone()[0]
    sql = """SELECT id FROM  loandatabase WHERE grade = %d""" % grade_num
    cursor.execute(sql)
    results = cursor.fetchall()
    for n in random.sample(range(num_grade),train_num/7):
        id_train.append(int(results[n][0]))
    
        







for id in range(train_num):
    try:
        sql = """SELECT * FROM  loandatabase WHERE id = %d""" % id_train[id]
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            igeoid = int(row[1])
            famount = row[2]
            fdti = row[3]
            brej_acc = int(row[4])
#            int_rate = float(row[5])
            grade = int(row[6])
            annual_income = float(row[7])
#            loan_status = int(row[8])
    #    print "GEOID = %d, Amount = %.2f, DTI = %.2f%%, Rej_Acc = %d" % \
    #            (igeoid, famount, fdti, brej_acc)
        X.append([famount, annual_income])
        if annual_income:
            X[id].extend([famount/annual_income, 1])
        else:
            X[id].extend([0.0, 0])        
        y.append(grade)
        # cost_of_living
        sql = """SELECT * FROM cost_of_living WHERE geoid = %d""" % igeoid
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for data in row[1:]:
                X[id].extend([float(data)])
            if float(row[1]):
                X[id].extend([famount/float(row[1]), 1])
            else:
                X[id].extend([0.0, 0])
            if float(row[2]):
                X[id].extend([famount/float(row[2]), 1])
            else:
                X[id].extend([0.0, 0])
            if float(row[3]):
                X[id].extend([famount/float(row[3]), 1])
            else:
                X[id].extend([0.0, 0])            
            if float(row[25]):
                X[id].extend([famount/float(row[25]), 1])
            else:
                X[id].extend([0.0, 0])              
        # Crime
        sql = """SELECT * FROM crime WHERE geoid = %d""" % igeoid
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for data in row[1:]:
                X[id].extend([float(data)])
        # Education
        sql = """SELECT * FROM education WHERE geoid = %d""" % igeoid
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for data in row[1:]:
                X[id].extend([float(data)])
        # Employment
        sql = """SELECT * FROM employment WHERE geoid = %d""" % igeoid
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for data in row[1:]:
                X[id].extend([float(data)])
            if float(row[1]):
                X[id].extend([famount/float(row[1]), 1])
            else:
                X[id].extend([0.0, 0])        
            
        # Housing
        sql = """SELECT * FROM housing WHERE geoid = %d""" % igeoid
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for data in row[1:]:
                X[id].extend([float(data)])
    
        # Weather
        sql = """SELECT * FROM weather WHERE geoid = %d""" % igeoid
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for data in row[1:]:
                X[id].extend([float(data)])
    except:
        temp = 0
print 'Data loading Done!'








X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.4, random_state=0)
scaler = preprocessing.StandardScaler().fit(X_train)
X_train_transformed = scaler.transform(X_train)

score_tmp = 0

C_values = [1e-2, 5e-2, 1e-1, 1]
for C_value in C_values:
#    clf = svm.SVC(C=1e-3,kernel='rbf',  gamma= gamma_value).fit(X_train_transformed, y_train)
    clf = svm.SVC(C = C_value,kernel='linear').fit(X_train_transformed, y_train)
    X_test_transformed = scaler.transform(X_test)
    tmp = clf.score(X_test_transformed, y_test)
    print 'C = ', C_value, tmp
    if tmp > score_tmp:
        score_tmp = tmp
        joblib.dump(clf, 'Grade.pkl') 
        joblib.dump(scaler, 'scaler_std.pkl')
        
print score_tmp
        
    
# 关闭数据库连接
db.close()        
    
    




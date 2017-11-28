# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 06:08:02 2016

@author: Administrator
"""
import numpy as np
import MySQLdb
from sklearn.externals import joblib
import random
from sklearn.metrics import accuracy_score

# 打开数据库连接
Database_ip = "172.25.31.146"
db = MySQLdb.connect(Database_ip,"root","123456789o","MMT" )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# 获取训练数据总数
sql = """SELECT COUNT(*) FROM loandatabase"""

try:
    cursor.execute(sql)
    result = cursor.fetchone()
    Number_RA = int(result[0])
#    print Number_RA
except:
    print "Error: unable to fecth data"


 
clf = joblib.load('Grade.pkl')
scaler = joblib.load('scaler_std.pkl')

X = []
y = []
train_num = 10
# 构建每个数据的特征向量
for id in range(train_num):
    try:
        sql = """SELECT * FROM  loandatabase WHERE id = %d""" % (random.randint(1, 2237910))
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
X_test_transformed = scaler.transform(X)
print 'predict'
print list(clf.predict(X_test_transformed))
print y

         
# 关闭数据库连接
db.close()    
#print 'Data loading Done!'
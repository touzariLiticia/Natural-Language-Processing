#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 16:19:03 2020

@author: h_djeddal
"""
import codecs
import re
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn import svm
from sklearn.model_selection import cross_validate
from sklearn import datasets, linear_model
    

      
def read_file(fn):
    with codecs.open(fn,encoding="utf-8") as f:
        return f.read()
   
fname="corpus.tache1.learn.utf8"
fname_test="corpus.tache1.test.utf8"
nblignes = 10000
#print( "nblignes = %d",nblignes)
alltxts = []
allabs=[]
#labs = np.ones(nblignes)
s=codecs.open(fname, 'r','utf-8') # pour régler le codage

cpt = 0
for i in range(nblignes):
    txt = s.readline()

    lab = re.sub(r"<[0-9]*:[0-9]*:(.)>.*","\\1",txt)
    txt = re.sub(r"<[0-9]*:[0-9]*:.>(.*)","\\1",txt)

    alltxts.append(txt)
    if(lab[0]=='C'):
        l=1
    else:
        l=-1
    allabs.append(l)
    cpt += 1
    #if cpt %1000 ==0:
     #   print (cpt)
#print(alltxts)


vectorizer = CountVectorizer()
tfidfvect=TfidfVectorizer()
Matrix = vectorizer.fit_transform(alltxts)
#Matrix_tfid=tfidfvect.fit_transform(alltxts)
#print(vectorizer.get_feature_names())
#print(Matrix.toarray())
classif = svm.SVC()
classif.fit(Matrix, allabs)
#print(classif.predict(Matrix))
#print(classif.n_support_)
#lasso = linear_model.Lasso()
cv_results = cross_validate(classif, Matrix, allabs)
print(cv_results)


"""        TEST PREDICTION 
alltxts_test = []
s=codecs.open(fname_test, 'r','utf-8') # pour régler le codage
#generation du bow du fichier test
cpt = 0
for i in range(nblignes):
    txt = s.readline()
    txt = re.sub(r"<[0-9]*:[0-9]*>(.*)","\\1",txt)

    alltxts_test.append(txt)

vect_test=CountVectorizer(vocabulary=vectorizer.get_feature_names())
Matrix_test=vect_test.fit_transform(alltxts_test)
prediction=classif.predict(Matrix_test)
fichier = open("prediction.txt", "a")
for res in prediction:
    if (res ==1):
        fichier.write("C\n")
    else:
        fichier.write("M\n")
fichier.close()
"""  
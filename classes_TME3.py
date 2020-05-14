#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 16:52:05 2020

@author: TOUZARI
"""

import TextRepresenter as TR
import json
import numpy as np
from math import *

from statistics import *
from classes_TME1 import *
from classes_TME2 import *

"""--------------TME3 """ 

class Query():
     def __init__(self,id,txt="",docs=[]):
         self.id=id
         self.txt=txt
         self.docs=docs
     def affiche(self):
         print(self.id)
         #print(self.txt)
         print(self.docs)
class QueryParser():
    def __init__(self):
        self.list_query=[]
    def getQueries(self,nomfichier,nomfichier2):
        l=1
        fichier = open(nomfichier, "r")
        read=False
        lignes = fichier.readlines()
        fichier.close() 
        prem=True
        liste={}
        docs={}
        texte=''
        id=''
        ligne = lignes[0].strip()
        while(l<len(lignes)):
            
            if(read):
                ligne = lignes[l].strip()
                l+=1
                if(l==len(lignes)):
                    break;
            if(ligne[0:2]==".I"):
                read=True
                if(not prem):#On cree un nouveau doc
                   
                    liste[id]=Query(id,texte)  
                    texte=''
                    id='' 
                id=int(ligne[3:])
                prem=False
            if(ligne==".W"):
                ligne = lignes[l].strip()
                l+=1
                while(l<len(lignes) and ligne[0:2]!=".N" and  ligne[0:2]!=".C" and ligne[0:2]!=".I" and ligne[0:2]!=".T" and ligne[0:2]!=".B" and ligne[0:2]!=".A" and ligne[0:2]!=".W" and ligne[0:2]!=".X" and ligne[0:2]!=".K"):
                    texte += ligne
                    ligne = lignes[l].strip()
                    l+=1
                if(ligne[0:2]==".I"):
                    read=False
                else:
                    read=True
        
        l=1
        fichier = open(nomfichier2, "r")
        read=False
        lignes = fichier.readlines()
        fichier.close() 
        prem=True
        ligne = lignes[0].strip()
        while(l<len(lignes)):
            id=int(ligne[0:3])
            a=ligne[3:13]
            doc=a.split('\t', 1)[0]
            if(id not in docs.keys()):
                docs[id]=[]
            docs[id].append(doc)
            ligne = lignes[l].strip()
            l+=1  
        
        for q in docs.keys():
            if(q in liste.keys()):
                liste[q].docs=docs[q]
               
            else:
                print('pertinence sans q',q)
              
        return list(liste.values())
    
    
class EvalMesure():
     def __init__(self):
         pass
     def evalQuery(self,liste,query):
         pass

class Precision(EvalMesure):
     def __init__(self,k):
         self.rang=k
     def evalQuery(self,liste,query):
         les_docs=[int(liste[i][0]) for i in range(self.rang)]
         tp=0
         Q_docs=set([int(i) for i in query.docs])
         for id in les_docs:
             if(id in Q_docs):
                 tp+=1
         return tp/self.rang
    
    
class Rappel(EvalMesure):
     def __init__(self,k):
         self.rang=k
     def evalQuery(self,liste,query):
         les_docs=[int(liste[i][0]) for i in range(self.rang)]
         tp=0
         Q_docs=set([int(i) for i in query.docs])
         fn=len(Q_docs)
         for id in les_docs:
             if(id in Q_docs):
                 tp+=1
         return tp/(tp+fn) 
     
class F_mesure(EvalMesure):
     def __init__(self,k,beta):
         self.rang=k
         self.beta=beta
     def evalQuery(self,liste,query):
         pres=Precision(self.rang) 
         P=pres.evalQuery(liste,query)
         rap=Rappel(self.rang)
         R=rap.evalQuery(liste,query)
         return (1+self.beta**2)*(P*R)/((R*(self.beta**2))+R)
     
class PrecisionMoy(EvalMesure):
     def __init__(self):
         self.rang=0
     def evalQuery(self,liste,query):
         les_docs=[int(i[0]) for i in liste]
         Q_docs=list(set([int(i) for i in query.docs]))
         AvgP=0
         n=len(Q_docs)
         for i in range(len(les_docs)):
             if(les_docs[i] in Q_docs):
                 pres=Precision(i+1)
                 AvgP+=pres.evalQuery(liste,query)
         return AvgP/n

class reciprocalRank(EvalMesure):
     def __init__(self,Q):
         self.Qset=Q
     def evalQuery(self,modele):
         nbQ=len(self.Qset)
         MRR=0
         for q in self.Qset:
             if(q.docs!=[]):
                 Q_docs=list(set([int(i) for i in q.docs]))
                 liste=modele.getRanking(q.txt)
                 continuer=True
                 i=0
                 while (continuer and i<len(liste)):
                     if(liste[i][0]in Q_docs):
                         continuer=False
                         MRR+=1/(i+1)
                     i+=1
         return MRR/nbQ
    
class NDCG(EvalMesure):
     def __init__(self,k):
         self.rang=k
     def evalQuery(self,liste,query):
         les_docs=[int(liste[i][0]) for i in range(self.rang)]
         Q_docs=set([int(i) for i in query.docs])
         pertinence = [1 if d in Q_docs else 0 for d in les_docs]
         DCCA=pertinence[0]+sum([pertinence[i]/(np.log(i+1)) for i in range(1,len(pertinence))])
         IDCCA=1+sum([1/np.log(i+1) for i in range(1,len(Q_docs))])
         return DCCA/IDCCA
        
        
         
class EvalIRModel(EvalMesure):
     def __init__(self,Q):
         self.Qset=Q  
     def Eval_Precision(self,k,modele):
         val=[]
         prec=Precision(k)
         for q in self.Qset: 
             liste=modele.getRanking(q.txt)
             val.append(prec.evalQuery(liste,q))
         return np.mean(val),np.std(val)
     
     def Eval_Rappel(self,k,modele):
         val=[]
         rap=Rappel(k)
         for q in self.Qset: 
             liste=modele.getRanking(q.txt)
             val.append(rap.evalQuery(liste,q))
         return np.mean(val),np.std(val) 
     
     def Eval_F_mesure(self,k,b,modele):
         val=[]
         fm=F_mesure(k,b)
         for q in self.Qset: 
             liste=modele.getRanking(q.txt)
             val.append(fm.evalQuery(liste,q))
         return np.mean(val),np.std(val)
     
     def Eval_PrecisionMoy(self,modele):
         val=[]
         fm=PrecisionMoy()
         for q in self.Qset: 
             liste=modele.getRanking(q.txt)
             val.append(fm.evalQuery(liste,q))
         return np.mean(val),np.std(val)
     
     def Eval_reciprocalRank(self,modele):
         rr=reciprocalRank(self.Qset)
         val=rr.evalQuery(modele)
         return val
     
     def Eval_NDCG(self,k,modele):
         val=[]
         ndcg=NDCG(k)
         for q in self.Qset: 
             liste=modele.getRanking(q.txt)
             val.append(ndcg.evalQuery(liste,q))
         return np.mean(val),np.std(val)
         
     def comparaison(X,Y):
        
         var=variance(X)+variance(Y)
         moy=abs(np.mean(X)-np.mean(Y))
         
    
"""fichier= open('data/cisi/cisi.rel', "r")
read=False
lignes = fichier.readlines()
fichier.close() 
ligne = lignes[0].strip()
l=0
while(l<len(lignes)):
     print(ligne)
     ligne = lignes[l].strip()
     l+=1

a='   28\t0\t'
 
print(a.split('\t', 1)[0])    """    
        
        
    

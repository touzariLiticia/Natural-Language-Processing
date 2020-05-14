#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 16:54:18 2020

@author: macbook
"""
import TextRepresenter as TR
import json
import numpy as np
from math import *
from classes_TME1 import *
               
"""--------------TME2 """  


def get_score_bool(q,index): #t1 ou t2 ou ...
    scores=dict()
    te=TR.PorterStemmer()
    for d in index.items():
        d=list(d)
        scores[d[0]]=0
        qq=te.getTextRepresentation(q)
        for v in qq.keys():
            if(v in d[1].keys()):
                scores[d[0]]=1
            
    return scores 

def get_score_vect_InnerProduct(q,index):#Inner Product
    scores=dict()
    te=TR.PorterStemmer()
    for d in index.items():
        d=list(d)
        scores[d[0]]=0
        qq=te.getTextRepresentation(q)
        for v in qq.keys():
            if(v in d[1].keys()):
                scores[d[0]]+=d[1][v]*qq[v]

    return scores

def get_score_vect_DiceCoef(q,index):#Inner Product
    scores=dict()
    te=TR.PorterStemmer()
    for d in index.items():
        d=list(d)
        scores[d[0]]=0
        qq=te.getTextRepresentation(q)
        for v in qq.keys():
            if(v in d[1].keys()):
                scores[d[0]]+=d[1][v]
        scores[d[0]]=(2*scores[d[0]])/(sum(qq.values())+sum(d[1].values())) 
    return scores 

def get_score_vect_Cosinus(q,index):#Inner Product
    scores=dict()
    te=TR.PorterStemmer()
    for d in index.items():
        d=list(d)
        scores[d[0]]=0
        qq=te.getTextRepresentation(q)
        for v in qq.keys():
            if(v in d[1].keys()):
                scores[d[0]]+=d[1][v]
        scores[d[0]]=(scores[d[0]])/(sqrt(sum(qq.values()))+sqrt(sum(d[1].values()))) 
    return scores

"""
def get_score_vect_InnerProduct(q,index):#Inner Product
    scores=dict()
    te=TR.PorterStemmer()
    for d in index.items():
        d=list(d)
        scores[d[0]]=0
        qq=te.getTextRepresentation(q)
        for v in qq.keys():
            if(v in d[1].keys()):
                scores[d[0]]+=1

    return scores

def get_score_vect_DiceCoef(q,index):#Inner Product
    scores=dict()
    te=TR.PorterStemmer()
    for d in index.items():
        d=list(d)
        scores[d[0]]=0
        qq=te.getTextRepresentation(q)
        for v in qq.keys():
            if(v in d[1].keys()):
                scores[d[0]]+=1
        scores[d[0]]=(2*scores[d[0]])/(len(qq.keys())+len(d[1].keys())) 
    return scores 
"""

class Weighter():
     def __init__(self,i):
         self.simpleIndex=i
         self.index=i.index
         self.index_inverse=i.index_inverse
         self.normDoc={}
         self.vide=True
     def getWeightsForDoc(self,idDoc):
         pass
     
     def getWeightsForStem(self,stem):
         pass
     
     def getWeightsForQuery(query):
         pass
     def get_normDoc(self,idDoc):
         if(self.vide):
             self.vide=False
             res=self.normDoc[idDoc]=np.linalg.norm(list(self.index[idDoc].values()))
         elif(idDoc not in self.normDoc.keys()):
             res=self.normDoc[idDoc]=np.linalg.norm(list(self.index[idDoc].values()))
         else:
             res=self.normDoc[idDoc]
         return res
     
     def get_normQuery(self,q):
         te=TR.PorterStemmer()   
         qq=te.getTextRepresentation(q) 
         return np.linalg.norm(list(qq.values()))
     
     def proba_stemInD(self,stem,idDoc):# proba du stem dans un doc 
         p=self.index_inverse[stem]
         if idDoc in p.keys():
             return p[idDoc]/sum(p.values())
         return 0
     def proba_stemInC(self,stem):# proba du stem dans le collection
         taille=0
         nbStem=sum(self.index_inverse[stem].values())
         for s in self.index_inverse.keys():
            taille+=sum(self.index_inverse[s].values())
         return nbStem/taille
     
class Weighter1(Weighter):
    
     """ 
     Schéma de pondération : wt,d = tft,d et wt,q = 1 si t ∈ q, O sinon
     """
    
     def __init__(self,i):
         
         self.simpleIndex=i
         self.index=i.index
         self.index_inverse=i.index_inverse
         self.normDoc={}
         self.vide=True
         
     def getWeightsForDoc(self,idDoc):
         tfs= self.simpleIndex.getTfsForDoc(idDoc)
         res={}
         for stem in self.index_inverse.keys():
             if(stem in tfs.keys()):
                 res[stem]=tfs[stem]
             else:
                 res[stem]=0
         return res
     
     def getWeightsForStem(self,stem):
         return self.simpleIndex.getTfsForStem(stem)
     
     def getWeightsForQuery(self,query):
         w_tq={}
         te=TR.PorterStemmer()   
         qq=te.getTextRepresentation(query) 
         
         for stem in self.index_inverse.keys():
             if(stem in qq.keys()):
                 w_tq[stem]=1
             else:
                 w_tq[stem]=0
         return w_tq
     
             
             
             
class Weighter2(Weighter):
    
     """ 
     Schéma de pondération : wt,d = tft,d et wt,q = tft,q
     """
    
     def __init__(self,i):
         #i.indexation()
         self.simpleIndex=i
         self.index=i.index
         self.index_inverse=i.index_inverse
         
     def getWeightsForDoc(self,idDoc):
         tfs= self.simpleIndex.getTfsForDoc(idDoc)
         res={}
         for stem in self.index_inverse.keys():
             if(stem in tfs.keys()):
                 res[stem]=tfs[stem]
             else:
                 res[stem]=0
         return res
     
     def getWeightsForStem(self,stem):
         return self.simpleIndex.getTfsForStem(stem)
     
     def getWeightsForQuery(self,query):
         w_tq={}
         te=TR.PorterStemmer()   
         qq=te.getTextRepresentation(query) 
         
         for stem in self.index_inverse.keys():
             if(stem in qq.keys()):
                 w_tq[stem]=qq[stem]
             else:
                 w_tq[stem]=0
         return w_tq

class Weighter3(Weighter):
    
     """ 
     Schéma de pondération : wt,d = tft,d et wt,q = tft,q
     """
    
     def __init__(self,i):
         #i.indexation()
         self.simpleIndex=i
         self.index=i.index
         self.index_inverse=i.index_inverse
         
     def getWeightsForDoc(self,idDoc):
         tfs= self.simpleIndex.getTfsForDoc(idDoc)
         res={}
         for stem in self.index_inverse.keys():
             if(stem in tfs.keys()):
                 res[stem]=tfs[stem]
             else:
                 res[stem]=0
         return res
     
     def getWeightsForStem(self,stem):
         return self.simpleIndex.getTfsForStem(stem)
     
     def getWeightsForQuery(self,query):
         w_tq={}
         te=TR.PorterStemmer()   
         qq=te.getTextRepresentation(query) 
         
         for stem in self.index_inverse.keys():
             if(stem in qq.keys()):
                 w_tq[stem]=self.simpleIndex.getIDFForStem(stem)
             else:
                 w_tq[stem]=0
         return w_tq  

class Weighter4(Weighter):
    
     """ 
     Schéma de pondération : wt,d = 1 + log(tft,d) si t ∈ d, 0 sinon ; et wt,q = idft si t ∈ q, 0
     """
    
     def __init__(self,i):
         #i.indexation()
         self.simpleIndex=i
         self.index=i.index
         self.index_inverse=i.index_inverse
         
     def getWeightsForDoc(self,idDoc):
         tfs= self.simpleIndex.getTfsForDoc(idDoc)
         res={}
         for stem in self.index_inverse.keys():
             if(stem in tfs.keys()):
                 res[stem]=1+np.log(tfs[stem])
             else:
                 res[stem]=0
         return res
     
     def getWeightsForStem(self,stem):
         return self.simpleIndex.getTfsForStem(stem) 
     
     def getWeightsForQuery(self,query):
         w_tq={}
         te=TR.PorterStemmer()   
         qq=te.getTextRepresentation(query) 
         
         for stem in self.index_inverse.keys():
             if(stem in qq.keys()):
                 w_tq[stem]=self.simpleIndex.getIDFForStem(stem)
             else:
                 w_tq[stem]=0
         return w_tq             
                
class Weighter5(Weighter):
    
     """ 
     Schéma de pondération : wt,d = (1 + log(tft,d))x idft si t ∈ d, 0 sinon ; 
     et wt,q = (1 + log(tft,q))x idft si t ∈ q, 0.
     """
    
     def __init__(self,i):
         #i.indexation()
         self.simpleIndex=i
         self.index=i.index
         self.index_inverse=i.index_inverse
         
     def getWeightsForDoc(self,idDoc):
         tfs= self.simpleIndex.getTfsForDoc(idDoc)
         res={}
         for stem in self.index_inverse.keys():
             if(stem in tfs.keys()):
                 res[stem]=(1+np.log(tfs[stem]))*self.simpleIndex.getIDFForStem(stem)
             else:
                 res[stem]=0
         return res
     
     def getWeightsForStem(self,stem):
         return self.simpleIndex.getTfsForStem(stem)
     
     def getWeightsForQuery(self,query):
         w_tq={}
         te=TR.PorterStemmer()   
         qq=te.getTextRepresentation(query) 
         
         for stem in self.index_inverse.keys():
             if(stem in qq.keys()):
                 w_tq[stem]=(1+np.log(qq[stem]))*self.simpleIndex.getIDFForStem(stem)
             else:
                 w_tq[stem]=0
         return w_tq  


class IRModel():
    
     def __init__(self,w):
         self.weighter=w
     def getScores(self,query):
         pass
        
     def getRanking(self,query):
         pass
         
class Vectoriel(IRModel):
    
     def __init__(self,w,f=False):
         self.weighter=w
         self.normalized=f
         
     def getScores(self,query):
         if(self.normalized):
             return self.Score_Cosinus(query)
         else:
             return self.Score_produitMat(query)
         
     def getRanking(self,query):
         scores=self.getScores(query)
         return sorted(scores.items(), key=lambda t: t[1],reverse=True)
         
     def Score_produitMat(self,query):
         prod={}
         Q=self.weighter.getWeightsForQuery(query)
         for d in self.weighter.index.keys():
             D=self.weighter.getWeightsForDoc(d)
             prod[d]=np.dot((np.array(list(D.values()))).T,(np.array(list(Q.values()))))
         return prod 

     def Score_Cosinus(self,query):
         prod=self.Score_produitMat(query)
         nq=self.weighter.get_normQuery(query)
         for d in prod.keys():
             prod[d]=prod[d]/(sqrt(nq)+sqrt(self.weighter.get_normDoc(d)))
         return prod
     

class ModeleLangue(IRModel):
    
     def __init__(self,w):
         self.weighter=w

     def getScores(self,query):
         P_qd={}
         MC={}
         te=TR.PorterStemmer()   
         qq=te.getTextRepresentation(query) 
         if(sum(qq.values())>20):
             lamda=0.8
         else:
             lamda=0.2
         for stem in qq.keys():
             MC[stem]=self.weighter.proba_stemInC(stem)
         for d in self.weighter.index.keys():
             score=1
             for stem in qq.keys():
                 score*=(1-lamda)*self.weighter.proba_stemInD(stem,d)+(lamda*MC[stem])   
             P_qd[d]=score
         return P_qd   
     def getRanking(self,query):
         scores=self.getScores(query)
         return sorted(scores.items(), key=lambda t: t[1],reverse=True)
         

class Okapi(IRModel):
    
     def __init__(self,w, k1=1.2, b=0.75):
         self.weighter=w
         self.k1=k1
         self.b=b
         self.avgdl=0
         for d in self.weighter.index.keys():
             self.avgdl+=sum(self.weighter.index[d].values())
         self.avgdl=self.avgdl/len(self.weighter.index.keys())
     def getScores(self,query):
         
         te=TR.PorterStemmer()   
         qq=te.getTextRepresentation(query) 
         IDFs={}
         TFs={}
         S_dq={}
         for stem in qq.keys():
             IDFs[stem]=self.weighter.simpleIndex.getIDFForStem(stem)
             TFs[stem]=self.weighter.simpleIndex.getTfsForStem(stem)
         for d in self.weighter.index.keys():
             taille=sum(self.weighter.index[d].values())
             score=0
             for stem in qq.keys():
                 if d in TFs[stem].keys():
                     score+=IDFs[stem]*(TFs[stem][d]/(TFs[stem][d]+self.k1*(1-self.b+self.b*(taille/self.avgdl))))
             S_dq[d]=score
         return S_dq 
     
     def getRanking(self,query):
         scores=self.getScores(query)
         return sorted(scores.items(), key=lambda t: t[1],reverse=True)  
     

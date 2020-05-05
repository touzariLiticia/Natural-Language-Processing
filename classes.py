
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:00:23 2020

@author: TOUZARI
"""
import TextRepresenter as TR
import json
import numpy as np
from math import *

"""--------------TME1 """

class Document(object):
     def __init__(self,id,titre="",date="",auteur="",mc="",txt="",lien=""):
         self.id=id
         self.txt=txt
         self.titre=titre
         self.date=date
         self.auteur=auteur
         self.mc=mc
         self.txt=txt
         self.lien=lien
     def getId(self):
         return self.id
     def getText(self):
         return self.txt
     def affichage(self):
         print(self.id," : ",self.titre)
         
class Parser():
    def __init__(self):
        self.list_doc=[]
    def getDocuments(self,nomfichier):
        l=1
        fichier = open(nomfichier, "r")
        read=False
        lignes = fichier.readlines()
        fichier.close() 
        prem=True
        lien=''
        texte=''
        mot_cle =''
        auteur = ''
        titre = ''
        date=''
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
                    self.list_doc.append(Document(id,titre,date,auteur,mot_cle,texte,lien))  
                    lien=''
                    texte=''
                    mot_cle =''
                    auteur = ''
                    titre = ''
                    date=''
                    id='' 
                id=int(ligne[3:])
                prem=False
            if(ligne==".T"):
                read=True
                titre = lignes[l].strip()
                l+=1   
                
            if(ligne==".B"):
                read=True
                date = lignes[l].strip()
                l+=1 
                
            if(ligne==".A"):
                ligne = lignes[l].strip()
                l+=1
               
                while(l<len(lignes) and ligne[0:2]!=".C" and ligne[0:2]!=".I" and ligne[0:2]!=".T" and ligne[0:2]!=".B" and ligne[0:2]!=".A" and ligne[0:2]!=".W" and ligne[0:2]!=".X" and ligne[0:2]!=".K"):
                    auteur += ligne
                    ligne = lignes[l].strip()
                    l+=1
                    
                read=False
                
            if(ligne==".K"):
                ligne = lignes[l].strip()
                l+=1
                
                while(l<len(lignes) and ligne[0:2]!=".C" and ligne[0:2]!=".I" and ligne[0:2]!=".T" and ligne[0:2]!=".B" and ligne[0:2]!=".A" and ligne[0:2]!=".W" and ligne[0:2]!=".X" and ligne[0:2]!=".K"):
                    mot_cle += ligne
                    ligne = lignes[l].strip()
                    l+=1
                read=False
                
                    
            if(ligne==".W"):
                ligne = lignes[l].strip()
                l+=1
                while(l<len(lignes) and ligne[0:2]!=".C" and ligne[0:2]!=".I" and ligne[0:2]!=".T" and ligne[0:2]!=".B" and ligne[0:2]!=".A" and ligne[0:2]!=".W" and ligne[0:2]!=".X" and ligne[0:2]!=".K"):
                    texte += ligne
                    ligne = lignes[l].strip()
                    l+=1
                read=False
                
            if(ligne==".X"):
                
                ligne =lignes[l].strip()
                l+=1
                while(l<len(lignes) and ligne[0:2]!=".C" and ligne[0:2]!=".I" and ligne[0:2]!=".T" and ligne[0:2]!=".B" and ligne[0:2]!=".A" and ligne[0:2]!=".W" and ligne[0:2]!=".X" and ligne[0:2]!=".K"):
                    lien += ligne
                    ligne = lignes[l].strip()
                    l+=1
                read=False
            if(ligne==".C"):
                
                ligne = lignes[l].strip()
                l+=1
                while(l<len(lignes) and ligne[0:2]!=".I" and ligne[0:2]!=".T" and ligne[0:2]!=".B" and ligne[0:2]!=".A" and ligne[0:2]!=".W" and ligne[0:2]!=".X" and ligne[0:2]!=".K"):
                    ligne = lignes[l].strip()
                    l+=1
                read=False
        
        return 
    def affichage_docs(self):
        for d in self.list_doc:
            d.affichage()
        
             
        
class IndexerSimple (object):
    def __init__(self,corp):
        self.corpus=corp
        self.index={}
        self.index_inverse={}
    def indexation(self):
        index= dict()
        index_inverse=dict()
        Trep=TR.PorterStemmer ()
        for doc in self.corpus :
            terms= Trep.getTextRepresentation(doc.getText())
            doc_id= doc.getId()
            index[doc_id] = terms
            for t in terms.keys():
                if (t in index_inverse.keys()):
                    if(doc_id in index_inverse[t].keys()):
                        index_inverse[t][doc_id] += terms[t]
                    else:
                        index_inverse[t][doc_id]= terms[t]
                else:
                    index_inverse[t]={}
                    index_inverse[t][doc_id]=terms[t]
        self.index=index
        self.index_inverse =index_inverse
        
    def sauve(self):
        fichier_index = open("index.txt", "a")
        fichier_index_inverse = open("index_inverse.txt", "a")
        json.dump(self.index,fichier_index)
        json.dump(self.index_inverse,fichier_index_inverse)
        fichier_index.close()
        fichier_index_inverse.close()

    def getTfsForDoc(self,idDoc):
        return self.index[idDoc]
    
    def getTfIDFsForDoc(self,idDoc):
        tfs=self.index[idDoc]
        N=len(self.index)
        idf={}
        tf_idf={}
        for m in tfs.keys():
            idf[m]=np.log((1+N)/(1+len(self.index_inverse[m])))   
            tf_idf[m]=tfs[m]*idf[m]
        return tf_idf
    def getTfsForStem(self,stem):
        return self.index_inverse[stem]
    def getTfIDFsForStem(self,stem):
        tfs=self.index_inverse[stem]
        N=len(self.index)
        df=len(tfs)
        idf=np.log((1+N)/(1+df))  
        tf_idf={}
        for d in tfs.keys():
            tf_idf[d]=tfs[d]*idf
        return tf_idf
    def getIDFForStem(self,stem):
        tfs=self.index_inverse[stem]
        N=len(self.index)
        df=len(tfs)
        idf=np.log((1+N)/(1+df))   
        return idf
    def getStrDoc(self,doc):
        return doc.txt
    
               
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

     def getScores(self,query):
         #for stem in self.weighter.index.keys():
         return    
     def getRanking(self,query):
         scores=self.getScores(query)
         return sorted(scores.items(), key=lambda t: t[1],reverse=True)    

          
        
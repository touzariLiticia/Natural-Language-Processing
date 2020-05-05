#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 17:35:09 2020

@author: TOUZARI
"""
from TextRepresenter import *
import json
from classes import *

#EXERCICE 1 

# 1. On interroge l'index direct pour avoir un calcule du score pertinent

p=Parser()
p.getDocuments("data/cisi/cisi.txt")   
i=IndexerSimple(p.list_doc) 
i.indexation()

# 2. Calculer le score des documents à partir du modèle booléen
"""
q = 'home sales top'
print('Le score de chaque document : ',get_score_bool(q,i.index))
"""

# 3. Calculer le score des documents `a partir du modèle vectoriel  
"""
print('Le score de chaque document : ',get_score_vect_InnerProduct(q,i.index))            
print('Le score de chaque document : ',get_score_vect_DiceCoef(q,i.index))       
print(get_score_vect_DiceCoef('home sale top',{1:{'home':5}, 2:{'sale':2,'home':1}}))  
"""
  
#EXERCICE 2 

# 1. Représentation pondérée des documents et de la requête

q = 'home home sales top'

w1=Weighter1(i)   
#w_tq1=w1.getWeightsForQuery(q)
#print(w_tq1) 
"""
w2=Weighter2(i)   
w_tq2=w2.getWeightsForQuery(q)
print(w_tq2['home'])  

w3=Weighter3(i)   
w_tq3=w3.getWeightsForQuery(q)
print(w_tq3)  

w4=Weighter4(i)   
w_tq4=w4.getWeightsForQuery(q)
w_td4=w4.getWeightsForDoc(1)
print(w_tq4['home'],w_td4['home'])

w5=Weighter5(i)   
w_tq5=w5.getWeightsForQuery(q)
w_td5=w5.getWeightsForDoc(1)
print(w_tq5['home'],w_td5['home'])"""
    
# 2. Modèles de RI 
 
q = 'home home sales top'

# Modèle Vectoriel
"""
vec=Vectoriel(w1,False)
print('Le score du modèle vectoriel : ',vec.getScores(q))
print('Liste de coupes (document-score) ordonnée par score décroissant : ',vec.getRanking(q))  

vec=Vectoriel(w1,True)
print('Le score du modèle vectoriel : ',vec.getScores(q))
print('Liste de coupes (document-score) ordonnée par score décroissant : ',vec.getRanking(q))  
"""

# Modèle de langue (lissage Jelinek-Mercer))   

ml=ModeleLangue(w1)
print('Le score du modèle vectoriel : ',ml.getScores(q))
print('Liste de coupes (document-score) ordonnée par score décroissant : ',ml.getRanking(q)) 

# Modèle Okapi 
    
    
    
    
    
    
    
    
    
    

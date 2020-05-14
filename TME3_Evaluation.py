#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 16:49:03 2020

@author: TOUZARI
"""

from TextRepresenter import *
import json
from classes_TME1 import *
from classes_TME2 import *
from classes_TME3 import *

# Exercice 2
# 1. Chargement du jeu de donnees
Q=QueryParser()
d=Q.getQueries("data/cisi/cisi.qry","data/cisi/cisi.rel")
"""for q in d:
    q.affiche()"""
    
# 2 Métriques
p=Parser()
p.getDocuments("data/cisi/cisi.txt")   
i=IndexerSimple(p.list_doc)
i.indexation()
w1=Weighter1(i)     
modele=Vectoriel(w1,False)

# Précision
k=20
query=d[0]
liste=modele.getRanking(query.txt)
"""
pres=Precision(20)
print('Precision de la requete 1 :',pres.evalQuery(liste,query))
rap=Rappel(20)
print('Rappel de la requete 1 :',rap.evalQuery(liste,query))
fm=F_mesure(20,0.5)
print('F-mesure de la requete 1 :',fm.evalQuery(liste,query))
presMoy=PrecisionMoy()
print('Precision Moyenne de la requete 1 :',presMoy.evalQuery(liste,query))
res=reciprocalRank(d)
print('Reciprocal Rank :',res.evalQuery(modele))"""

# 3 Plateforme d’évaluation
Eval=EvalIRModel(d)
print('Evaluation de a précision pour le modéle vectoriel :',Eval.Eval_Precision(k,modele))

# 4 Bonus



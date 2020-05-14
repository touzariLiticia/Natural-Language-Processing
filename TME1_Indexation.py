#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:42:45 2020

@author: TOUZARI
"""
from TextRepresenter import *
import json
from classes_TME1 import *


#EXERCICE 1


#EXERCICE 2


#EXERCICE 3
#--------------Parsing de la collection

p=Parser()
p.getDocuments("data/cisi/cisi.txt")   
#p.affichage_docs()

#--------------Indexation

i=IndexerSimple(p.list_doc)  
i.indexation()      
print(i.index[1])
print(i.index_inverse['present'])

print('La représentation (stem-tf) d’un document : ',i.getTfsForDoc(1))
print('La représentation (stem-TFIDF) d’un document : ',i.getTfIDFsForDoc(1))
print('La représentation (doc-TFIDF) d’un stem  : ',i.getTfsForStem('present'))
print('La représentation (doc-TFIDF) d’un stem : ',i.getTfIDFsForStem('present'))

#---------------Bonus
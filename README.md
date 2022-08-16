
# ClinicalNLP
Natural Language Processing within Python for symptom extraction of clinical text


## Overview
This project maps clinical text to existing biomedical corpora through various Unified Medical Language System (UMLS) technologies. All code is in python

## API Requirements and Resources:  
1.	Python-based web API for MetaMap: SKR Web API 
      -  Packages Required: requests, requests html
      - [Click for instructions on and installing the MetaMap API](https://github.com/lhncbc/skr_web_python_api)
2.    UMLS REST API 
      - Packages required: requests, json, argparse, pyquery, lxml 
      - [Click for sample code using UMLS REST API](https://github.com/HHS/uts-rest-api/tree/master/samples/python)
      - [UMLS REST API technical documentation](https://documentation.uts.nlm.nih.gov/rest/home.html)

## Python Scripts: 

### **metamap-api** 

Parameters: a deidentified clinical note `.txt`. The code utilizes MetaMap to perform biomedical NLP. MetaMap identifies concepts in clinical text, mapping them to over 200 dictionaries in the UMLS Metathesaurus. Negation handling (NegEx) is included in this process. 

Output: a `.txt` file with  mappings for each identified sign or symptom in the note. For each term, the output file displays: 
- Preferred term name 
- Concept Unique Identifier (CUI) 
- Additional information



### **cui-search**
Parameters: list of CUIs and term names. The script accesses the concept mappings of each CUI within the SNOMED-CT ontology. This ontological structure can be described as a graph of connected terms. 

Output: a `.txt` file for *each* CUI in the input list. For each term, the output file displays: 
- Related ID name
- ui (SNOMED-CT unique identifier) 
- Source Vocabulary (this will be SNOMED-CT) 
- Relation Label
- Related ID 




# ClinicalNLP
Natural Language Processing within Python for symptom extraction of clinical text


## Overview
      here, i will state the overview of my project

## APIs used:  
1.	Python-based web API for MetaMap: SKR Web API 
      -  Packages Required: requests, requests html
      - Link to instructions on building and installing the api:https://github.com/HHS/uts-rest-api/tree/master/samples/python 
2.    UMLS REST API 
      - Packages required: requests, json, argparse, pyquery, lxml 
      - Link to samples that code was built on: https://github.com/HHS/uts-rest-api/tree/master/samples/python
      - Link to UMLS API technical documentation: https://documentation.uts.nlm.nih.gov/rest/home.html

## Python Scripts: 

### metamap-api 

takes in a deidentified clinical note (in the form of a text file) and utilizes MetaMap to perform biomedical mapping to the UMLS Metathesaurus. The program outputs a text file with formatted mappings for each identified entity (sign or symtpom)in the note; this output includes the preferred term name, CUI, and additional information. The output file will be subsequently used by ‘cui-search.py’ to search SNOMED-CT.


### cui-search
takes in concept unique identifier (CUI) and preferred term name -- maps to SNOMED-CT ontology, outputting text file

**a concept unique identifier is a code used to tag clinical terms in biomedical dictionaries**



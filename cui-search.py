#---------------------------------------------------------------------------------------------------------------------------------------
#Alina Zatzick -- CUI SEARCH code
# usage: CUI lookup that uses umls REST api to access SNOMED ontology
# parameters: -i INPUTFILE -k APIKEY -v VERSION -s SOURCE -o OUTPUTFILE
#           If you do not provide the -s parameter, the program assumes you are using UMLS cui
# output: text file for each CUI in the input list, containing concept mappings
#---------------------------------------------------------------------------------------------------------------------------------------

from Authentication import *
import requests
import json
import argparse
import pandas as pd
import sys
import os

parser = argparse.ArgumentParser(description='process user given parameters')
parser.add_argument("-v", "--version", required =  False, dest="version", default = "current", help = "enter version example-2015AA")
parser.add_argument("-i", "--inputfile", required=True, dest="inputfile", help="enter input file")
parser.add_argument("-s", "--source", required =  False, dest="source", help = "enter source name if known")
args = parser.parse_args()


apikey = 'a90cc3d1-d392-4903-bf9a-228a8ac8802e'             #ENTER PERSONAL API KEY HERE
version = args.version

#Enter full filepath of input file (METAMAP OUTPUT)
inputfile = '/Users/alinazatzick/Desktop/HMC Summer 2022/MetaMap-CuiSearch/OUTPUT/MetaMap' + "/" + args.inputfile

#Replace with filepath of where you would like your output file to be located
outputfile= '/Users/alinazatzick/Desktop/HMC Summer 2022/MetaMap-CuiSearch/OUTPUT/CuiSearch' 
 
source = args.source
sabs = 'SNOMEDCT_US'                                       
uri = "https://uts-ws.nlm.nih.gov"

#---------------------------------------------------------------------------------------------------------------------------------------
#Function to load the inputfile and read into a list
#---------------------------------------------------------------------------------------------------------------------------------------
def importFile (inputfile):
    cui_df = pd.read_csv(inputfile, 
                sep = ",",
                header = 0)
    cui_list = cui_df.itertuples()
    return cui_list 

#---------------------------------------------------------------------------------------------------------------------------------------
#Search function to return SNOMED ontology from specified CUI
#Accesses UMLS REST API to complete search
#Returns text file for each CUI's concept relations  
#---------------------------------------------------------------------------------------------------------------------------------------
def cuiSearch(cui):
    #termname 
    identifier = cui[2]
    term_name = cui[1]
    
    outputfile1 = outputfile + "/" + term_name + ".txt"
    
    #Acessing UMLS REST API
    AuthClient = Authentication(apikey)
    tgt = AuthClient.gettgt()
    pageNumber=1
    content_endpoint = "/rest/content/"+str(version)+"/CUI/"+str(identifier)+"/relations?sabs="+str(sabs)
    
    #Printing search results to outputfile
    sys.stdout=open(outputfile1,"w")
    print("\nSearch results for term: " + term_name + "\tCUI:" + identifier +  '\n\n')

    while True:
        
        query = {'ticket':AuthClient.getst(tgt),'pageNumber':pageNumber}
        r = requests.get(uri+content_endpoint,params=query)
        r.encoding = 'utf-8'
        
        ###################################
        #JSON FILE OUTPUT
        ###################################
        
        items  = json.loads(r.text)
        json_string = json.dumps(items, indent = 4)
        #print((json_string))
    
        ###################################
        #PRINT OUTPUT
        ###################################
        
        pageCount=items["pageCount"] 

        print("PageNumber" + str(pageNumber)+"\n")
        for result in items["result"]:
            try: 
                print("Related ID Name: " + result["relatedIdName"])
            except:
                NameError
            try:
                print("ui: " + result["ui"])
            except:
                NameError
            try:
                print("Source Vocabulary: " + result["rootSource"])
            except:
                NameError
            try:
                print("Relation Label: " + result["relationLabel"])
            except:
                NameError
            try: 
                print("Related ID: " + result["relatedId"] )
            except:
                NameError
            print("\n")
            
        pageNumber += 1
            
        if pageNumber > pageCount:
            print("End of result set")
            break 
    print("*********") 
    
    sys.stdout.close()

# MAIN FUNCTION----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
def main():
    #calling functions
    cui_list = importFile(inputfile)
    for elem in cui_list:
       cuiSearch(elem)

if __name__ == "__main__":
    main()
#---------------------------------------------------------------------------------------------------------------------------------------
#Alina Zatzick -- MetaMap implementation 
# usage: Accesses UMLS python API to get MetaMap output for each term in a given clinical note
# parameters: -i INPUTFILE -k APIKEY -s SERVICE URL
#           If you do not provide the -s parameter, the program assumes you are using metamap_interactive_url (provided by UMLS)
# output: text file containing MetaMap output for the input note
#---------------------------------------------------------------------------------------------------------------------------------------

import argparse
import os 
from io import StringIO
from tabulate import tabulate
import numpy
import pandas as pd
from skr_web_api import Submission, METAMAP_INTERACTIVE_URL

parser = argparse.ArgumentParser(description="MetaMap test authorization")
parser.add_argument("-s", "--serviceurl", required=False, default=METAMAP_INTERACTIVE_URL, help="url of service")
parser.add_argument("-i", "--inputfile", required = True, help = "input file")

args = parser.parse_args()
serviceurl = args.serviceurl

apikey = 'a90cc3d1-d392-4903-bf9a-228a8ac8802e'                  #ENTER PERSONAL API KEY HERE
email = 'alinazat@uw.edu'                                        #ENTER PERSONAL EMAIL HERE

#ENTER PATH TO INPUT FILE HERE
inputfile =  '/Users/alinazatzick/Desktop/HMC Summer 2022/MetaMap-CuiSearch/Deidentified_files_for_Onedrive' + "/" +  args.inputfile 
outputfile = '/Users/alinazatzick/Desktop/HMC Summer 2022/MetaMap-CuiSearch/OUTPUT/MetaMap/' + "MetaOUT" + args.inputfile

#CHANGING PANDAS SETTINGS FOR TABLE DISPLAY
pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', None)
pd. set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

#---------------------------------------------------------------------------------------------------------------------------------------
#Accessing MetaMap API
#Functions: 
#           1) read_input    --> reads input file into python  
#           2) mm_excecution --> harnesses python api for metamap, returns MMI output 
#           3) write_to file --> OPTIONAL funciton to write raw MMI output to text file
#---------------------------------------------------------------------------------------------------------------------------------------
def read_input(inputfile):
    with open(inputfile, "r") as f:
        note = f.read().replace('\n', '')
    return note

#parameters = input text, serviceurl (umls_metamap), email, apikey
#output = raw MMI output 
def mm_excecution(inputtext, serviceurl, email, apikey):
    inst = Submission(email, apikey)
    if serviceurl:
        inst.set_serviceurl(serviceurl)
    
    inst.init_mm_interactive(inputtext, args='-N')
    response = inst.submit()
    
    print('response status: {}'.format(response.status_code))                       #printing response code (200 if successful)
    MMI_output = (format(response.content.decode()))
    #print(MMI_output)                                                              #option to print raw MetaMap output
    return(MMI_output)

def write_to_file(MMI_output):
    with open(outputfile, "w") as f:
        f.write(MMI_output)

#---------------------------------------------------------------------------------------------------------------------------------------
# Formatting MMI output into Data Frame and readable outputFile
# create_df = PARENT function to create df from mmi output
# parameters = metamap raw output
# output = data frame
#---------------------------------------------------------------------------------------------------------------------------------------
def create_df(MMI_output):
    df_MMI = StringIO(MMI_output)
    df = pd.read_csv(df_MMI, 
                     sep="|",header=0, 
                     names=['User', 'MMI', 'score', 'Preferred Term Name', 'CUI', 'Semantic type', 'information', 'place', 'not sure', 'date'],
                     usecols=['Preferred Term Name', 'CUI', 'Semantic type', 'information'])
    df1 = negation(df)
    df2 = df_duplicates(df1)
    
    #print(tabulate(df2, headers = 'keys'))                                    #option to print df
    return df2

#---------------------------------------------------------------------------------------------------------------------------------------
# Function to narrow down semantic types into signs and symptoms only
# parameters = data frame
# output = select data frame with rows with semantic type == 'sosy' (signs and symptoms)
#---------------------------------------------------------------------------------------------------------------------------------------
def signsSymptoms(df):
    df['Semantic type'] = df['Semantic type'].astype('string')
    
    sosy_df = df[df['Semantic type'].str.contains('sosy')]
    print(tabulate(sosy_df, headers = 'keys')) 
    return sosy_df

#---------------------------------------------------------------------------------------------------------------------------------------
# Function to handle negation in data frame, called by create_df (above)
#---------------------------------------------------------------------------------------------------------------------------------------
def negation(df): 
    df['information'] = df['information'].astype('string')
   
    #if negation tagger is present 
    negations = df[df['information'].astype(str).str.contains('-1]')]
    df_new = df[~df['information'].isin(negations['information'])]
    
    other_negations = df_new[df_new['information'].astype(str).str.contains('No"-tx')]
    df_new = df_new[~df_new['information'].isin(other_negations['information'])] 

    return df_new 

#---------------------------------------------------------------------------------------------------------------------------------------
# Function to eliminate duplicates in CUIs / terms
#---------------------------------------------------------------------------------------------------------------------------------------
def df_duplicates(df):
    df.drop_duplicates(subset="CUI", keep = False, inplace=True)
    return df

#---------------------------------------------------------------------------------------------------------------------------------------
# Returns a text file containing MetaMap information
#---------------------------------------------------------------------------------------------------------------------------------------
def output(df1):
    #specify specific file path
    df1.to_csv(outputfile, 
               columns = ['Preferred Term Name', 'CUI'],      #pairing down to preferred term name and CUI
               sep = ",",
               index = False),
               
# MAIN FUNCTION----------------------------------------------------------------------------------------------------------------------------------------------   
def main():
    #calling above methods
    input_text = read_input(inputfile)
    MMI_output = mm_excecution(input_text, serviceurl, email, apikey)
    
    df1 = create_df(MMI_output)                             #write_to_file(MMI_output)
    df2 = signsSymptoms(df1)                                #right now this is writing SOSY
    output(df2)
   
if __name__ == "__main__":
    main()
    
    

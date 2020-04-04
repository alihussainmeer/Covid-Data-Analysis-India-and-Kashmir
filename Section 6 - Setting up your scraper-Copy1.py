#!/usr/bin/env python
# coding: utf-8

# # Set-up

# In[33]:


import pandas as pd
from tabula import read_pdf
import numpy as np
import re

df = read_pdf('https://www.mohfw.gov.in/pdf/DistrictWiseList324.pdf',multiple_tables=True,stream =True,pages = 'all',guess=False)
districts = ['Srinagar','Budgam','Pulwama','Baramulla','Shopian','Bandipora','Jammu','Rajouri','Udhampur'] # change to add your districts


df = df[1].copy()
report2 = df[df[df.columns[-2]].isin(districts)]


total_districts = report2[report2.columns[1]].dropna().unique().astype(int).max()
total_districts


if total_districts> 9 :
    print('Warning : You need to add more districts')

final = report2[[report2.columns[-2],report2.columns[-1]]]
final.columns =['District','Positive Cases'] 
final['Positive Cases'] = final['Positive Cases'].astype(int)
#final contains the data from districts which we fetched from pdf file

statewise = (pd.read_html('https://www.mohfw.gov.in')[0]).set_index('S. No.')
statewise = statewise.iloc[:-2,:]

target = statewise.columns[1]
foreign_history = int(''.join(re.findall('[1-9]',target)))
foreign = pd.DataFrame()
foreign['Foreign Travel History'] = [foreign_history]



totals = statewise.iloc[-2:-1,:] #a totals to be kept in a separate df
statewise[[statewise.columns[1],statewise.columns[2],statewise.columns[3]]] = statewise[[statewise.columns[1],statewise.columns[2],statewise.columns[3]]].astype(int)

statewise['Death Rate']=statewise['Death']/statewise['Total Confirmed cases (Including 65 foreign Nationals)']
statewise['Recovery Rate'] = statewise['Cured/Discharged/Migrated']/statewise['Total Confirmed cases (Including 65 foreign Nationals)']
statewise.rename(columns={
    'Name of State / UT': 'State/Union Territory'
},inplace=True)

states_data_pop = pd.read_csv('state-pop.csv').drop(columns='Unnamed: 0')
statewise = statewise.merge(states_data_pop,how = 'left',on='State/Union Territory')
#statewise contains the data statewise after merging it with wiki data 
##################################################################################################################################

import gspread
import gspread_dataframe as gd
from oauth2client.service_account import ServiceAccountCredentials



#fetching the data from google sheets into the dataframe
def update_credit_page(other,sheetname = 'Sheet1'):
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    #----------------------------Need to send this to Rubys Laptop---------------------------
    
    #replace the filepath with the file you download from credentials file
    #also create spreadsheet with the name of the sheets given below
    credentials = ServiceAccountCredentials.from_json_keyfile_name(file_path, scope)
    gc = gspread.authorize(credentials)
    #-----------replace with the actual spreadsheet name -----------
    ws = gc.open("corona").worksheet(sheetname)
    
    gd.set_with_dataframe(ws, other)
    print("Corona :"+str(sheetname) +" :Sheet updated") 



update_credit_page(final,sheetname='District')#sheet1

update_credit_page(statewise,sheetname='state')#sheet2

update_credit_page(totals,sheetname='totals') #sheet3

update_credit_page(foreign,sheetname='foreign')#--sheet4





#wiki data for states population and code
'''
tmp = pd.read_html('https://en.wikipedia.org/wiki/States_and_union_territories_of_India')

cols = [['State/Union Territory','ISO 3166-2:IN','Population[40]']]
tmp1 = tmp[4][['Union territory','ISO 3166-2:IN','Population[40]']]
tmp2 = tmp[3][['State','ISO 3166-2:IN','Population[40]']]

tmp1.columns = cols
tmp2.columns = cols

states_data_pop = tmp1.append(tmp2)


'''


# In[84]:





# In[ ]:





# In[ ]:





# In[ ]:





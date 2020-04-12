#!/usr/bin/env python
# coding: utf-8

# # Set-up

# In[ ]:


import pandas as pd
from tabula import read_pdf
import numpy as np
import re
import time
import requests_html

session = requests_html.HTMLSession()
r = session.get('https://www.mohfw.gov.in/')
k =[i.links for i in r.html.find('a[href*=DistrictWise]')]
url = str(k[0]).strip("{''}")

for i in [1]:
    #time.sleep(3600)
    df = read_pdf(url,multiple_tables=True,stream =True,pages = 'all',guess=False)
    
    dfs = pd.DataFrame()
    dfs = df[1].iloc[0]
    dfs = dfs.T.reset_index().T
    for i in df[1:]:
        i  = i.T.reset_index().T
        dfs = dfs.append(i)

    dfs = dfs[~(dfs[0] == 'Unnamed: 0')]
    dfs = dfs.reset_index(drop = True)

    dfs = dfs.iloc[:-2]

    df=dfs.copy()

    tmpo = df[df[df.columns[0]]=='JAMMU AND KASHMIR']
    number_dist = int(tmpo[tmpo.columns[1]].values[0].strip('*'))

    tmp_ind = tmpo.index.values[0]

    ind = number_dist
    print(ind)
    divi = ind / 2
    if (divi)-int(divi) > 0 :
        upper = divi
        lower = divi+1
    else:
        upper = divi
        lower = divi

    upper,lower = int(upper),int(lower)
    print(upper,lower)
    df = df.iloc[(tmp_ind-upper):(tmp_ind+lower)]
    #districts = ['Srinagar','Badgam','Kulgam','Pulwama','Baramulla','Shopian','Bandipora','Jammu','Rajouri','Udhampur','Ganderbal','Kupwara'] # change to add your districts

    print(df.shape)
    #df = df[2].copy()
    #df.loc[-1] = df.columns
    df[df.columns[-2]] = df[df.columns[-2]].apply(lambda x: str(x).title())
    #report2 = df[df[df.columns[-2]].isin(districts)]


    total_districts = df[df.columns[1]].dropna().unique()
    total_districts


    '''if total_districts> 11 :
        print('Warning : You need to add more districts')'''

    final = df[[df.columns[-2],df.columns[-1]]]
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

    statewise['Death Rate']=statewise['Death']/statewise[statewise.columns[2]]
    statewise['Recovery Rate'] = statewise['Cured/Discharged/Migrated']/statewise[statewise.columns[2]]
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
        credentials = ServiceAccountCredentials.from_json_keyfile_name(enter the path to your json key , scope)
        gc = gspread.authorize(credentials)
        #-----------replace with the actual spreadsheet name -----------
        ws = gc.open("corona").worksheet(sheetname)

        gd.set_with_dataframe(ws, other)
        print("Corona :"+str(sheetname) +" :Sheet updated")

    cols = ['State/Union Territory',
       'Total Confirmed cases (Including 65 foreign Nationals)',
       'Cured/Discharged/Migrated', 'Death', 'Death Rate', 'Recovery Rate',
       'ISO 3166-2:IN', 'Population[40]']
    statewise.columns = cols
    statewise[statewise.columns[0]] = statewise[statewise.columns[0]].apply(lambda x : str(x).upper())
    
    update_credit_page(final,sheetname='District')

    update_credit_page(statewise,sheetname='state')

    update_credit_page(totals,sheetname='totals')

    update_credit_page(foreign,sheetname='foreign')





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


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





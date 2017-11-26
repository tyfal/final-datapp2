#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 22:15:57 2017

@author: tfalcoff
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup

text = "net income"

url = 'https://www.sec.gov/Archives/edgar/data/277135/000027713512000008/gww20111231-10k.htm'

r = requests.get(url)
    
soup = BeautifulSoup(r.text,'html.parser')

def tables(soup):
    
    return soup.find_all('table')

def form_dig(text, soup):
    
    tables = soup.find_all('table')
    
    table_df = pd.read_html(str(tables).lower())
    
    data = []
    
    count = 0
    
    for table in table_df:
        
        for col in table:
                            
            try:
                                
                search = table[col].str.contains(text, na=False)
                                
                if search.any():
                    
                    data.append(table_df[count].loc[search].dropna(axis=1, how='all'))
                               
            except AttributeError:
                                
                pass
        
        count += 1
        
    return data


def form_context(text, soup):
    
    con_list = []
        
    form_list = soup.getText().lower().split()
        
    count = 0
    
    for word in form_list:
        
        if word == 'consolidated':
            
            con_list.append(count)
            
        count += 1
                
    text_list = []
                
    count = 0
    
    len_text = len(text.split())
    
    for word in form_list:
        
        if ' '.join(form_list[count:count+len_text]) == text:
            
            text_list.append(count)
            
        count += 1 
        
    context = []
            
    for t in text_list:
            
        dif_list = []
            
        for c in con_list:
                
            dif_list.append(t - c)
                
        context.append(dif_list)
        
    return context


def data_mine(data, text):
    
    mined_list = []
    
    for x in data:
        
        try:
        
            for y in x[0]:
                
                mined_list.append(y)
            
        except KeyError:
            
            pass
        
    return mined_list
    

data = form_dig(text, soup)

context = form_context(text, soup)

titles = data_mine(data, text)

    
        


    

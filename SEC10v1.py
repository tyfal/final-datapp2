#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 19:59:13 2017

@author: tfalcoff
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 20:27:14 2017

@author: tfalcoff
"""

import requests, re, math, string
import pandas as pd
from bs4 import BeautifulSoup

#ticker = 'F'    
#form_type = "10-K"
#end_date = "2017-6-22"


def form_count_calc(form_type, start_date="YYYY-MM-DD", end_date="YYYY-MM-DD"):
    
    start = []
    
    [start.append(int(denom)) for denom in start_date.split("-")]
    
    end = []
    
    [end.append(int(denom)) for denom in end_date.split("-")]
    
    month_dif = (end[0]*12+end[1]) - (start[0]*12+start[1])
    
    if form_type.upper() == "10-Q":
        
        form_count = month_dif//4
        
    if form_type.upper() == "10-K":
        
        if (month_dif/12 - month_dif//12) >= .25:
            
            form_count = math.ceil(month_dif/12)
        
        else:
            
            form_count = month_dif//12
            
    priorto = end_date.replace("-","")
    
    return {"form_count":form_count, "priorto":priorto}


def get_form(ticker, form_type, priorto=""):

    base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+ticker+"&type="+form_type+"&dateb="+priorto+"&owner=exclude&count=40"
    
    r = requests.get(base_url, timeout=.5)
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    doc_buttons = soup.find_all(id="documentsbutton")
    
    links = []
    
    for button in doc_buttons:
        
        links.append(button.get("href"))
        
    form_links = []
    
    for l in links:
    
        r2 = requests.get("https://www.sec.gov"+l, timeout=.5)
        
        soup2 = BeautifulSoup(r2.text, "html.parser")
        
        if form_type == "10-Q":
        
            anchor = soup2.find("a",string=re.compile("q.htm"))
            
            if anchor == None:
                
                anchor = soup2.find("a",string=re.compile("10-q.htm"))
                
        if form_type == "10-K":
        
            anchor = soup2.find("a",string=re.compile("k.htm"))
            
            if anchor == None:
                
                anchor = soup2.find("a",string=re.compile("10-k.htm"))
                
        if anchor != None:
                
            form_links.append("https://www.sec.gov"+anchor.get("href"))
    
    return form_links
'''   
priming = form_count_calc(form_type, start_date="2016-1-1", end_date="2017-6-22")

form_links = get_form(ticker, form_type, priorto=priming['priorto'])[:priming['form_count']]

print(form_links)
'''
def ten_k_dig(form_links, text):

    r = requests.get(form_links[0], timeout=.5)
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    form_body = soup.find("body")
    
    body_level_elements = form_body.find_all(recursive=False)
    
    look_for_rows = False
    
    for element in body_level_elements:
        
        if "consolidated" in str(element).lower(): #may only work for arguments in consolidated info tables
            
            look_for_rows = True
            
            look_count = 0
            
        if look_for_rows and look_count < 2:
            
            look_count += 1
            
            element_rows = element.find_all("tr")
    
            for row in element_rows:
                
                row_text = row.getText()
                
                alpha_count = 0
                
                digit_count = 0
                
                for char in row_text.lower():
                    
                    if char in string.ascii_lowercase:
                        
                        alpha_count += 1
                        
                    if char in string.digits:
                        
                        digit_count += 1
                        
                year_list = []
                        
                if alpha_count == 0 and digit_count > 0:
                    
                    year_list.append(row_text.split())
                    
                    if len(year_list[-1][0]) == 4 and len(year_list[-1]) > 1:
                        
                        if int(year_list[-1][0]) + 1 == int(year_list[-1][1]):
                            
                            ascending = True
                            
                        else:
                            
                            ascending = False
                
                if text.lower() in row_text.lower() and look_for_rows and len(row_text)<200:
                    
                    digit_string = ''
                    
                    for char in row_text:
                        
                        if char not in string.ascii_letters + "$":
                            
                            digit_string += char
                    
                    metric_list = digit_string.split()
                    
                    form_date = soup.find(string=re.compile("For the fiscal year ended"))
                    
                    try:
                    
                        recent = int(form_date.split()[-1])
                        
                    except ValueError:
                        
                        form_date = form_date.findNext().getText()
                        
                        recent = int(form_date.split()[-1])
                    
                    row_parent = row.parent
                    
                    table_df = pd.read_html(str(row_parent))[0]
                    
                    years = table_df.loc[0].dropna().values
                    
                    inc = []
                    
                    for col in table_df:
                        
                        try:
                           
                           inc.append(table_df[col].str.contains(text, na=False))
                           
                        except AttributeError:
                            
                            pass
                    
                    print(years)
                    
                    for i in inc:
                        
                        print(table_df.loc[i].dropna(axis=1, how='all'))
                        
                        break
                    
                    for row2 in row_parent.find_all("tr"):
                        
                        if str(recent) in row2.getText():
                            
                            print(row2.getText())
                            
                            break
                    
                    if ascending:
                        
                        year_list = []
                        
                        metric_count = len(metric_list) - 1
                        
                        for metric in metric_list:
                            
                            year_list.append(int(recent)-metric_count)
                            
                            metric_count -= 1
                        
                    else:
                        
                        year_list = []
                        
                        metric_count = 0
                        
                        for metric in metric_list:
                            
                            year_list.append(int(recent)-metric_count)
                            
                            metric_count += 1
                            
                    print(year_list)
                
                    return list(zip(year_list, metric_list))
                
                
def recentIS(s, form_type):
    
    ticker = s.stock_symbol
    end_lst = s.financial().str_date[-1].split("-")
    end = "-".join([end_lst[2], end_lst[0], end_lst[1]])
    start_lst = s.financial().str_date[0].split("-")
    start = "-".join([start_lst[2], start_lst[0], start_lst[1]])
    
    table_list = []
    
    text = ["income", "total", "net"]
    
    table = "After battling the interweb... it won d[-_-]b"
    
    try:
        
        priming = form_count_calc(form_type, start_date=start, end_date=end)

        form_links = get_form(ticker, form_type, priorto=priming['priorto'])[:priming['form_count']]

        r = requests.get(form_links[0], timeout=.5)

        soup = BeautifulSoup(r.text,'html.parser')

        for t in soup.find_all('table'):

            txtCount = 0

            for txt in text:

                if txt in str(t).lower() and len(t) < 100000:

                    txtCount += 1

            if txtCount == len(text):

                table = str(t).replace("\n"," ")

                table += "<br><br>"

                break
                
    except:
                
        pass
        
    return table
    
    '''        
    for url in form_links:
        
        try:

            r = requests.get(url)

            soup = BeautifulSoup(r.text,'html.parser')

            for t in soup.find_all('table'):

                txtCount = 0

                for txt in text:

                    if txt in str(t).lower():

                        txtCount += 1

                if txtCount == len(text):

                    table = str(t).replace("\n"," ")

                    table += "<br><br>"

                    break
                    
                else:
                    
                    table = "<br><br>"
                
        except:
                
            table = "<br><br>"
            
        table_list.append(table)
        
        return table_list
        
    '''
    
#print(ten_k_dig(form_links, "Net income"))
#print(ten_k_dig(form_links, "Dividends"))
#print(ten_k_dig(form_links, "Basic"))
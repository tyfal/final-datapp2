from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime
from django.contrib.auth.models import User
from pandas_datareader import data
import pandas as pd
import pylab, datetime
from time import strftime

# Create your models here.


class Portfolio(models.Model):
    
    
    name = models.CharField(max_length=20, primary_key=True)

    created = models.DateField('created', null=True, blank=True)

    start_date = models.DateField('start')

    end_date = models.DateField('end')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):

        return self.name
    
    
    def get_absolute_url(self):
        
        return reverse('folios2:stock-add', kwargs={'name': self.name})


class Stock(models.Model):
    
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, null=True)

    stock_symbol = models.CharField(max_length=10)

    added = models.DateField('added', default=timezone.now())

    quantity = models.IntegerField(default=1)
    
    income_statement_10k = models.CharField(max_length=10000, null=True, blank=True)
    
    income_statement_10q = models.CharField(max_length=10000, null=True, blank=True)


    def Financial(self):

        data_source = 'google'

        start_date = self.portfolio.start_date

        end_date = self.portfolio.end_date

        df = data.DataReader(self.stock_symbol, data_source, start_date, end_date)

        Values = df.values

        High = df['High'].values

        Low = df['Low'].values

        Open = df['Open'].values

        Close = df['Close'].values
        
        df.str_date = []
            
        [df.str_date.append(x.strftime('%m-%d-%Y')) for x in df.index.date]
        
        return df
    
    financial = Financial
    

    def __str__(self):

        return self.stock_symbol
    
    
    def get_absolute_url(self):
        
        return reverse('folios2:stock-add', kwargs={'name':self.portfolio.name})






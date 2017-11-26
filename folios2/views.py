from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Stock
import requests, re, math, string, datetime
import pandas as pd
from bs4 import BeautifulSoup
from SEC10v1 import *
from string import punctuation
from django.views import generic
from django.views.generic import View
from .forms import UserForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from income_statement import income_statement
from django.core.urlresolvers import reverse_lazy


# Create your views here.


def index(request):

    portfolio_list = Portfolio.objects.all()

    stock_by_port = []

    qty_by_port = []
    
    worth = []
    
    port_date = []
    
    close_by_port = []

    for port in Portfolio.objects.all():
        
        stock_count = 0
        
        port_worth = []

        x = []

        y = []
        
        close_by_stock = []

        for s in Stock.objects.all():
            
            stock_value = []
            
            try:

                count = 0

                if s.portfolio.name == port.name:
                    
                    if stock_count == 0: 
                
                        stock_count += 1

                        date_list = []

                        [date_list.append(x) for x in s.financial().str_date]

                        port_date.append(date_list)

                    close_list = s.financial().Close

                    for c in close_list:
                        
                        stock_value.append(c*s.quantity)

                        if len(port_worth) < len(close_list):

                            port_worth.append(c*s.quantity)

                        else:

                            port_worth[count] += (c*s.quantity)

                        count += 1
                    
                    x.append(s.stock_symbol)

                    y.append(s.quantity)
                    
                    close_by_stock.append(stock_value)
                
            except:
                
                pass
                
        worth.append(port_worth)

        stock_by_port.append(x)

        qty_by_port.append(y)
        
        close_by_port.append(close_by_stock)

    context = {'portfolio_list': portfolio_list, 'stock_by_port':stock_by_port, 'qty_by_port':qty_by_port, 'worth': worth, 'port_date':port_date, 'close_by_port':close_by_port}

    return render(request, 'folios2/index.html', context)


@login_required(login_url='../login')
def detail(request, name):

    try:

        portfolio_name = Portfolio.objects.get(pk=name)
        
        stock_list = Stock.objects.filter(portfolio=portfolio_name)

        symbol_list = []
        
        date_list = []
        
        close_list = []
        
        date_list = []
        
        dividends = []
        
        tenk_list = []
        
        tenq_list = []
        
        for s in stock_list:
        
            symbol_list.append(s.stock_symbol)
            
            tenk_list.append(s.income_statement_10k)
                
            tenq_list.append(s.income_statement_10q)
            
            yl = []
            
            xl = []
            
            for x, y in zip(s.financial().str_date, s.financial().Close):
                
                xl.append(x)
                
                yl.append(y)
                
            date_list.append(xl)
            
            close_list.append(yl)

    except Portfolio.DoesNotExist:

        raise Http404("Portfolio does not exist")

    return render(request, 'folios2/detail.html', {'portfolio': portfolio_name, 'stock_list': stock_list, 'close_list': close_list, 'date_list':date_list,'tenk_list': tenk_list, 'tenq_list': tenq_list})


class UserFormView(View):
    
    form_class = UserForm
    
    template_name = 'folios2/registration_form.html'
    
    # display blank form
    def get(self, request):
        
        form = self.form_class(None)
        
        return render(request, self.template_name, {'form':form})
        
    # proces form data
    def post(self, request):
        
        form = self.form_class(request.POST)
        
        if form.is_valid():
            
            user = form.save(commit=False)
            
            # cleaned (normalized) data
            username = form.cleaned_data['username']
            
            password = form.cleaned_data['password']
            
            user.set_password(password)
            
            user.save()
            
            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)
            
            if user is not None:
                
                if user.is_active:
                    
                    login(request, user)
                    
                    return redirect('folios2:profile')
            
        return render(request, self.template_name, {'form':form})
                 

class PortfolioCreate(CreateView):
    
    model = Portfolio
    
    fields = ['name', 'start_date', 'end_date', 'created', 'user']
    

class PortfolioUpdate(UpdateView):
    
    model = Portfolio
    
    fields = ['name', 'start_date', 'end_date', 'created', 'user']
    
    
class PortfolioDelete(DeleteView):
    
    model = Portfolio
    
    success_url = reverse_lazy('folios2:profile')
    

class StockCreate(CreateView):
    
    model = Stock
    
    fields = ['portfolio', 'stock_symbol', 'quantity']
    
    
class StockUpdate(UpdateView):
    
    model = Stock
    
    fields = ['portfolio', 'stock_symbol', 'quantity']
    

    
class StockDelete(DeleteView):
    
    model = Stock
    
    success_url = reverse_lazy('folios2:profile')
    
    
def IncomeStatement(request, pk):
    
    s = Stock.objects.filter(pk=pk)[0]
        
    income_statement(s)
    
    return redirect('folios2:detail', s.portfolio)
        
        
@login_required(login_url='../login')
def profile(request):
    
    portfolio_list = Portfolio.objects.filter(user=request.user)

    stock_by_port = []

    qty_by_port = []
    
    worth = []
    
    port_date = []
    
    close_by_port = []

    for port in portfolio_list:
        
        stock_count = 0
        
        port_worth = []

        x = []

        y = []
        
        close_by_stock = []

        for s in Stock.objects.all():
            
            stock_value = []
            
            try:

                count = 0

                if s.portfolio.name == port.name:
                    
                    if stock_count == 0: 
                
                        stock_count += 1

                        date_list = []

                        [date_list.append(x) for x in s.financial().str_date]

                        port_date.append(date_list)

                    close_list = s.financial().Close

                    for c in close_list:
                        
                        stock_value.append(c*s.quantity)

                        if len(port_worth) < len(close_list):

                            port_worth.append(c*s.quantity)

                        else:

                            port_worth[count] += (c*s.quantity)

                        count += 1
                    
                    x.append(s.stock_symbol)

                    y.append(s.quantity)
                    
                    close_by_stock.append(stock_value)
            except:
                
                pass
                
        worth.append(port_worth)

        stock_by_port.append(x)

        qty_by_port.append(y)
        
        close_by_port.append(close_by_stock)

    context = {'user':request.user, 'portfolio_list': portfolio_list, 'stock_by_port':stock_by_port, 'qty_by_port':qty_by_port, 'worth': worth, 'port_date':port_date, 'close_by_port':close_by_port}

    return render(request, 'folios2/profile.html', context)
    
                      
                      
    
    
    
    
    
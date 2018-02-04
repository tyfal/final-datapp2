from folios2.models import Stock, Portfolio
from SEC10v1 import recentIS, get_form, form_count_calc

def income_statement(stock):
    
    if stock.income_statement_10k == None or stock.income_statement_10k == "After battling the interweb... it won d[-_-]b":
    
        stock.income_statement_10k = recentIS(stock, "10-K")
        
        stock.save()
        
    if stock.income_statement_10q == None or stock.income_statement_10k == "After battling the interweb... it won d[-_-]b":
    
        stock.income_statement_10q = recentIS(stock, "10-Q")

        stock.save()
        

def form_links(stock):
    
    priming = form_count_calc("10-Q", start_date=str(stock.portfolio.start_date), end_date=str(stock.portfolio.end_date))

    form_links = get_form(stock.stock_symbol, "10-Q", priorto=priming['priorto'])[:priming['form_count']]
    
    stock.form_links = form_links
        
    stock.save()
    
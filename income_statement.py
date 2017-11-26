from folios2.models import Stock
from SEC10v1 import recentIS

def income_statement(stock):
    
    if stock.income_statement_10k == None or stock.income_statement_10k == "After battling the interweb... it won d[-_-]b":
    
        stock.income_statement_10k = recentIS(stock, "10-K")
        
        stock.save()
        
    if stock.income_statement_10q == None or stock.income_statement_10k == "After battling the interweb... it won d[-_-]b":
    
        stock.income_statement_10q = recentIS(stock, "10-Q")

        stock.save()
    
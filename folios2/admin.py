from django.contrib import admin
from .models import Portfolio, Stock

# Register your models here.

class StockInline(admin.TabularInline):
    
    model = Stock
    
    extra = 0

class PortfolioAdmin(admin.ModelAdmin):
    
    list_display = ['name', 'created']
    
    inlines = [StockInline]
    

admin.site.register(Portfolio, PortfolioAdmin)
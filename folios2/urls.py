from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name="folios2"

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^(?P<user>[^0-9]+)/portfolio/add/$', views.PortfolioCreate.as_view(), name='portfolio-add'),
    url(r'^(?P<name>[^0-9]+)/stock/add/$', views.StockCreate.as_view(), name='stock-add'),
    url(r'^portfolio/(?P<pk>[^0-9]+)/update/$', views.PortfolioUpdate.as_view(), name='portfolio-update'),
    url(r'^portfolio/(?P<pk>[^0-9]+)/delete/$', views.PortfolioDelete.as_view(), name='portfolio-delete'),
    url(r'^stock/(?P<pk>\d+)/update/$', views.StockUpdate.as_view(), name='stock-update'),
    url(r'^stock/(?P<pk>\d+)/income-statement/$', views.IncomeStatement, name='income-statement'),
    url(r'^stock/(?P<pk>\d+)/links/$', views.Links, name='links'),
    url(r'^stock/(?P<pk>\d+)/delete/$', views.StockDelete.as_view(), name='stock-delete'),
    url(r'^login/$', auth_views.login, {'template_name': 'folios2/login_form.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '../'}, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^(?P<name>[^0-9]+)/$', views.detail, name='detail')
]

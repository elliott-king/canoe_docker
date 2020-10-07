from django.urls import path
from . import views

app_name = 'demo'
urlpatterns = [
    path('', views.index, name='index'),
    path('cash_flow', views.cash_flow, name='cash_flow'),
    path('<int:client_id>/', views.detail, name='detail'),
]
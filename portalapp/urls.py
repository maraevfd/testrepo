from django.urls import path
from portalapp import views

urlpatterns = [
    path('', views.start_page, name='home'),
    path('expenses/', views.show_all, name='expenses'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_category/', views.add_category, name='add_category'),
    path('<slug:slug>/', views.by_category, name='by_category'),
]

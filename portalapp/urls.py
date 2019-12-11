from django.urls import path
from portalapp import views

urlpatterns = [
    path('', views.start_page, name='home'),
    path('expenses/', views.show_all, name='expenses'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('get_salary/', views.get_a_salary, name='get_salary'),
    path('add_category/', views.add_category, name='add_category'),
    path('<slug:slug>/', views.by_category, name='by_category'),
    path('<int:category_id>/send/', views.send_email, name='send_email')
]

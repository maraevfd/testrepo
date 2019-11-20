from django.urls import path, include
from portalapp.views import BaseView, ExpenseListView, show_last

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('expenses/', ExpenseListView.as_view(), name='expenses'),
    path('latest/', show_last, name='latest'),
]

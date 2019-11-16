from django.urls import path, include
from portalapp.views import BaseView

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
]

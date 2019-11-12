from django.urls import path, include
from portalapp.views import example_view

urlpatterns = [
    path('', example_view, name='example'),
]

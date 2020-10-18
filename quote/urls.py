from django.urls import include, path
from . import views

urlpatterns =[
    path('', views.view_quote, name='view_quote'),
]
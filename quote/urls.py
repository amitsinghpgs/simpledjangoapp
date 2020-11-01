from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.view_quote, name='view_quote'),
    path('delete/<pk>', views.QuoteDelete.as_view(), name='view_delete_quote')
]
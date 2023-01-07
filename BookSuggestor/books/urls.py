from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.searchList, name='search'),
    path('book/<int:pk>', views.book, name='book')
]
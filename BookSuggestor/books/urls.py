from django.urls import path
from . import views

urlpatterns = [
    path('add', views.addData, name="add"),
    path('',views.bookSuggestor, name='suggestor'),
    path('search', views.bookSearch, name='search'),
    path('detail',views.bookDetails,name='detail')
]
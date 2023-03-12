from django.urls import path
from . import views

urlpatterns = [
    path('add', views.addData, name="add"),
    path('',views.bookSuggestor, name='suggestor'),
    path('search', views.bookSearch, name='search'),
    path('detail/<int:id>',views.bookDetails,name='detail'),
    path('update/<int:id>',views.updateBook,name='update'),
    path('confirmDelete/<int:id>',views.confirmDelete,name='confirm'),
    path('delete/<int:id>',views.deleteBook,name='delete'),
]
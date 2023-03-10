from django.forms import ModelForm
from books.models import Author, Book, Genre


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        labels={
            'aname':'Author Name'
        }


class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
        
        labels={
            'type':'Book Genre'
        }


class BookForm(ModelForm):
    class Meta:
        model = Book
        # fields = "__all__"
        exclude = ['genre','author',"photo"]
        labels={
            'name':'Book Name',
        }



class SearchForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name','genre','author']
        

        

from django.shortcuts import render, HttpResponse
from .models import Book, Genre, Author

# Create your views here.
def home(request):

    return render(request, 'books/homepage.html')


def searchList(request):
    author = request.GET.get('author')
    genre = request.GET.get('genre')
    liked = request.GET.get('liked')
    print(author,genre,liked)
    book = Book.objects.all()
    

    books = {}


    
    return render(request, 'books/searchpage.html')


def book(request, pk):
    id=pk
    return HttpResponse(f"Book Detail page Number {id}")


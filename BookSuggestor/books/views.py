from django.db import models
from django.shortcuts import render, redirect
from books.models import Book, Genre, Author
from books.forms import AuthorForm, BookForm, GenreForm


def addData(request):
    authForm = AuthorForm()
    bkForm = BookForm()
    genForm = GenreForm()

    if request.method == "POST":
        af = AuthorForm(request.POST)
        if af.is_valid():
            auth_name = af.cleaned_data['aname']

        gf = GenreForm(request.POST)
        if gf.is_valid():
            gen_type = gf.cleaned_data['type']

        bf = BookForm(request.POST)
        if bf.is_valid():
            book_name = bf.cleaned_data["name"]
            # author = bf.cleaned_data["author"]
            book_photo = bf.cleaned_data["photo"]
            # genre = bf.cleaned_data["genre"]

        a = Author.objects.create(aname=auth_name)
        a.save()
        g = Genre.objects.create(type=gen_type)
        g.save()
        b = Book.objects.create(name=book_name,photo=book_photo,genre=g,author=a)

    books = Book.objects.all()
    context = {'books':books, 'authForm':authForm, 'bkForm':bkForm, 'genForm':genForm}

    return render(request, 'books/addData.html', context)



def bookSuggestor(request):
    pass

def bookSearch(request):
    pass

def bookDetails(request):
    pass
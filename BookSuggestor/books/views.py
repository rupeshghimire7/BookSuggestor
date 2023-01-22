from django.db import models
from django.shortcuts import render, redirect
from books.models import Book, Genre, Author
from books.forms import AuthorForm, BookForm, GenreForm


def addData(request):

    books = Book.objects.all()
    book_names=[]
    for book in books:
        book_names.append(book.name.upper())
    count = len(book_names)


    if request.method == "POST":
        af = AuthorForm(request.POST)
        if af.is_valid():
            auth_name = af.cleaned_data['aname']
            auth_name.capitalize()


        gf = GenreForm(request.POST)
        if gf.is_valid():
            gen_type = gf.cleaned_data['type']
            gen_type.capitalize()


        bf = BookForm(request.POST, request.FILES)
        if bf.is_valid():
            b = bf.save(commit=False)
            print(b.name.upper())
            if b.name.upper() in book_names:
                pass
            else: 
                a = Author.objects.create(aname=auth_name)
                a.save()
                g = Genre.objects.create(type=gen_type)
                g.save()
                b.genre = g
                b.author = a
                b.save()
    else:
        af = AuthorForm()
        bf = BookForm()
        gf = GenreForm()



    context = {'books':books, 'authForm':af, 'bkForm':bf, 'genForm':gf}

    return render(request, 'books/addData.html', context)



def bookSuggestor(request):
    pass

def bookSearch(request):
    pass

def bookDetails(request):
    pass
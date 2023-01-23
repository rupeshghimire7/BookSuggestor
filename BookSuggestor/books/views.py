from django.db import models
from django.shortcuts import render, redirect
from books.models import Book, Genre, Author
from books.forms import AuthorForm, BookForm, GenreForm, SearchForm

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
            if b.name.upper() in book_names:
                pass
            else: 
                a = Author.objects.create(aname=auth_name.upper())
                a.save()
                g = Genre.objects.create(type=gen_type.upper())
                g.save()
                b.name = b.name.upper()
                b.genre = g
                b.author = a
                b.save()
    else:
        af = AuthorForm()
        bf = BookForm()
        gf = GenreForm()



    context = {'books':books, 'authForm':af, 'bkForm':bf, 'genForm':gf,'count':count}

    return render(request, 'books/addData.html', context)



def bookSuggestor(request):
    form = SearchForm()
    
    books = Book.objects.all()
    book_list = []
    for book in books:
        if (book.name.upper() in book_list):
            pass
        else:
            book_list.append(book.name.upper())
    context = {'form':form,'books':book_list}
    return render(request, 'books/suggestBook.html',context )



def bookSearch(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        liked = form.cleaned_data['name']
        genre = form.cleaned_data["genre"]
        author = form.cleaned_data["author"]
    bk_likes = Book.objects.get(name=liked)
    bk_genres = Book.objects.get(genre=genre)
    bk_authors = Book.objects.get(author=author)

def bookDetails(request):
    pass
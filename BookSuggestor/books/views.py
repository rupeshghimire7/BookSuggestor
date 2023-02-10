from django.db import models
from django.shortcuts import render, redirect, HttpResponse
from books.models import Book, Genre, Author
from books.forms import AuthorForm, BookForm, GenreForm, SearchForm
from django.db import connection


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def getbooks():
    cursor= connection.cursor()
    # books = Book.objects.all()
    cursor.execute("SELECT * FROM books_book")
    books = dictfetchall(cursor)
    print(books)
    # cursor.execute("SELECT id from books_author ")
    book_list = []
    for book in books:
        print(book)
        cursor.execute("SELECT aname from books_author WHERE id=%s",[book['author_id']])
        anames = dictfetchall(cursor)
        print(anames)
        if (book["name"].upper() in book_list):
            pass
        else:
            book_list.append(book["name"].upper())
    print(book_list)

    return book_list


def addData(request):
    cursor = connection.cursor()
    book_names = getbooks()
    count = len(book_names)


    if request.method == "POST":
        af = AuthorForm(request.POST)
        if af.is_valid():
            auth_name = af.cleaned_data['aname']


        gf = GenreForm(request.POST)
        if gf.is_valid():
            gen_type = gf.cleaned_data['type']


        bf = BookForm(request.POST, request.FILES)
        if bf.is_valid():
            b = bf.save(commit=False)
            if b.name.upper() in book_names:
                pass
            else: 
                # a = Author.objects.create(aname=auth_name.upper())
                # a.save()
                cursor.execute("INSERT into books_author (aname) VALUES (%s)", [auth_name.upper()])
                cursor.execute("SELECT id FROM books_author WHERE aname=%s",[auth_name.upper()])
                a = cursor.fetchone()
                print("author id : ",a)
    #             # g = Genre.objects.create(type=gen_type.upper())
    #             # g.save()
                cursor.execute("INSERT into books_genre (type) VALUES (%s)", [gen_type.upper()])
                cursor.execute("SELECT id FROM books_genre WHERE type=%s",[gen_type.upper()])
                g = cursor.fetchone()


                cursor.execute("INSERT into books_book (name,author_id,genre_id) VALUES(%(name)s, %(a)s, %(g)s)",{'name':b.name.upper(), 'a':a, 'g':g})
    else:
        af = AuthorForm()
        bf = BookForm()
        gf = GenreForm()



    context = {'books':book_names, 'authForm':af, 'bkForm':bf, 'genForm':gf,'count':count}

    return render(request, 'books/addData.html',context)



def bookSuggestor(request):
    form = SearchForm()
    book_list = getbooks()
    context = {'form':form,'books':book_list}
    return render(request, 'books/suggestBook.html', context )



def bookSearch(request):
    sf = SearchForm(request.POST)
    if sf.is_valid:
        liked = sf.cleaned_data["name"]
        author = sf.cleaned_data['author']
        genre = sf.cleaned_data['genre']
        
        print(liked,author,genre)
    return HttpResponse("HELLO") 



# def bookSearch(request):
#     with connection.cursor() as cursor:
#         books = []
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             liked = form.cleaned_data['name']
#             genre = form.cleaned_data["genre"]
#             author = form.cleaned_data["author"]

        

#             #Book.objects.get(name=liked)
#             cursor.execute("SELECT * FROM books_book where name=%s",[liked])
#             bk_likes_dict = dictfetchall(cursor)

#             for book in bk_likes_dict:
#                 books.append(book.name)

#             # Book.objects.get(genre=genre)
#             cursor.execute("SELECT id FROM books_genre WHERE genre=%s",[genre])
#             g_id = cursor.fetchone()
#             cursor.execute("SELECT name FROM books_book WHERE genre_id=%s",[g_id])
#             book_g = cursor.fetchone()

#             # bk_genres = dictfetchall(cursor)

#             # Book.objects.get(author=author)
#             cursor.execute("SELECT id FROM books_author where aname=%s",[author])
#             a_id = cursor.fetchone()
#             cursor.execute("SELECT name FROM books_book WHERE genre_id=%s",[g_id])
#             book_g = cursor.fetchone()
#             print(a_id)
#             # cursor.execute("SELECT * FROM books_book where author=%s",[author])
#             # bk_authors = dictfetchall(cursor)
            
#             print(bk_likes_dict)

#         context = {}
#     return render(request, 'books/matchBook.html',)



def bookDetails(request):
    pass



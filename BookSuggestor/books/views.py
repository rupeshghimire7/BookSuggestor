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


def getgenre():
    cursor = connection.cursor()
    cursor.execute("Select type from books_genre")
    allTypes = dictfetchall(cursor)
    genres = [genre['type'].upper() for genre in allTypes]
    print("All Genres:",genres)
    return genres


def getauthors():
    cursor = connection.cursor()
    cursor.execute("Select aname from books_author")
    allAuthors = dictfetchall(cursor)
    authors = [author['aname'].upper() for author in allAuthors]
    print("All Authors:",authors)

    return authors




def getbooks():
    cursor = connection.cursor()
    # books = Book.objects.all()
    cursor.execute("SELECT * FROM books_book")
    books = dictfetchall(cursor)
    # print(books)
    # cursor.execute("SELECT id from books_author ")
    book_list = []
    for book in books:
        # print(book)
        cursor.execute("SELECT aname from books_author WHERE id=%s",[book['author_id']])
        anames = dictfetchall(cursor)
        # print(anames)
        if (book["name"].upper() in book_list):
            pass
        else:
            book_list.append(book["name"].upper())
    # print(book_list)

    return book_list


def addData(request):
    cursor = connection.cursor()
    book_names = getbooks()
    allAuthors = getauthors()
    allTypes = getgenre()
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

                if auth_name.upper() not in allAuthors:
                    cursor.execute("INSERT into books_author (aname) VALUES (%s)", [auth_name.upper()])
                cursor.execute("SELECT id FROM books_author WHERE aname=%s",[auth_name.upper()])
                a = cursor.fetchone()
                print("author id : ",a)


    #             # g = Genre.objects.create(type=gen_type.upper())
    #             # g.save()

                if gen_type.upper() not in allTypes:
                    cursor.execute("INSERT into books_genre (type) VALUES (%s)", [gen_type.upper()])
                cursor.execute("SELECT id FROM books_genre WHERE type=%s",[gen_type.upper()])
                g = cursor.fetchone()

                print("allBooks: ",book_names)
                if b.name.upper() not in book_names:
                    cursor.execute("INSERT into books_book (name,author_id,genre_id) VALUES(%(name)s, %(a)s, %(g)s)",{'name':b.name.upper(), 'a':a, 'g':g})
                else:
                    print("This Book is already in database.")    
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
    cursor = connection.cursor()
    sf = SearchForm(request.POST)
    if sf.is_valid():
        liked = sf.cleaned_data["name"].upper()
        author = sf.cleaned_data['author']
        # print("Author is: ",author)
        genre = sf.cleaned_data['genre']
        # print("Genre is:",genre)

        matching = {}
        cursor.execute("SELECT author_id,genre_id FROM books_book WHERE name=%s",[liked])
        # books = dictfetchall(cursor)
        if cursor.fetchone():
            auth_id,gen_id = cursor.fetchone()
        else:
            cursor.execute("Select author_id, genre_id from books_book")
            auth_id,gen_id = cursor.fetchone()    

        cursor.execute("Select * from books_book where author_id=%s or genre_id=%s",[auth_id,gen_id])
        books = dictfetchall(cursor)
        print(books)
        for book in books:
            if book['name'] not in matching:
                matching[book["name"]] = book
        # print("Matching:",matching)

        cursor.execute("Select * from books_book where author_id=(select id from books_author where aname=%s)",[author])
        Author_books = dictfetchall(cursor)
        # print("Author Books:",Author_books)
        for book in Author_books:
            if book['name'] not in matching:
                matching[book["name"]] = book


        cursor.execute("Select * from books_book where genre_id = (select id from  books_genre where type=%s)",[genre])
        Genre_books = dictfetchall(cursor)
        for book in Genre_books:
            if book['name'] not in matching:
                matching[book["name"]] = book
        print("ALL MATCHING BOOKS ARE:\n",matching)

        count = len(matching)



    # return HttpResponse("hello")
    return render(request, 'books/matchBook.html', {'matching':matching})


def bookDetails(request, id):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books_book where id = %s",[id])
    book = dictfetchall(cursor)
    context = {}
    for detail in book:
        context['name'] = detail["name"] 
        cursor.execute("Select aname from books_author where id=%s",[detail['author_id']])
        context["author"] = cursor.fetchone()[0]
        cursor.execute("Select type from books_genre where id=%s",[detail['genre_id']])
        context["genre"] = cursor.fetchone()[0]
        print(context)
    return render(request,'books/bookDetail.html', context )

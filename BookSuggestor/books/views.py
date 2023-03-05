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

def allBooks():
    cursor = connection.cursor()
    book_list = getbooks()
    allBooks_dict = {}
    for book in book_list:
        cursor.execute("SELECT * FROM books_book WHERE name=%s",[book])
        book_data = dictfetchall(cursor)
        for item in book_data:
            name=item['name']
            allBooks_dict[name] = item
        # print("SINGLE BOOK LIST:",book_data)
    print("ALL BOOKS: ",allBooks_dict)
    return(allBooks_dict)



def addData(request):
    cursor = connection.cursor()
    book_names = allBooks()
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
    allBooks()
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
        id_list = cursor.fetchone()
        if id_list:
            id_list = list(id_list)
        else:
            cursor.execute("Select author_id, genre_id from books_book")
            id_list = list(cursor.fetchone())

        auth_id = id_list[0]
        gen_id = id_list[1]
   

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



def updateBook(request,id):
    
    #GETTING THE DATA FROM THE DATABASE

    print("The id is:",id)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books_book where id = %s",[id])
    book = cursor.fetchone()
    print("The book is: ",book)
    title = book[1]
    cursor.execute("Select aname from books_author where id=%s",[book[3]])
    author = cursor.fetchone()[0]
    cursor.execute("Select type from books_genre where id=%s",[book[4]])
    genre = cursor.fetchone()[0]


    #SENDING OUT THE FORM WITH THE DATA FOR UPDATING

    print("The title is: ",title)
    print("The author is: ",author)
    print("The genre is: ",genre)
    book1 = Book.objects.get(id=id)
    print(type(book1))
    print("The book is: ",book1)
    form = SearchForm(request.POST, instance=book1)
    print(type(id))
    book = {'title':title, 'author':author, 'genre':genre }


    #UPDATING THE DATA

    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name'].upper()
            author_new = form.cleaned_data['author']
            genre_new = form.cleaned_data['genre']
            print("The name is: ",name)
            print("The author is: ",author_new)
            print("The genre is: ",genre_new)
        if name != title:
            cursor.execute("UPDATE books_book SET name=%s WHERE id=%s",[name,id])
        if author_new != author:
            cursor.execute("UPDATE books_book SET author_id=(SELECT id FROM books_author WHERE aname=%s) WHERE id=%s",[author_new,id])
        if genre_new != genre:
            cursor.execute("UPDATE books_book SET genre_id=(SELECT id FROM books_genre WHERE type=%s) WHERE id=%s",[genre_new,id])
            return redirect('add')
    return render(request, 'books/updateBook.html', {'book':book, 'form':form, 'id':id})
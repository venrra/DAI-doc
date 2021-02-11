# mi_aplicacion/views.py
from .models import Libro, Prestamo
from django.shortcuts import render, HttpResponse, redirect
from .forms import BookForm, LoanForm, SearchBook, SearchLoan
from django.views.decorators.csrf import csrf_protect

# Create your views here.

def index(request):
    context = {}
    return render(request, 'index.html', context)
    #return HttpResponse('Hello World!')


### Libros

def books(request):
    form_search = SearchBook()
    context = {
        'form' : form_search
    }
    if request.method == 'POST':
        form_search_post = SearchBook(request.POST)
        if form_search_post.is_valid():
            key=form_search_post.data['busqueda']
            value=form_search_post.data['search']
            context['books'] = Libro.get_libro(key,value)
            return render(request, 'books.html', context)

    context['books'] = Libro.objects.all()
    return render(request, 'books.html', context)

### Prestamos

def loans(request):
    form_search = SearchLoan()
    context = {
        'form' : form_search
    }
    if request.method == 'POST':
        form_search_post = SearchLoan(request.POST)
        if form_search_post.is_valid():
            key=form_search_post.data['busqueda']
            value=form_search_post.data['search']
            context['loans'] = Prestamo.get_prestamo(key,value)
            return render(request, 'loans.html', context)

    context['loans'] = Prestamo.objects.all()
    return render(request, 'loans.html', context)

def add_book(request):
    form = BookForm()
    context ={
        'form' : form
    }
    return render(request, 'add_book.html', context)

def edit_book(request):
    form = BookForm()
    contex={
        'form':form
    }
    if request.method == 'POST':
        if 'edit' in request.POST:
            id = request.POST['edit']
            contex['book'] = Libro.objects.get(id=id)
            return render(request, 'edit_book.html', contex)

    return redirect(books)


def add_loan(request):
    form = LoanForm()
    context ={
        'form' : form
    }
    return render(request, 'add_loan.html', context)

def edit_loan(request):
    return redirect(books)

def test_template(request):
    context = {}   # Aquí van la las variables para la plantilla
    return render(request,'test.html', context)
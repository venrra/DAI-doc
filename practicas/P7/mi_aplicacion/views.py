# mi_aplicacion/views.py
from .models import Libro, Prestamo
from django.shortcuts import render, HttpResponse, redirect
from .forms import BookForm, LoanForm, SearchBook, SearchLoan
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.

def index(request):
    context = {}
    return render(request, 'index.html', context)
    #return HttpResponse('Hello World!')

### Libros
@login_required
def books(request):
    form_search = SearchBook()
    context = {
        'form' : form_search
    }
    if request.method == 'POST':
        form_search_post = SearchBook(request.POST)
        if form_search_post.is_valid():
            key=form_search_post.cleaned_data['busqueda']
            value=form_search_post.cleaned_data['search']
            context['books'] = Libro.get_libro(key,value)
            return render(request, 'books.html', context)
    context['books'] = Libro.objects.all()
    return render(request, 'books.html', context)
@login_required
def book(request, id):
    form_search = SearchBook()
    context = {
        'form' : form_search
    }
    context['books'] = Libro.get_libro('id',id)
    return render(request, 'books.html', context)

### Prestamos
@permission_required('mi_aplicacion.view_prestamo')
@login_required
def loans(request):
    form_search = SearchLoan()
    context = {
        'form' : form_search
    }
    if request.method == 'POST':
        form_search_post = SearchLoan(request.POST)
        if form_search_post.is_valid():
            key=form_search_post.cleaned_data['busqueda']
            value=form_search_post.cleaned_data['search']
            context['loans'] = Prestamo.get_prestamo(key,value)
            return render(request, 'loans.html', context)

    context['loans'] = Prestamo.objects.all()
    return render(request, 'loans.html', context)

@permission_required('mi_aplicacion.view_prestamo')
@login_required
def loan(request, id):
    form_search = SearchLoan()
    context = {
        'form' : form_search
    }
    context['loans'] = Prestamo.get_prestamo('id',id)
    return render(request, 'loans.html', context)

@permission_required('mi_aplicacion.add_libro')
@login_required
def add_book(request):
    form = BookForm()
    context ={
        'form' : form
    }
    if request.method == 'POST':
        form_add = BookForm(request.POST)
        if form_add.is_valid():
            libro=form_add.save()
            return redirect('book', id=libro.id)

    return render(request, 'add_book.html', context)

@permission_required('mi_aplicacion.change_libro')
@permission_required('mi_aplicacion.delete_libro')
@login_required
def edit_book(request):
    form = BookForm()
    contex={
        'form':form
    }
    if request.method == 'POST':
        if 'edit' in request.POST:
            id = request.POST['edit']
            libro = Libro.objects.get(id=id)
            form.fields['titulo'].initial = libro.titulo
            form.fields['autor'].initial = libro.autor
            contex['book'] = libro
            contex['id'] = id
            return render(request, 'edit_book.html', contex)
        elif 'save' in request.POST:
            form_save = BookForm(request.POST)
            if form_save.is_valid():
                libro = Libro.objects.get(id=request.POST['save'])
                libro.titulo = form_save.cleaned_data['titulo']
                libro.autor = form_save.cleaned_data['autor']
                libro.save()
                return redirect(book, id=libro.id)
        elif 'delete' in request.POST:
            id = request.POST['delete']
            Libro.objects.get(id=id).delete()
    return redirect(books)

@permission_required('mi_aplicacion.add_prestamo')
@login_required
def add_loan(request):
    form = LoanForm()
    context ={
        'form' : form
    }
    if request.method == 'POST':
        form_add = LoanForm(request.POST)
        if form_add.is_valid():
            loan=form_add.save()
            return redirect('loan', id=loan.id)

    return render(request, 'add_loan.html', context)

@permission_required('mi_aplicacion.change_prestamo')
@permission_required('mi_aplicacion.delete_prestamo')
@login_required
def edit_loan(request):
    form = LoanForm()
    contex={
        'form':form
    }
    if request.method == 'POST':
        if 'edit' in request.POST:
            id = request.POST['edit']
            loan = Prestamo.objects.get(id=id)
            form.fields['libro'].initial = loan.libro
            form.fields['fecha'].initial = loan.fecha
            form.fields['usuario'].initial = loan.usuario
            contex['loan'] = loan
            contex['id'] = id
            return render(request, 'edit_loan.html', contex)
        elif 'save' in request.POST:
            form_save = LoanForm(request.POST)
            if form_save.is_valid():
                loan = Prestamo.objects.get(id=request.POST['save'])
                loan.libro = form_save.cleaned_data['libro']
                loan.fecha = form_save.cleaned_data['fecha']
                loan.usuario = form_save.cleaned_data['usuario']
                loan.save()
                return redirect('loan', id=loan.id)
        elif 'delete' in request.POST:
            id = request.POST['delete']
            Prestamo.objects.get(id=id).delete()
    return redirect(loans)

def test_template(request):
    context = {}   # Aquí van la las variables para la plantilla
    return render(request,'test.html', context)
# mi_aplicacion/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books', views.books, name='books'),
    path('add_book', views.add_book, name='add_book'),
    path('book/edit', views.edit_book, name='edit_book'),
    path('loans', views.loans, name='loans'),
    path('add_loan', views.add_loan, name='add_loan'),
    path('loan/edit', views.edit_loan, name='edit_loan'),
]
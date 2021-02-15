# mi_aplicacion/urls.py

from django.conf.urls import include, url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books', views.books, name='books'),
    path('books/<int:id>', views.book, name='book'),
    path('add_book', views.add_book, name='add_book'),
    path('book/edit', views.edit_book, name='edit_book'),
    path('loans', views.loans, name='loans'),
    path('loans/<int:id>', views.loan, name='loan'),
    path('add_loan', views.add_loan, name='add_loan'),
    path('loan/edit', views.edit_loan, name='edit_loan'),
]
urlpatterns += [
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
]
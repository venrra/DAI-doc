from django import forms
from .models import Libro, Prestamo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

BUSQUEDA_BOOKS = (
    ('titulo', 'titulo'),
    ('autor', 'autor')
)

BUSQUEDA_LOANS = (
    ('libro', 'libro'),
    ('fecha', 'fecha'),
    ('usuario', 'usuario')
)

class BookForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ('titulo', 'autor',)

class LoanForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ('libro', 'fecha', 'usuario',)

class SearchBook(forms.Form):
    busqueda = forms.ChoiceField(choices=BUSQUEDA_BOOKS, label=False)
    search = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Buscar...'}),
        label=False
        )

class SearchLoan(forms.Form):
    busqueda = forms.ChoiceField(choices=BUSQUEDA_LOANS, label=False)
    search = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Buscar...'}),
        label=False
    )
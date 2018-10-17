from django import forms

class AddBookForm(forms.Form):
    query = forms.CharField(label='Search for a book', max_length=100)
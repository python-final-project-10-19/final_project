from django import forms

class AddBookForm(forms.Form):
    query = forms.CharField(label='Search for a book', max_length=100)


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
    )

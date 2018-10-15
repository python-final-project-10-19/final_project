from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.exceptions import PermissionDenied
from ..models import Book, Profile
import requests
import os
from ..forms import AddBookForm


def book_add_view(request):
    if request.method == "POST":
        form = AddBookForm()
        print(request.json())
    else:
        form = AddBookForm()

    return render(request, 'books/book_add.html', {'form': form})

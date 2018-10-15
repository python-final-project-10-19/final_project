from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.exceptions import PermissionDenied
from ..models import Book, Profile
import requests
import os
from ..forms import AddBookForm


def book_add_view(request):
    context = {'results': []}
    if request.method == "POST":
        form = AddBookForm()
        input_value = request.POST['query']
        print(input_value)
        response = requests.get('https://www.googleapis.com/books/v1/volumes?q={}&maxResults=4'.format(input_value)).json()
        results_list = response['items']

        for result in results_list:
            try:
                title = result['volumeInfo']['title']
            except:
                title = ''
            try:
                author = result['volumeInfo']['authors'][0]
            except:
                author = ''
            try:
                description = result['volumeInfo']['description']
            except:
                description = ''
            try:
                categories = result['volumeInfo']['categories']
            except:
                categories = ''
            try:
                image_url = result['volumeInfo']['imageLinks']['thumbnail']
            except:
                image_url = ''

            context['results'].append({
                'title': title,
                'author': author,
                'description': description,
                'categories': categories,
                'image_url': image_url,
                # 'purchase_link': result['saleInfo']['buyLink'],
                })
        print(context)
    else:
        form = AddBookForm()

    return render(request, 'books/book_add.html', {'form': form, 'results': context['results']})

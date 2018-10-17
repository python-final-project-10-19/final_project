from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.exceptions import PermissionDenied
from ..models import Book, Profile
import requests
import os
from ..forms import AddBookForm


def book_add_view(request):
    if not request.user.is_authenticated:
        return redirect('home')

    context = {'results': []}
    if request.method == "POST":

        form = AddBookForm()
        input_value = request.POST.get('query')
        print('here is out input_value', input_value)
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

    else:
        form = AddBookForm()

    return render(request, 'books/book_add.html', {'form': form, 'results': enumerate(context['results'])})


def book_post_view(request):

    if request.method == "POST":
        # import pdb; pdb.set_trace()
        # TODO: Add this book to book model for that user.
        # user = User()

        fb_account = Profile.objects.filter(user__id=request.user.id)
        fb_id = list(fb_account.values('fb_id'))[0]['fb_id']

        Book.objects.create(
            user=request.user,
            owner=fb_id,
            title=request.POST['title'],
            author=request.POST['author'],
        )


    return redirect('/books/add/')

from django.shortcuts import render, get_object_or_404, redirect, reverse, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from book_share_project.models import Book, Profile, Document
import requests
import os
from book_add_app.forms import AddBookForm, DocumentForm





def book_list_view(request):
    if not request.user.is_authenticated:
        return redirect('home')

    # Setting default to google books api search
    return redirect('book_search')


def book_add_search(request):
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

    return render(request, 'add/book_add_google.html', {'form': form, 'results': enumerate(context['results'])})


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

    return redirect('/add/search')


def book_add_scan(request):
    if not request.user.is_authenticated:
        return redirect('home')

    # Handle file upload
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return redirect('book_scan')
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(request, 'add/book_add_scan.html', {'documents': documents, 'form': form})

    # return render(request, 'add/book_add_scan.html')

    # def index(request):
    # return render_to_response('myapp/index.html')

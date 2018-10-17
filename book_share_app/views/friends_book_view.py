from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.exceptions import PermissionDenied
from ..models import Book, Profile
import requests
import os


def book_list_view(request):
    # Instead of permission denied, consider a redirect to the home page.
    if not request.user.is_authenticated:
        raise PermissionDenied

    profile = Profile.objects.filter(
        user__id=request.user.id
        )
    print(profile)
    fb_id = list(profile.values('fb_id'))[0]['fb_id']

    endpoint = 'https://graph.facebook.com/{}?fields=friends'.format(fb_id)
    headers = {'Authorization': 'Bearer {}'.format(os.environ.get('FB_GRAPH_TOKEN'))}
    response = requests.get(endpoint, headers=headers).json()

    friends_data = response['friends']['data']
    friends = []
    for friend in friends_data:
        friends.append(friend['id'])

    profile.update(friends=friends)

    # TODO: We need to find books corresponding to each friends fb_id
    # books = Book.objects.filter(user__id=request.user.id)
    books = []
    for friend in friends:
        print(friend)
        books = Book.objects.filter(owner=friend)
        if len(books):
            book_obj = {'title': '', 'author': ''}
            for book in books:
                # import pdb; pdb.set_trace()
                book_obj['title'] = list(book.values('title'))[0]['title']
                book_obj['author'] = list(book.values('author'))[0]['author']

    context = {
        'books': book_obj
    }

    return render(request, 'books/book_list.html', context)


# def book_detail_view(request, pk=None):
#     if not request.user.is_authenticated:
#         return redirect(reverse('login'))

#     book = get_object_or_404(Book, id=pk, user__username=request.user.username)

#     context = {
#         'book': book,
#     }

#     return render(request, 'books/book_detail.html', context)

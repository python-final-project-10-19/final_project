from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.exceptions import PermissionDenied
from book_share_project.models import Book, Profile, Notifications
import requests
import os


def book_list_view(request):
    if not request.user.is_authenticated:
        return redirect('home')

    # Setting default to friends collection view
    return redirect('friends_collection')


def personal_view(request):
    if not request.user.is_authenticated:
        return redirect('home')

    profile = Profile.objects.filter(
        user__id=request.user.id
        )

    fb_id = list(profile.values('fb_id'))[0]['fb_id']

    all_books = []
    books = Book.objects.filter(owner=fb_id)

    if len(books):
            for book in books.values():
                book_obj = {
                    'title': book['title'],
                    'author': book['author'],
                   }
                all_books.append(book_obj)

    context = {
        'books': all_books
    }

    return render(request, 'collections/book_list_personal.html', context)


def friends_view(request):
    if not request.user.is_authenticated:
        return redirect('home')

    profile = Profile.objects.filter(
        user__id=request.user.id
        )

    fb_id = list(profile.values('fb_id'))[0]['fb_id']

    # Logged in user pressing 'request book' button
    if request.method == "POST":
        # import pdb; pdb.set_trace()

        Notifications.objects.create(
            type='request',
            status='pending',
            from_user=fb_id,
            to_user=request.POST.get('owner'),
            book_id=request.POST.get('book_id'),
        )

        book = Book.objects.filter(id=request.POST.get('book_id'))
        book.update(status='requested')
        book.update(requester=fb_id)

        return redirect('/collections/friends')


    # Grab and update user's friends from FB API
    endpoint = 'https://graph.facebook.com/{}?fields=friends'.format(fb_id)
    headers = {'Authorization': 'Bearer {}'.format(os.environ.get('FB_GRAPH_TOKEN'))}
    response = requests.get(endpoint, headers=headers).json()
    try:
        friends_data = response['friends']['data']
    except KeyError:
        friends_data = []
    friends = []
    for friend in friends_data:
        friends.append(friend['id'])
    profile.update(friends=friends)

    # For each friend grab their books from book model
    all_books = []
    for friend in friends:
        books = Book.objects.filter(owner=friend)
        friend_profile = Profile.objects.filter(fb_id=friend)
        # import pdb; pdb.set_trace()
        if len(friend_profile):
            friend_name = list(friend_profile.values('first_name'))[0]['first_name'] + ' ' + list(friend_profile.values('last_name'))[0]['last_name']

        if len(books):
            for book in books.values():

                book_obj = {
                    'id': book['id'],
                    'title': book['title'],
                    'author': book['author'],
                    'owner': friend_name,
                    'status': book['status'],
                    'requester': book['requester']
                    }
                all_books.append(book_obj)

    context = {
        'books': enumerate(all_books),
        'fb_id': fb_id
    }

    return render(request, 'collections/book_list_friends.html', context)


# def book_detail_view(request, pk=None):
#     if not request.user.is_authenticated:
#         return redirect(reverse('login'))

#     book = get_object_or_404(Book, id=pk, user__username=request.user.username)

#     context = {
#         'book': book,
#     }

#     return render(request, 'books/book_detail.html', context)

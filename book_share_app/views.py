from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.exceptions import PermissionDenied
from .models import Book, Profile
from allauth.socialaccount.models import SocialAccount
import requests
import json


def book_list_view(request):
    if not request.user.is_authenticated:
        raise PermissionDenied

    profile = Profile.objects.filter(
        user_id__username=request.user.username
        )
    fb_id = list(profile.values('fb_id'))[0]['fb_id']

    endpoint = 'https://graph.facebook.com/{}?fields=friends'.format(fb_id)
    headers = {"Authorization": "Bearer 278758722745488|zgMN8ZoPRELH14yZO8TiQQNGgPM"}
    response = requests.get(endpoint, headers=headers).json()

    friends_data = response['friends']['data']
    friends = []
    for friend in friends_data:
        friends.append(friend['id'])

    profile.update(friends=friends)

    books = Book.objects.filter(user_id__username=request.user.username)

    context = {
        'books': books
    }

    return render(request, 'books/book_list.html', context)


# def book_detail_view(request, pk=None):
#     if not request.user.is_authenticated:
#         return redirect(reverse('login'))

#     book = get_object_or_404(Book, id=pk, user_id__username=request.user.username)

#     context = {
#         'book': book,
#     }

#     return render(request, 'books/book_detail.html', context)

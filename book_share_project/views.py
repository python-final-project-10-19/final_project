from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Profile, Notifications, Book
from allauth.socialaccount.models import SocialAccount
import requests
import os


def home_view(request):
    if request.user.is_authenticated:

        profile = Profile.objects.filter(user__id=request.user.id)

        fb_account = SocialAccount.objects.filter(user__id=request.user.id)

        # We have the right social_account instance (i.e., table row). There has to be an easier way to grab the uid (i.e., the cell in that row)
        uid = list(fb_account.values('uid'))[0]['uid']

        if not profile:

            endpoint = 'https://graph.facebook.com/{}?fields=picture'.format(uid)
            headers = {'Authorization': 'Bearer {}'.format(os.environ.get('FB_GRAPH_TOKEN'))}
            response = requests.get(endpoint, headers=headers).json()
            picture = response['picture']['data']['url']

            Profile.objects.create(
                user=request.user,
                username=request.user.username,
                email=request.user.email,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                fb_id=uid,
                picture=picture,
            )

    return render(request, 'base/home.html')


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('home')

    return render(request, 'custom_account/logout.html')


def notifications_view(request):
    if not request.user.is_authenticated:
        return redirect('home')

    profile = Profile.objects.filter(user__id=request.user.id)
    fb_account = SocialAccount.objects.filter(user__id=request.user.id)
    fb_id = list(fb_account.values('uid'))[0]['uid']

    if request.method == "POST":
        if request.method.POST('response') == 'accepted':
            notification = Notifications.objects.filter(id=request.method.POST('notification')['id'])
            notification.update(status='accepted')

            book = Book.objects.filter(id=request.method.POST('notification')['book_id'])
            book.update(status='checked out')

        if request.method.POST('response') == 'declined':
            notification = Notifications.objects.filter(id=request.method.POST('notification')['id'])
            notification.update(status='declined')

            book = Book.objects.filter(id=request.method.POST('notification')['book_id'])
            book.update(status='available')

        return redirect('/notifications')


    notifications = Notifications.objects.filter(Q(from_user=fb_id) | Q(to_user=fb_id)).order_by('-date_added')

    all_notifications = []

    for notification in notifications:
        type = notification.type
        id = notification.id

        book_id = notification.book_id
        book = Book.objects.filter(id=book_id)[0]
        book_title = book.title

        from_user = notification.from_user
        to_user = notification.to_user
        profile_from_user = Profile.objects.filter(fb_id=from_user)[0]
        profile_to_user = Profile.objects.filter(fb_id=to_user)[0]
        picture_from = profile_from_user.picture
        picture_to = profile_to_user.picture
        name_from = profile_from_user.first_name
        name_to = profile_to_user.first_name

        notification_object = {
            'fb_id': fb_id,
            'type': type,
            'book_id': book_id,
            'book_title': book_title,
            'name_from': name_from,
            'name_to': name_to,
            'picture_from': picture_from,
            'picture_to': picture_to,
        }

        all_notifications.append(notification_object)

    context = {
        'notifications': enumerate(all_notifications)
    }

    # import pdb; pdb.set_trace()

    return render(request, 'base/notifications.html', context)

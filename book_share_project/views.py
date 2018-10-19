from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Profile, Notifications, Book
from allauth.socialaccount.models import SocialAccount
import requests
import os


def home_view(request):
    """
        Home page view,
        if user is logged-in, validates if current user is saved.
        If current user is a new user, saves into our database(Profile model)
    """
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
    """
        Logout page redirecting to home
    """
    if not request.user.is_authenticated:
        return redirect('home')

    return render(request, 'custom_account/logout.html')


def notifications_view(request):
    """
        Grabs all notifications that are related to current user and order by date.
        With each retreived notification, filter and validate it and saves it into another object instance,
        append validated object into a list and returns in a JSON format.
    """
    if not request.user.is_authenticated:
        return redirect('home')

    profile = Profile.objects.filter(user__id=request.user.id)
    fb_account = SocialAccount.objects.filter(user__id=request.user.id)
    fb_id = list(fb_account.values('uid'))[0]['uid']

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



    if request.method == "POST":
        # import pdb; pdb.set_trace()
        if request.POST.get('response') == 'accepted':
            notification = Notifications.objects.filter(id=request.POST.get('notification[id]'))
            notification.update(status='accepted')
            # Notifications.objects.create()
            book = Book.objects.filter(id=request.POST.get('notification[book_id]'))
            book.update(status='checked out')

        if request.POST.get('response') == 'declined':
            notification = Notifications.objects.filter(id=request.POST.get('notification[id]'))
            notification.update(status='declined')

            book = Book.objects.filter(id=request.POST.get('notification[book_id]'))
            book.update(status='available')

        return redirect('/notifications')

    notifications = Notifications.objects.filter(Q(from_user=fb_id) | Q(to_user=fb_id)).order_by('-date_added')

    # import pdb; pdb.set_trace()

    all_notifications = []

    for notification in notifications:
        type = notification.type
        id = notification.id

        book_id = notification.book_id
        book = Book.objects.filter(id=book_id)[0]
        book_title = book.title
        book_status = book.status

        from_user = notification.from_user
        to_user = notification.to_user
        notification_status = notification.status
        profile_from_user = Profile.objects.filter(fb_id=from_user)[0]
        profile_to_user = Profile.objects.filter(fb_id=to_user)[0]
        picture_from = profile_from_user.picture
        picture_to = profile_to_user.picture
        name_from = profile_from_user.first_name
        name_to = profile_to_user.first_name

        notification_object = {
            'id': notification.id,
            'fb_id': fb_id,
            'from_user': from_user,
            'to_user': to_user,
            'type': type,
            'book_id': book_id,
            'book_title': book_title,
            'status': notification_status,
            'name_from': name_from,
            'name_to': name_to,
            'picture_from': picture_from,
            'picture_to': picture_to,
        }

        all_notifications.append(notification_object)

    context = {
        'notifications': enumerate(all_notifications)
    }

    return render(request, 'base/notifications.html', context)

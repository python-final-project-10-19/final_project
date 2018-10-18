from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from .models import Profile
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

    return render(request, 'base/notifications.html')

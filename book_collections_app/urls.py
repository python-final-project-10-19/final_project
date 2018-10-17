from .views import book_list_view, personal_view, friends_view

from django.urls import path

urlpatterns = [
    path('', book_list_view, name='book_list_landing'),
    # path('<int:pk>', book_detail_view, name='book_detail')
    path('personal/', personal_view, name='personal_collection'),
    path('friends/', friends_view, name='friends_collection'),
]


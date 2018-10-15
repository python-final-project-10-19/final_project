from .views.book_add_view import book_add_view
from .views.friends_book_view import book_list_view

from django.urls import path

urlpatterns = [
    path('', book_list_view, name='book_list'),
    # path('<int:pk>', book_detail_view, name='book_detail')
    path('add/', book_add_view, name='book_add'),
]

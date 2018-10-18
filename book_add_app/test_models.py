from django.test import TestCase, RequestFactory
from book_share_project.factories import UserFactory, BookFactory
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from book_share_project.models import Book, Profile
import datetime


class TestBookModel(TestCase):
    def setUp(self):
        """Test setup
        """
        self.user = UserFactory()
        self.user.save()
        SocialAccount.objects.create(
                provider='facebook',
                uid=100128270978326,
                last_login=datetime.datetime.now(),
                date_joined=datetime.datetime.now(),
                extra_data='',
                user_id=self.user.id,
                )

    def test_profile_create(self):
        social_account = SocialAccount.objects.get(user_id=self.user.id)
        fb_id = social_account.uid
        Profile.objects.create(
                user=self.user,
                username=self.user.username,
                email=self.user.email,
                first_name=self.user.first_name,
                last_name=self.user.last_name,
                fb_id=fb_id,
            )
        profile = Profile.objects.get(user_id=self.user.id)
        self.assertEqual(profile.username, self.user.username)

    def test_book_create(self):
        """"""
        self.book = BookFactory()
        self.book.save()

        social_account = SocialAccount.objects.get(user_id=self.user.id)
        fb_id = social_account.uid

        Book.objects.create(
            title=self.book.title,
            owner=fb_id,
            author=self.book.author,
            user_id=self.book.user,
        )
        book = Book.objects.get(title=self.book.title)
        self.assertEqual(book.title, book.title)

    # def test_profile_delete(self):
    #     pass



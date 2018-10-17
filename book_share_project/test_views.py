from django.test import TestCase, Client
from .factories import UserFactory
from allauth.socialaccount.models import SocialAccount
import datetime
import requests


class TestBaseViews(TestCase):
    """Tests for the home page view
    """
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
        self.c = Client()



    def test_home_page_without_login(self):
        """If not logged in, user should see login button.
        """
        response = self.c.get('', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.content)

    def test_home_page_with_login(self):
        """If logged in, user should see logout button.
        """
        self.c.force_login(self.user)

        res = self.c.get('')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Logout', res.content)

    def test_collections_page_without_login(self):
        """If not logged in, should redirect to home page
        """
        res = self.c.get('/books', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Login', res.content)

    def test_collections_page_with_login(self):
        """Login as a user, go to books route to see Collection page"""
        self.c.force_login(self.user)
        res = self.c.get('')
        res = self.c.get('/books', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Collections', res.content)

    def test_add_books_page_without_login(self):
        """If not logged in, should redirect to home page
        """
        res = self.c.get('/books/add', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Login', res.content)

    def test_add_book_form_brings_back_results(self):
        """Test add book for google api to return book results"""
        self.c.force_login(self.user)
        res = self.c.post('/books/add/', data={'query': 'Lord of the rings'}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Lord', res.content)

    def test_book_post_view(self):
        """Test add book to personal library """
        self.c.force_login(self.user)
        res = self.c.get('')
        res = self.c.post('/books/post/', data={
            'title': "Home",
            'author': "Marilynne Robinson",
            'description': "Returning ",
            'image_url': "http://books.google.com/books"},
                          follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Home', res.content)



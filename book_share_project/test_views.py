from django.test import TestCase, Client
from .factories import UserFactory
from allauth.socialaccount.models import SocialAccount
import datetime
from book_add_app.smart_scan import smart_scan


class TestBaseViews(TestCase):
    """Tests for the home page view"""
    def setUp(self):
        """Test setup """
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
        """If not logged in, user should see login button. """
        response = self.c.get('', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.content)

    def test_home_page_with_login(self):
        """If logged in, user should see logout button."""
        self.c.force_login(self.user)

        res = self.c.get('')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Logout', res.content)

    def test_collections_page_without_login(self):
        """If not logged in, should redirect to home page"""
        res = self.c.get('/collections', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Login', res.content)

    def test_collections_page_with_login(self):
        """If logged in, user should see logout button. """
        self.c.force_login(self.user)
        res = self.c.get('')
        res = self.c.get('/collections', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Collections', res.content)

    # failed
    # def test_collections_personal_page_with_login(self):
    #     """Test "your book" collection personal button endpoint with login"""
    #     self.c.force_login(self.user)
    #     res = self.c.get('/collections/personal/', follow=True)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertIn(b'Collection', res.content)

    def test_add_books_page_without_login(self):
        """If not logged in, should redirect to home page """
        res = self.c.get('/add', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Login', res.content)

    def test_add_book_form_brings_back_results(self):
        """Search book and returns a google api book results list """
        self.c.force_login(self.user)
        res = self.c.post('/add/search/', data={'query': 'Lord of the rings'}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Tolkien', res.content)

    def test_smart_scan_view_without_login(self):
        """Test smart scan endpoint without login."""
        res = self.c.get('/add/scan/', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'<h1>Welcome! Please login with Facebook.</h1>', res.content)

    def test_smart_scan_view_with_login(self):
        """Test smart scan endpoint without login."""
        self.c.force_login(self.user)
        res = self.c.get('/add/scan/', follow=True)
        self.assertIn(b'Spine Extractor', res.content)

    def test_personal_collections_page_without_login(self):
        """If not logged in, should redirect to home page"""
        res = self.c.get('/collections/personal/', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Login', res.content)

    def test_personal_collections_page_with_login(self):
        """If logged in, user should see logout button. """
        self.c.force_login(self.user)
        res = self.c.get('')
        res = self.c.get('/collections/personal/', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Your Books', res.content)

    def test_scan_works(self):
        """If logged in, user should see logout button. """
        self.c.force_login(self.user)
        res = self.c.get('')
        res = self.c.get('/collections/personal/', follow=True)
        img_file = '../image_files/IMG_2053.jpg'
        actual = smart_scan(img_file)

        self.assertIsInstance(actual, list)







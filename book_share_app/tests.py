from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import Book


class TestBookModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', email='test@example.com')
        self.user.set_password('hello')

        self.book = Book.objects.create(
            title='Feed the cat',
            author='Scruff McGruff',
            status='complete',
            user_id=self.user
        )

        Book.objects.create(title='War and Peace', author='Tolstoy', status='complete', user_id=self.user)
        Book.objects.create(title='Walden', author='Thoreau', status='complete', user_id=self.user)

    def test_book_titles(self):
        self.assertEqual(self.book.title, 'Feed the cat')

    def test_book_detail(self):
        book = Book.objects.get(title='Walden')
        self.assertEqual(book.author, 'Thoreau')


class TestBookViews(TestCase):
    def setUp(self):
        """Set up function for view testing
        """
        self.request = RequestFactory()
        self.user = User.objects.create(username='test2', email='test2@example.com')
        self.user.set_password('hello2')

        self.book_one = Book.objects.create(title='War and Peace', author='Tolstoy', status='complete', user_id=self.user)
        self.book_two = Book.objects.create(title='Walden', author='Thoreau', status='complete', user_id=self.user)

    def test_book_detail_view(self):
        """Get book one and verify that title contains part of the title passed in.
        """
        from .views import book_detail_view
        request = self.request.get('')
        request.user = self.user
        response = book_detail_view(request, f'{self.book_one.id}')
        self.assertIn(b'Peace', response.content)

    def test_book_detail_status(self):
        """Test that status code for book_detail_view is a 200.
        """
        from .views import book_detail_view
        request = self.request.get('')
        request.user = self.user
        response = book_detail_view(request, f'{self.book_one.id}')
        self.assertEqual(200, response.status_code)

    def test_book_list_view(self):
        """Verify that the full book list contains one of the titles above.
        """
        from .views import book_list_view
        request = self.request.get('')
        request.user = self.user
        response = book_list_view(request)
        self.assertIn(b'Walden', response.content)

    def test_book_list_status(self):
        """Test that status code for book_list_view is a 200.
        """
        from .views import book_list_view
        request = self.request.get('')
        request.user = self.user
        response = book_list_view(request)
        self.assertEqual(200, response.status_code)

    def test_book_detail_date_filter(self):
        from .views import book_detail_view
        request = self.request.get('')
        request.user = self.user
        response = book_detail_view(request, f'{self.book_one.id}')

        self.assertIn(b'Created: Today.', response.content)

# from django.test import TestCase, RequestFactory
# from django.contrib.auth.models import User
# from .models import Book


# class TestBookModel(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(username='test', email='test@example.com')
#         self.user.set_password('hello')

#         self.book = Book.objects.create(
#             title='Feed the cat',
#             author='Scruff McGruff',
#             status='complete',
#             user=self.user
#         )

#         Book.objects.create(title='War and Peace', author='Tolstoy', status='complete', user=self.user)
#         Book.objects.create(title='Walden', author='Thoreau', status='complete', user=self.user)

#     def test_book_titles(self):
#         self.assertEqual(self.book.title, 'Feed the cat')

#     def test_book_detail(self):
#         book = Book.objects.get(title='Walden')
#         self.assertEqual(book.author, 'Thoreau')




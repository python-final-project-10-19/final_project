from django.test import TestCase, RequestFactory
from book_share_project.factories import UserFactory, BookFactory
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from book_share_project.models import Book, Profile, Notifications
import datetime


# models test
class ProfileTest(TestCase):
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

    def create_profile(self, username='ben', email='bhurst8@gmail.com', first_name='ben', last_name='hurst', fb_id='13719073', picture='http://asdjkhvbkajdhs.com', friends=['24910', '20480124'], user_id=1):
        return Profile.objects.create(username=username, email=email, first_name=first_name, last_name=last_name, fb_id=fb_id, picture=picture, friends=friends, user_id=self.user.id)

    def test_profile_creation(self):
        p = self.create_profile()
        self.assertTrue(isinstance(p, Profile))
        self.assertEqual(p.username, 'ben')





# class TestProfileModel(TestCase):
#     def setUp(self):
#         """Test setup
#         """
#         self.user = UserFactory()
#         self.user.save()
#         SocialAccount.objects.create(
#                 provider='facebook',
#                 uid=100128270978326,
#                 last_login=datetime.datetime.now(),
#                 date_joined=datetime.datetime.now(),
#                 extra_data='',
#                 user_id=self.user.id,
#                 )

#     def test_profile_create(self):
#         social_account = SocialAccount.objects.get(user_id=self.user.id)

#         fb_id = social_account.uid
#         test_profile = Profile(
#                 user=self.user,
#                 username=self.user.username,
#                 email=self.user.email,
#                 first_name=self.user.first_name,
#                 last_name=self.user.last_name,
#                 fb_id=fb_id,
#             )
#         test_profile.save()
#         returned_profile = Profile.objects.get(user_id=self.user.id)
#         self.assertEqual(returned_profile.username, test_profile.username)

#     def test_profile_is_deleted(self):
#         """Profile has beed deleted."""
#         self.assertEqual(Profile.objects.count(), 0)


# # class TestBookModel(TestCase):

# #     def setUp(self):
# #         """ create user
# #         """
# #         self.user = UserFactory()
# #         self.user.save()
# #         SocialAccount.objects.create(
# #                 provider='facebook',
# #                 uid=100128270978326,
# #                 last_login=datetime.datetime.now(),
# #                 date_joined=datetime.datetime.now(),
# #                 extra_data='',
# #                 user_id=self.user.id,
# #                 )
# #         """create book
# #         """
# #         book = BookFactory()
# #         book.user = self.user
# #         user_id = self.user.id
# #         book.save()
# #         self.book = book


# #     def test_book_create(self):
# #         """"""


# #         self.assertEqual(Book.objects.count(), 1)




# class TestNotificationsModel(TestCase):
#     def setUp(self):
#         """Test setup
#         """
#         self.user = UserFactory()
#         self.user.save()
#         SocialAccount.objects.create(
#                 provider='facebook',
#                 uid=100128270978326,
#                 last_login=datetime.datetime.now(),
#                 date_joined=datetime.datetime.now(),
#                 extra_data='',
#                 user_id=self.user.id,
#                 )


#         """create notification
#         """
#     def test_notifications_create(self):
#         social_account = SocialAccount.objects.get(user_id=self.user.id)
#         fb_id = social_account.uid

#         Profile.objects.create(
#             user=self.user,
#             username=self.user.username,
#             email=self.user.email,
#             first_name=self.user.first_name,
#             last_name=self.user.last_name,
#             fb_id=fb_id,
#         )

#         Notifications.objects.create(
#             type='request',
#             status='pending',
#             from_user=fb_id,
#             to_user=fb_id,
#             book_id='2',
#         )
#         profile = Profile.objects.get(user_id=self.user.id)
#         notifications = Notifications.objects.get()
#         self.assertEqual(notifications.type, 'request')
#         self.assertEqual(notifications.status, 'pending')
#         self.assertEqual(notifications.from_user, profile.fb_id)
#         self.assertEqual(notifications.from_user, profile.fb_id)
#         self.assertEqual(notifications.book_id, '2')

#     def test_notifications_is_deleted(self):
#         """Profile has beed deleted."""
#         self.assertEqual(Notifications.objects.count(), 0)

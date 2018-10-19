from django.contrib.auth.models import User
from book_share_project.models import Profile, Book
from faker import Faker
import factory

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Create a test user for writing tests."""

    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    # username = 'olivia'
    # email = 'mkyqzpevqr_1539464428@tfbnw.net'
    # first_name = 'Olivia'
    # last_name = 'Dingleberg'


class BookFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=4)
    author = factory.Faker('name')
   


# class SocialAccountFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = SocialAccount


# class ProfileFactory(factory.django.DjangoModelFactory):
#     """Create a test profile for writing tests."""

#     class Meta:
#         model = Profile

#     user = factory.SubFactory(UserFactory)
#     username = user.username
#     email = user.email
#     first_name = user.first_name
#     last_name = user.last_name
#     fb_id = 64976597687



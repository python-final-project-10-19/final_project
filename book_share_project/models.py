from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MaxValueValidator


class Profile(models.Model):
    """
        Visited user information gets saved onto profile class.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    username = models.CharField(max_length=48, null=True)
    email = models.CharField(max_length=48, null=True)
    first_name = models.CharField(max_length=48, null=True)
    last_name = models.CharField(max_length=48, null=True)
    fb_id = models.CharField(max_length=48, null=True)
    picture = models.URLField(max_length=1024)
    friends = ArrayField(models.CharField(max_length=48), null=True)

    # def __str__(self):
    #     return 'Profile: {} ({})'.format(self.username, self.fb_id)

    # def __repr__(self):
    #     return 'Profile: {} ({})'.format(self.username, self.fb_id)


class Book(models.Model):
    """
        Book class saved when registered user adds a new book to their collection.
    """
    STATES = [
        ('available', 'Available'),
        ('checked out', 'Checked Out'),
        ('requested', 'Requested'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    # profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='books')
    owner = models.CharField(max_length=48, null=True)
    borrower = models.CharField(max_length=48, blank=True, null=True)
    requester = models.CharField(max_length=48, blank=True, null=True)
    title = models.CharField(max_length=48)
    author = models.CharField(max_length=4096)
    image_url = models.URLField(max_length=1024, null=True)
    year = models.CharField(max_length=48, blank=True, null=True)
    status = models.CharField(choices=STATES, default='available', max_length=48)
    date_added = models.DateTimeField(auto_now=True, blank=True)
    last_borrowed = models.DateTimeField(blank=True, null=True)
    pre_save_status = models.CharField(max_length=48, editable=False)

    # def __str__(self):
    #     return 'Book: {} ({})'.format(self.title, self.status)

    # def __repr__(self):
    #     return 'Book: {} ({})'.format(self.title, self.status)


@receiver(models.signals.post_save, sender=Book)
def set_book_borrowed_date(sender, instance, **kwargs):
    """
        Triggers when a book gets checked out to a user.
        Updates the status of Book objects.
    """
    if instance.status == 'checked out' and instance.pre_save_status == 'available':
        instance.last_borrowed = timezone.now()
        instance.pre_save_status = 'checked out'
        instance.save()


@receiver(models.signals.pre_save, sender=Book)
def set_pre_save_status(sender, instance, **kwargs):
    """
        Sets the initial status of Book object once gets instantiates.
    """
    if instance.status == 'available':
        instance.pre_save_status = 'available'


class Document(models.Model):
    docfile = models.FileField(upload_to='documents')


class Notifications(models.Model):
    """
        Class that holds all activities occurs within the application.
        Used to keep all actions of users in the application.
    """
    TYPES = [
        ('request', 'Request'),
        ('response', 'Response'),
    ]

    type = models.CharField(choices=TYPES, max_length=48)
    status = models.CharField(max_length=48, null=True)
    from_user = models.CharField(max_length=48, null=True)
    to_user = models.CharField(max_length=48, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True)
    book_id = models.CharField(max_length=48, null=True)

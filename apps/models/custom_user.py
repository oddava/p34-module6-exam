from django.contrib.auth.models import AbstractUser
from django.db.models.fields import TextField, CharField, URLField, EmailField


class CustomUser(AbstractUser):
    email = EmailField(unique=True)
    username = None
    phone_number = CharField(max_length=20, blank=True)
    mobile_number = CharField(max_length=20, blank=True)
    pfp_url = URLField(max_length=255, blank=True)
    role = TextField(max_length=255, blank=True)
    company = TextField(max_length=255, blank=True)
    skype = TextField(max_length=255, blank=True, null=True)
    facebook_url = TextField(blank=True, null=True)
    linkedin_url = TextField(blank=True, null=True)
    twitter_url = TextField(blank=True, null=True)

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'user'
        verbose_name_plural = 'users'
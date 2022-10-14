from django.db import models

# Importing the settings module from Django
from django.conf import settings

# Create your models here.


class Profile(models.Model):

    # This is a one-to-one association to the Django user with which the profile is associated
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    # This is an optional URL where we can learn more about the user
    website = models.URLField(blank=True)

    # This is an optional, tweet-sized blurb to learn more about the user quickly
    bio = models.CharField(max_length=240, blank=True)

    # This makes Profile objects we create appear in a more human-friendly manner on the admin site
    def __str__(self):
        return self.user.get_username()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    # Again, this makes any Tag objects we create appear in a more human-friendly manner on the admin site
    def __str__(self):
        return self.name


class Post(models.Model):

    # This allows our blog posts to be ordered by publish date, with the most recent being first
    class Meta:
        ordering = ["-publish_date"]

    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField()
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    # This ensures that authors that still have posts aren't accidentally deleted
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)

    tags = models.ManyToManyField(Tag, blank=True)

from django.contrib import admin

# Register your models here.

# First, we import the models we have created
from blog.models import Profile, Post, Tag

# Now, we register our models with in admin.py file.
# In doing so, we can define how we want this data to be displayed in the admin interface


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post

    # This specifies to Django which specific fields we want to see about each post in the admin interface
    # The order of attributes we include creates a tuple with that order
    list_display = (
        "id",
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    )

    # This defines which fields by which we want to allow filtering
    list_filter = (
        "published",
        "publish_date",
    )

    # This defines which displayed fields can be edited. We omit the ID field for obvious reasons
    list_editable = (
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    )

    # Allows us to search by these fields
    search_fields = (
        "title",
        "subtitle",
        "slug",
        "body",
    )

    # This makes it so the 'slug' field automatically consists of the title and subtitle
    prepopulated_fields = {
        "slug": (
            "title",
            "subtitle",
        )
    }

    # This uses the publish_date of all posts to create a browsable date hierarchy
    date_hierarchy = "publish_date"

    # This creates a button at the top to allow changes to be saved
    save_on_top = True

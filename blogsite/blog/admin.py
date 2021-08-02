from django.contrib import admin
# from blog.models import user_entry
from blog.models import Post
from blog.models import Comment
from blog.models import Profile
# Register your models here.


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)


# To make our model visible on the admin page, we need to register the model with admin.site.register(Post).

# IMPORTANT TIP
# Whenever you edit the admin.py file or create a new model, run migrate command to migrate changes to the database.

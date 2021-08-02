from django.db import models
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404,  redirect
from django.http import HttpResponseRedirect, HttpResponse

from django.urls import reverse

from django.conf import settings
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE,blank=False,null=True)
    title = models.CharField(max_length=200)
    header_image = models.ImageField(blank = True, null=True, upload_to="images/")
    text = RichTextField(blank=True, null=True)
    created_date = models.DateTimeField(blank = True, null= True)
    published_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={'pk':self.pk})

    def total_likes(self):
        return self.likes.count()


    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
        # from total comments on post , only approved comments will be filtered and returned (shown on blog ), unapproved comments will be rejected.


    def publish(self):
        self.published_date = timezone.now()
        # self - connects method and its arguments to instance of a class.
        self.save()

    def __str__(self):
        return self.title
    # when we call __str__() we will get a text (string) with a Post title.

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments',null= True)
    # The related_name option in models.ForeignKey allows us to have access to comments from within the Post model.
    author = models.CharField(max_length=200,blank=False)
    text = models.TextField(blank=False)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)


    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE )
    bio = models.TextField(blank=False)
    profile_pic =  models.ImageField(blank = True, null=True, upload_to="images/profile")
    fb_url = models.CharField(max_length=255,blank = True, null=True)
    pratilipi_url = models.CharField(max_length=255,blank = True, null=True)
    linkedin_url = models.CharField(max_length=255,blank = True, null=True)

    def get_absolute_url(self):
        return reverse("blog:show_profile_page", kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.user)


     #  HOW TO SAVE OUR MODEL IN DATABASE?
     # First we have to make Django know that we have some changes in our model.
     #  (We have just created it!) Go to your console window and type python manage.py makemigrations blog
     #
     #  Django prepared a migration file for us that we now have to apply to our database. Type python manage.py migrate blog.
     #
     #  Our Post model is now in our database! It would be nice to see it, right? Jump to the next chapter to see what your Post looks like!

     # To add, edit and delete the posts we've just modeled, we will use Django admin.
     # To make our model visible on the admin page, we need to register the model with admin.site.register(Post).

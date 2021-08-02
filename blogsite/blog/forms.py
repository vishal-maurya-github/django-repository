from django import forms
from django.contrib.auth.models import User
# from  blog.models import user_entry
from blog.models import Post
from blog.models import Comment
from blog.models import Profile

class user_entry_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model=User
        fields = ('username','email','password')

# class Meta : to use fields of models in ur app.


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author','title','text','header_image')

# In this scenario we want only title and text to be exposed – author should be the person who is currently logged in (you!) and created_date should be automatically set when we create a post (i.e. in the code), right?

# And that's it! All we need to do now is use the form in a view and display it in a template.


class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author','text')

class ProfilePageForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('bio','profile_pic','fb_url','pratilipi_url','linkedin_url')

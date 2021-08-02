from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse

from django.urls import reverse,reverse_lazy

from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView

from django.contrib.auth.forms import UserChangeForm
from blog import models

# from blog.models import user_entry
from blog.forms import user_entry_form

from blog.models import Post
from blog.forms import PostForm

from blog.models import Comment
from blog.forms import CommentForm

from blog.models import Profile
from blog.forms import ProfilePageForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.utils import timezone



# Create your views here.

# CLASS BASED VIEWS

# HOME PAGE
class HomeView(TemplateView):
    template_name = 'home.html'

# ABOUT PAGE
class AboutView(TemplateView):
    template_name = 'about.html'

class ProfileTemplateView(TemplateView):
    template_name = 'profile2.html'

# SHOW PROFILE PAGE VIEW
class ShowProfilePageView(DetailView):
    # why DetailView ?
    # Whenever we look up a blog post, that specific blog post is DetailView and this is sort of the same thing.
    # ....We have got bunch of users here and we wanna look in their profile detail so will use DetailView.
        model = models.Profile
        template_name = 'user_profile.html'

    # Everytime user goes to a profile page, we need to look up at user profile.
    # .. In order to know what user to look up , we gonnna need to pass our view their id no.
    #  and we will get this id no. from url.
    #  and the same we have done in other urls.

    # after defining url in urls.py , we need to get this <int:pk> thing in this view
        def get_context_data(self, *args, **kwargs):
            context = super(ShowProfilePageView, self).get_context_data( *args, **kwargs)
            # instead of grabbing everything let's just grab a specific user.
            page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
            # this primary key above , we are getting from self.kwargs which is getting passed in through the url.
            context["page_user"] = page_user
            return context
            # now we can use this context variable to show user details on  profile page(we just created).

# AUTHOR POST LIST
class AuthorPostListView(ListView):
    context_object_name = 'posts'
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # model= Post
    model = models.Post
    # def get_queryset(self):
    #     return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    template_name ='blog/profile.html'




# CREATE PROFILE PAGE VIEW
class CreateProfilePageView(CreateView):
    model = models.Profile
    form_class = ProfilePageForm
    template_name = 'blog/create_user_profile_page.html'

    # after creating form at create_user_profile_page.html, we need to know which user is filling that form for that we need below fn.
    # below django method i.e. form_valid is called when correct data is entered into the form and the form has been successfully validated without any errors.
    def form_valid(self,form):
        form.instance.user = self.request.user
        # what this does is , it's saying hey ! there is user filling out this form , let's grab that user and make it available to the form itself(i.e. form.instance.user).
        # and then we can just save the form by....
        return super().form_valid(form)
    # print(super().form_valid(form))
        # and we pass in the form itself that has been submitted from the page.
        # what this return ? -What it returns is the result of the superclass implementation of the method, which happens to be a redirect to the success URL.

        # EXTRA CONCEPTS : The super () function is used to give access to methods and properties of a parent or sibling class.
        # The super () function returns an object that represents the parent class.
# CONCLUSION : we are making user id available to our profile so that when we save the form it get saved under the right user.
# Explained By e.g. of Bob ( NEW USER )
# bill when he creates his profile page , bill is user 7 (say) that 7 will pass as argument 'self' in form_valid()
# ...we can set it up into the form as the instance of the form with that user and set it equal to that 7 (ie. self.request.user would be 7 now ).
#  ...we are saying hey take 7 (self.request.user ) put it on the form as the user and then save the form.


# EDIT PROFILE PAGE VIEW
class EditProfilePageView(UpdateView):
    model = models.Profile
    template_name = 'blog/edit_profile_page.html'
    fields = ['bio','profile_pic','fb_url','pratilipi_url','linkedin_url']
    success_url = reverse_lazy('blog:author_post_list')












# FUNCTION TO REGISTER

def register(request):

    registered = False

    # we will depend on this variable to tell if someone is registered or not!

    if request.method == "POST":
        UserEntryForm = user_entry_form(data=request.POST)

        # Check to see both forms are valid
        if UserEntryForm.is_valid():

            # Save User Form to Database
            user = UserEntryForm.save()
            # Hash the password
            user.set_password(user.password)

            # Update Database with Hashed password

            user.save()
            registered = True

        else:
            print(UserEntryForm.errors)

    else:
        UserEntryForm = user_entry_form()


    return render(request,'blog/register.html',
                                        {'UserEntryForm':UserEntryForm,
                                          'registered':registered})

# CLASS TO UPDATE SETTINGS
class UserEditView(UpdateView):
    form_class = UserChangeForm
    template_name = 'blog/edit_profile.html'
    success_url = reverse_lazy('home')

# funtion to make edit profile form know who the user is
    def get_object(self):
        return self.request.user



# FUNCTION TO LOG IN

def user_login(request):
    # log_in = False
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        # If we have a user
        if user:
            #Check if the account is active
            if user.is_active:

                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                # log_in = True

                return redirect('home')
                # return HttpResponseRedirect(request,reverse('home'),{'log_in':log_in})

            else:
                # If account is not active:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed.")
            print("Username: {} and password: {} ".format(username,password))
            return HttpResponse("invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'blog/login.html', {})

# FUNCTION TO LOG OUT

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

# POST LIST
class PostListView(ListView):
    context_object_name = 'posts'
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # model= Post
    model = models.Post
    # def get_queryset(self):
    #     return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    template_name = 'post_list.html'




# POST DETAIL
class PostDetailView(DetailView):
    context_object_name = 'post'
    model = models.Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        stuff= get_object_or_404(Post, id=self.kwargs['pk'])
        # pk has been passed because if we are on post 15 , we wana look up post with id 15
        total_likes = stuff.total_likes()
        context["total_likes"]=total_likes
        return context

# POST DETAIL
# class LikeDetailView(DetailView):
#     context_object_name = 'post'
#     model = models.Post
#     template_name = 'blog/post_list.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(LikeDetailView, self).get_context_data(**kwargs)
#         stuff= get_object_or_404(Post, id=self.kwargs['pk'])
#         # pk has been passed because if we are on post 15 , we wana look up post with id 15
#         total_likes = stuff.total_likes()
#         context["total_likes"]=total_likes
#         return context





# POST LIKE FUNCTION
def LikeView(request, pk):
    # here we need to save a post which is being liked !
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    # after submitting form, we grab the post id as we named it in form(in post_detail.html) as name='post_id'
    # ...and then whatever the post that has thid id , look that up in Post table
    # ..and assign all of that in this post variable .
    post.likes.add(request.user)
    # here not only we are saving a like but saving a like from a user, means vishal or alok likes this post so we have to
    # pass that user also in.
    return HttpResponseRedirect(reverse('blog:post_detail',args=[str(pk)]))
    # return back user to same page after liking the post.(pk has been passed so that user gets to see post which he liked )






# POST CREATE
class PostCreateView(CreateView):
    fields = ('author','title', 'text','header_image')
    # These are fields that we will allow user to create.
    # it almost  acts like a security measure, may be we don'want someone to edit the location of school or the name of school etc.
    model = models.Post


# POST UPDATE
class PostUpdateView(UpdateView):
    fields = ('author','title', 'text','header_image')
    model = models.Post

# POST DELETE
class PostDeleteView(DeleteView):
    model = models.Post
    success_url = reverse_lazy('blog:author_post_list')

 # COMMENT CREATE
def add_comment_to_post(request,pk):
    # In order to add comment to a post, we take in a request & the primary key that links the actual comment to the post.
    #  So, if u are on post detail page and you click OK, i want to comment on this , there is a primary key that goes along with that post.
    post = get_object_or_404(Post,pk=pk)
        # either get that post object or 404 page (means u can't find it ) and pass in the Post model and then pk=pk.
    #   IF SOMEONE COMMENTS
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            comment.post = post
            #  connecting that particular comment to the Post's object.(see models for clarification , where post is field of Comment Model)
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
            # after comment done , redirecting user to post_detail page and also making post's primary key equal to comment primary key.
        #   IF SOMEONE DOES NOT COMMENT
    else:
        form = CommentForm()
        return render(request,'blog/comment_form.html',{'form':form})

# COMMENT APPROVE
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)
# pk=comment.post.pk ?
    # remember the comment is connected to a particular post (in Comment Model),& if we want to approve that comment , go to the post of that comment ,
    # ...then i need the post.pk
    # ...now we actually go to Post Model ,and we will ask what's the primary key of the post that this comment was linked to
    # ...(as post of Comment Model is a foreign key, so we can grab primary key from Post Model )

# COMMENT DELETE
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:post_detail',pk=post_pk)

from blog import views
from django.conf.urls import url
from django.urls import path


app_name = 'blog'

urlpatterns = [

    url(r'^login/$', views.user_login,name='login'),
    url(r'^about/$', views.AboutView.as_view(),name='about'),

    url(r'^register/$', views.register,name='register'),
    path('edit_profile/', views.UserEditView.as_view(), name='edit_profile'),

    url(r'^logout/$', views.user_logout,name='logout'),

    url(r'^post_list/$', views.PostListView.as_view(),name='post_list'),
    url(r'^author_post_list/$', views.AuthorPostListView.as_view(),name='author_post_list'),


    url(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),

    # This means if you enter http://127.0.0.1:8000/post/5/ into your browser,
    # Django will understand that you are looking for a view called post_detail and transfer the information that pk equals 5 to that view.
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
    path('like/<int:pk>', views.LikeView, name='like_post'),
    path('profile/', views.ProfileTemplateView.as_view(), name='profile'),
    path('<int:pk>/edit_profile_page/', views.EditProfilePageView.as_view(), name='edit_profile_page'),
    path('<int:pk>/profile/', views.ShowProfilePageView.as_view(), name='show_profile_page'),

    path('create_profile_page/', views.CreateProfilePageView.as_view(), name='create_profile_page'),

]

from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'basic_app'

urlpatterns=[
    path('relative/',views.relative,name='relative'),
    path('other/',views.other,name='other'),
]






# from  basic_app import views
# from django.urls import path
#
# # TEMPLATE TAGGING
#
# app_name= 'basic_app'
# # basically tells django to look into the basic_app and find the url that matches.
#
# urlpatterns = [
# path(r'^relative/',views.relative,name='relative'),
# path(r'^other/',views.other,name='other'),
# ]

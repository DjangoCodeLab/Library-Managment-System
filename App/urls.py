from django.urls import path
from App.views import *
urlpatterns = [
    path('',home,name = 'home'),
    path('products',products,name = 'products'),
    path('login', login_user,name = 'login' ),
    path('register', register_user, name = 'register'),
    path('logout', logout_user, name = 'logout_user'),
    path('profile/',profile,name = 'profile'),
    path('edit-profile/',edit_profile,name = 'edit_profile'),
    path('update/<id>',update_book , name = 'update'),
    path('delete/<id>',delete , name = 'delete'),
]

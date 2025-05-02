
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views

from .views import *


#Translated
urlpatterns = (

	path('login/', login_user, name='login'), 

	path('logout/', logout, name='logout'), 

	path('register_user/', register_user, name='register_user'), 

	path('home/', home, name='home'), 

	path('messages/', messages, name='messages'), 

	path('users/', users, name='users'), 


	# path('user_profile/<user_id>/', user_profile, name='user_profile'),

)

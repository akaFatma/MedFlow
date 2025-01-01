from django.urls import path
from . import views


urlpatterns = [
    path('test', views.test_token, name='test'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
]

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from .views import get_cookie_view, set_cookie_view, set_session_view, get_session_view, AboutMeView, RegisterView, logout_view, FooBarView, HelloView
from django.urls import path

app_name = 'myauth'

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('logout/', logout_view, name='logout'),
    path('login/', LoginView.as_view(template_name='myauth/login.html', redirect_authenticated_user=True), name='login'),
    path('cookie/get', get_cookie_view, name='cookie_get'),
    path('cookie/set', set_cookie_view, name='cookie_set'),
    path('session/set', set_session_view, name='session_set'),
    path('session/get', get_session_view, name='session_get'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('register/', RegisterView.as_view(), name='register'),
    path('foo-bar/', FooBarView.as_view(), name='foo-bar'),

]

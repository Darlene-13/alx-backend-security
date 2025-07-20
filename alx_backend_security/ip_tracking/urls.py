from django.urls import path
from . import views

urlpatterns = [
    path("fake-login/", views.anonymous_login, name="anon_login"),
    path("secure-login/", views.authenticated_login, name="auth_login")
]
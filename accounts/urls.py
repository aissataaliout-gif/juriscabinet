from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("login/", views.login_view, name="login"),

    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),

    path("register/", views.register_view, name="register"),
]
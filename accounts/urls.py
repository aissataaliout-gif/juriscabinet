from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.lawyer_list, name="lawyer_list"),
    path("nouveau/", views.lawyer_create, name="lawyer_create"),
    path("<int:pk>/modifier/", views.lawyer_update, name="lawyer_update"),
    path("<int:pk>/supprimer/", views.lawyer_delete, name="lawyer_delete"),
    path("dashboard/", views.lawyer_dashboard, name="lawyer_dashboard"),
]
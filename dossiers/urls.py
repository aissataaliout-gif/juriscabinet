from django.urls import path
from . import views

urlpatterns = [
    path("", views.dossier_list, name="dossier_list"),
    path("<int:pk>/", views.dossier_detail, name="dossier_detail"),
    path("nouveau/", views.dossier_create, name="dossier_create"),
    path("<int:pk>/modifier/", views.dossier_update, name="dossier_update"),
    path("<int:pk>/supprimer/", views.dossier_delete, name="dossier_delete"),
]
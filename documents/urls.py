from django.urls import path
from . import views

urlpatterns = [
    path("", views.document_list, name="document_list"),
    path("nouveau/", views.document_create, name="document_create"),
    path("<int:pk>/modifier/", views.document_update, name="document_update"),
    path("<int:pk>/supprimer/", views.document_delete, name="document_delete"),
]
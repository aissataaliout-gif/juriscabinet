from django.urls import path
from . import views

urlpatterns = [
    path("", views.invoice_list, name="invoice_list"),
    path("nouvelle/", views.invoice_create, name="invoice_create"),
    path("<int:pk>/modifier/", views.invoice_update, name="invoice_update"),
    path("<int:pk>/supprimer/", views.invoice_delete, name="invoice_delete"),
]
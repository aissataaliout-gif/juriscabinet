from django.urls import path
from . import views

urlpatterns = [
    path("", views.message_create, name="message_create"),
    path("inbox/", views.inbox, name="inbox"),
    path("<int:pk>/", views.message_detail, name="message_detail"),
    path("sent/", views.sent_messages, name="sent_messages"),
]
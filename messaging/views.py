from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message
from .forms import MessageForm
from notifications.models import Notification


@login_required
def message_create(request):
    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()

            Notification.objects.create(
    user=message.receiver,
    title="Nouveau message",
    message=f"Vous avez reçu un nouveau message de {request.user.username}."
)

            messages.success(request, "Le message a été envoyé avec succès.")
            return redirect("message_create")

    else:
        form = MessageForm()

    return render(
        request,
        "messaging/message_form.html",
        {"form": form},
    )
@login_required
def inbox(request):
    messages_received = Message.objects.filter(
        receiver=request.user
    ).order_by("-sent_at")

    return render(
        request,
        "messaging/inbox.html",
        {"messages_received": messages_received},
    )
@login_required
def message_detail(request, pk):
    message = get_object_or_404(
        Message,
        pk=pk,
        receiver=request.user
    )

    if not message.is_read:
        message.is_read = True
        message.save()

    return render(
        request,
        "messaging/message_detail.html",
        {"message": message},
    )
@login_required
def sent_messages(request):
    sent = Message.objects.filter(
        sender=request.user
    ).order_by("-sent_at")

    return render(
        request,
        "messaging/sent_messages.html",
        {"sent_messages": sent},
    )
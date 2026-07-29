from django.shortcuts import render,redirect,get_object_or_404
from .models import Client
from .forms import ClientForm
from django.contrib import messages

def client_list(request):
    clients = Client.objects.all()
    return render(request, "clients/client_list.html", {
        "clients": clients
    })


def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST, request.FILES)

        if form.is_valid():
           form.save()
           messages.success(request, "Le client a été ajouté avec succès.")
        return redirect("client_list")
    else:
        form = ClientForm()

    return render(request, "clients/client_form.html", {
        "form": form
    })
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        form = ClientForm(request.POST, request.FILES, instance=client)

        if form.is_valid():
           form.save()
           messages.success(request, "Le client a été modifié avec succès.")
        return redirect("client_list")
    else:
        form = ClientForm(instance=client)

    return render(request, "clients/client_form.html", {
        "form": form
    })
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.delete()
        messages.success(request, "Le client a été supprimé avec succès.")
        return redirect("client_list")

    return render(request, "clients/client_confirm_delete.html", {
        "client": client
    })
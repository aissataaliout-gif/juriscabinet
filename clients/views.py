from django.shortcuts import render,redirect,get_object_or_404
from .models import Client
from .forms import ClientForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from dossiers.models import Dossier
from appointments.models import Appointment
from documents.models import Document
from billing.models import Invoice


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

@login_required
def client_dashboard(request):
    client = request.user.client_profile

    dossiers = Dossier.objects.filter(client=client)
    documents = Document.objects.filter(dossier__client=client)
    invoices = Invoice.objects.filter(dossier__client=client)
    appointments = Appointment.objects.filter(dossier__client=client)

    context = {
        "client": client,
        "dossiers": dossiers,
        "documents": documents,
        "invoices": invoices,
        "appointments": appointments,
        "dossiers_count": dossiers.count(),
        "documents_count": documents.count(),
        "invoices_count": invoices.count(),
        "appointments_count": appointments.count(),
    }

    return render(
        request,
        "clients/client_dashboard.html",
        context,
    )
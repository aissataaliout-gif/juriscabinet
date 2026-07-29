from django.shortcuts import render, redirect, get_object_or_404
from .models import Dossier
from .forms import DossierForm
from django.contrib import messages

def dossier_list(request):
    dossiers = Dossier.objects.all()

    return render(request, "dossiers/dossier_list.html", {
        "dossiers": dossiers
    })
def dossier_create(request):
    if request.method == "POST":
        form = DossierForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Le dossier a été créé avec succès.")
            return redirect("dossier_list")
    else:
        form = DossierForm()

    return render(request, "dossiers/dossier_form.html", {
        "form": form
    })
def dossier_update(request, pk):
    dossier = get_object_or_404(Dossier, pk=pk)

    if request.method == "POST":
        form = DossierForm(request.POST, instance=dossier)

        if form.is_valid():
            form.save()
            messages.success(request, "Le dossier a été modifié avec succès.")
            return redirect("dossier_list")
    else:
        form = DossierForm(instance=dossier)

    return render(request, "dossiers/dossier_form.html", {
        "form": form
    })
def dossier_delete(request, pk):
    dossier = get_object_or_404(Dossier, pk=pk)

    if request.method == "POST":
        dossier.delete()
        messages.success(request, "Le dossier a été supprimé avec succès.")
        return redirect("dossier_list")

    return render(request, "dossiers/dossier_confirm_delete.html", {
        "dossier": dossier
    })
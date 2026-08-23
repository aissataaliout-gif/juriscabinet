from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Dossier
from .forms import DossierForm


@login_required
def dossier_list(request):

    # ADMIN : voit tous les dossiers
    if request.user.role == "ADMIN":
        dossiers = Dossier.objects.all()

    # CLIENT : voit uniquement ses propres dossiers
    elif request.user.role == "CLIENT":
        client = request.user.client_profile
        dossiers = Dossier.objects.filter(client=client)

    # AVOCAT : temporairement, on conserve l'accès existant.
    # Nous sécuriserons précisément ses dossiers après vérification
    # du lien User ↔ Lawyer.
    elif request.user.role == "LAWYER":
        dossiers = Dossier.objects.all()

    else:
        return HttpResponseForbidden("Accès refusé.")

    return render(
        request,
        "dossiers/dossier_list.html",
        {
            "dossiers": dossiers
        }
    )


@login_required
def dossier_create(request):

    # Seuls ADMIN et AVOCAT peuvent créer un dossier
    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à créer un dossier.")

    if request.method == "POST":
        form = DossierForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Le dossier a été créé avec succès."
            )
            return redirect("dossier_list")

    else:
        form = DossierForm()

    return render(
        request,
        "dossiers/dossier_form.html",
        {
            "form": form
        }
    )


@login_required
def dossier_update(request, pk):

    dossier = get_object_or_404(Dossier, pk=pk)

    # Le client ne peut pas modifier
    if request.user.role == "CLIENT":
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à modifier ce dossier."
        )

    # Seuls ADMIN et AVOCAT peuvent modifier
    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden("Accès refusé.")

    if request.method == "POST":
        form = DossierForm(
            request.POST,
            instance=dossier
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Le dossier a été modifié avec succès."
            )
            return redirect("dossier_list")

    else:
        form = DossierForm(instance=dossier)

    return render(
        request,
        "dossiers/dossier_form.html",
        {
            "form": form
        }
    )


@login_required
def dossier_delete(request, pk):

    dossier = get_object_or_404(Dossier, pk=pk)

    # Seuls ADMIN et AVOCAT peuvent supprimer
    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à supprimer ce dossier."
        )

    if request.method == "POST":
        dossier.delete()

        messages.success(
            request,
            "Le dossier a été supprimé avec succès."
        )

        return redirect("dossier_list")

    return render(
        request,
        "dossiers/dossier_confirm_delete.html",
        {
            "dossier": dossier
        }
    )
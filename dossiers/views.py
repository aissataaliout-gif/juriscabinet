from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db import models
from .models import Dossier
from .forms import DossierForm
from messaging.models import Message

@login_required
def dossier_list(request):

    if request.user.role == "ADMIN":
        dossiers = Dossier.objects.all()

    elif request.user.role == "CLIENT":
        client = request.user.client_profile
        dossiers = Dossier.objects.filter(client=client)

    elif request.user.role == "LAWYER":
        dossiers = Dossier.objects.all()

    else:
        return HttpResponseForbidden("Accès refusé.")

    # Comptes par statut (calculés avant filtrage, pour les onglets)
    all_dossiers = dossiers
    counts = {
        "TOUS": all_dossiers.count(),
        "OUVERT": all_dossiers.filter(status="OUVERT").count(),
        "EN_COURS": all_dossiers.filter(status="EN_COURS").count(),
        "FERME": all_dossiers.filter(status="FERME").count(),
    }

    # Filtre par statut
    status = request.GET.get("status", "")
    if status in ["OUVERT", "EN_COURS", "FERME"]:
        dossiers = dossiers.filter(status=status)

    # Recherche par titre, client ou avocat
    q = request.GET.get("q", "").strip()
    if q:
        dossiers = dossiers.filter(
            models.Q(title__icontains=q) |
            models.Q(client__first_name__icontains=q) |
            models.Q(client__last_name__icontains=q) |
            models.Q(lawyer__first_name__icontains=q) |
            models.Q(lawyer__last_name__icontains=q)
        )

    return render(
        request,
        "dossiers/dossier_list.html",
        {
            "dossiers": dossiers,
            "counts": counts,
            "current_status": status,
            "q": q,
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

@login_required
def dossier_detail(request, pk):

    dossier = get_object_or_404(Dossier, pk=pk)

    if request.user.role == "CLIENT":
        if dossier.client != request.user.client_profile:
            return HttpResponseForbidden("Accès refusé à ce dossier.")

    documents = dossier.documents.all()
    appointments = dossier.appointments.order_by("appointment_date")
    dossier_messages = dossier.messages.order_by("sent_at")

    if request.method == "POST" and "content" in request.POST:
        content = request.POST.get("content", "").strip()

        if content:
            if request.user.role == "CLIENT":
                receiver = dossier.lawyer.user
            else:
                receiver = dossier.client.user

            if receiver:
                Message.objects.create(
                    sender=request.user,
                    receiver=receiver,
                    dossier=dossier,
                    subject=f"Dossier #{dossier.id}",
                    content=content,
                )
                messages.success(request, "Message envoyé.")
            else:
                messages.error(
                    request,
                    "Impossible d'envoyer : aucun compte utilisateur lié à ce contact."
                )

        return redirect("dossier_detail", pk=dossier.id)

    return render(
        request,
        "dossiers/dossier_detail.html",
        {
            "dossier": dossier,
            "documents": documents,
            "appointments": appointments,
            "dossier_messages": dossier_messages,
        }
    )
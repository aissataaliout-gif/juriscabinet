from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Appointment
from .forms import AppointmentForm
import json
from django.core.serializers.json import DjangoJSONEncoder


@login_required
def appointment_list(request):

    if request.user.role == "ADMIN":
        appointments = Appointment.objects.all()

    elif request.user.role == "CLIENT":
        client = request.user.client_profile

        appointments = Appointment.objects.filter(
            dossier__client=client
        )

    elif request.user.role == "LAWYER":
        # Pour l'instant, on conserve l'accès actuel de l'avocat.
        # Nous vérifierons son lien User ↔ Lawyer avant de filtrer
        # ses rendez-vous précisément.
        appointments = Appointment.objects.all()

    else:
        return HttpResponseForbidden("Accès refusé.")

    return render(
        request,
        "appointments/appointment_list.html",
        {
            "appointments": appointments
        },
    )


@login_required
def appointment_create(request):

    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à créer un rendez-vous."
        )

    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Le rendez-vous a été créé avec succès."
            )

            return redirect("appointment_list")

    else:
        form = AppointmentForm()

    return render(
        request,
        "appointments/appointment_form.html",
        {
            "form": form
        },
    )


@login_required
def appointment_update(request, pk):

    appointment = get_object_or_404(
        Appointment,
        pk=pk
    )

    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à modifier ce rendez-vous."
        )

    if request.method == "POST":
        form = AppointmentForm(
            request.POST,
            instance=appointment
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Le rendez-vous a été modifié avec succès."
            )

            return redirect("appointment_list")

    else:
        form = AppointmentForm(
            instance=appointment
        )

    return render(
        request,
        "appointments/appointment_form.html",
        {
            "form": form
        },
    )


@login_required
def appointment_delete(request, pk):

    appointment = get_object_or_404(
        Appointment,
        pk=pk
    )

    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à supprimer ce rendez-vous."
        )

    if request.method == "POST":
        appointment.delete()

        messages.success(
            request,
            "Le rendez-vous a été supprimé avec succès."
        )

        return redirect("appointment_list")

    return render(
        request,
        "appointments/appointment_confirm_delete.html",
        {
            "appointment": appointment
        },
    )

@login_required
def appointment_calendar(request):

    if request.user.role == "ADMIN":
        appointments = Appointment.objects.all()

    elif request.user.role == "CLIENT":
        client = request.user.client_profile
        appointments = Appointment.objects.filter(dossier__client=client)

    elif request.user.role == "LAWYER":
        appointments = Appointment.objects.all()

    else:
        return HttpResponseForbidden("Accès refusé.")

    events = []
    for a in appointments:
        events.append({
            "title": a.title,
            "start": a.appointment_date.isoformat(),
            "url": f"/appointments/{a.id}/modifier/",
        })

    events_json = json.dumps(events, cls=DjangoJSONEncoder)

    return render(
        request,
        "appointments/appointment_calendar.html",
        {
            "events_json": events_json,
        },
    )
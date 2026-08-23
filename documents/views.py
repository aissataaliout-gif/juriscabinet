from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Document
from .forms import DocumentForm


@login_required
def document_list(request):

    if request.user.role == "ADMIN":
        documents = Document.objects.all()

    elif request.user.role == "CLIENT":
        client = request.user.client_profile

        documents = Document.objects.filter(
            dossier__client=client
        )

    elif request.user.role == "LAWYER":
        documents = Document.objects.all()

    else:
        return HttpResponseForbidden("Accès refusé.")

    return render(
        request,
        "documents/document_list.html",
        {
            "documents": documents
        },
    )


@login_required
def document_create(request):

    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à ajouter un document."
        )

    if request.method == "POST":
        form = DocumentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Le document a été ajouté avec succès."
            )

            return redirect("document_list")

    else:
        form = DocumentForm()

    return render(
        request,
        "documents/document_form.html",
        {
            "form": form
        },
    )


@login_required
def document_update(request, pk):

    document = get_object_or_404(
        Document,
        pk=pk
    )

    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à modifier ce document."
        )

    if request.method == "POST":
        form = DocumentForm(
            request.POST,
            request.FILES,
            instance=document
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Le document a été modifié avec succès."
            )

            return redirect("document_list")

    else:
        form = DocumentForm(
            instance=document
        )

    return render(
        request,
        "documents/document_form.html",
        {
            "form": form
        },
    )


@login_required
def document_delete(request, pk):

    document = get_object_or_404(
        Document,
        pk=pk
    )

    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à supprimer ce document."
        )

    if request.method == "POST":
        document.delete()

        messages.success(
            request,
            "Le document a été supprimé avec succès."
        )

        return redirect("document_list")

    return render(
        request,
        "documents/document_confirm_delete.html",
        {
            "document": document
        },
    )
from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Invoice
from .forms import InvoiceForm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

from django.conf import settings

from reportlab.platypus import Image
from reportlab.lib.units import cm

@login_required
def invoice_list(request):

    if request.user.role == "ADMIN":
        invoices = Invoice.objects.all().order_by("-created_at")

    elif request.user.role == "CLIENT":
        client = request.user.client_profile

        invoices = Invoice.objects.filter(
            dossier__client=client
        ).order_by("-created_at")

    elif request.user.role == "LAWYER":
        # On conservera la gestion actuelle de l'avocat
        # jusqu'à vérification de son lien User ↔ Lawyer.
        invoices = Invoice.objects.all().order_by("-created_at")

    else:
        return HttpResponseForbidden("Accès refusé.")

    return render(
        request,
        "billing/invoice_list.html",
        {"invoices": invoices},
    )

@login_required
def invoice_create(request):

    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à créer une facture."
        )

    if request.method == "POST":
        form = InvoiceForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "La facture a été créée avec succès."
            )

            return redirect("invoice_list")

    else:
        form = InvoiceForm()

    return render(
        request,
        "billing/invoice_form.html",
        {"form": form},
    )

@login_required
def invoice_update(request, pk):

    invoice = get_object_or_404(
        Invoice,
        pk=pk
    )

    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à modifier cette facture."
        )

    if request.method == "POST":
        form = InvoiceForm(
            request.POST,
            instance=invoice
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "La facture a été modifiée avec succès."
            )

            return redirect("invoice_list")

    else:
        form = InvoiceForm(
            instance=invoice
        )

    return render(
        request,
        "billing/invoice_form.html",
        {"form": form},
    )
@login_required
def invoice_delete(request, pk):

    invoice = get_object_or_404(
        Invoice,
        pk=pk
    )

    if request.user.role not in ["ADMIN", "LAWYER"]:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à supprimer cette facture."
        )

    if request.method == "POST":
        invoice.delete()

        messages.success(
            request,
            "La facture a été supprimée avec succès."
        )

        return redirect("invoice_list")

    return render(
        request,
        "billing/invoice_confirm_delete.html",
        {"invoice": invoice},
    )
@login_required
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.user.role == "CLIENT":
            client = request.user.client_profile

            if invoice.dossier.client != client:
                return HttpResponseForbidden(
                "Vous n'êtes pas autorisé à consulter cette facture."
                )

    elif request.user.role not in ["ADMIN", "LAWYER"]:
            return HttpResponseForbidden("Accès refusé.")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="Facture_{invoice.id}.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER
    title.textColor = colors.HexColor("#0B1F4D")

    heading = styles["Heading2"]
    heading.textColor = colors.HexColor("#0B1F4D")

    normal = styles["BodyText"]

    elements = []

    logo_path = os.path.join(
    settings.BASE_DIR,
    "static",
    "images",
    "logo.png"
)

    if os.path.exists(logo_path):
        logo = Image(logo_path)
        logo.drawHeight = 3.5 * cm
        logo.drawWidth = 3.5 * cm
        elements.append(logo)

    elements.append(Spacer(1, 10))

    # ==========================
    # EN-TÊTE
    # ==========================

    elements.append(
        Paragraph(
            "<font size='24'><b>JurisCabinet</b></font>",
            title,
        )
    )

    elements.append(
        Paragraph(
            "<font color='#666666'>Gestion numérique des cabinets d'avocats</font>",
            normal,
        )
    )

    elements.append(
        Paragraph(
            "<font color='#666666'>Bamako - Mali</font>",
            normal,
        )
    )

    elements.append(
        Paragraph(
            "<font color='#666666'>contact@juriscabinet.com</font>",
            normal,
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "<b><font size='18'>FACTURE</font></b>",
            title,
        )
    )

    elements.append(
        Paragraph(
            f"<b>N° JC-{invoice.created_at.year}-{invoice.id:05d}</b>",
            heading,
        )
    )

    elements.append(
        Paragraph(
            f"Date : {invoice.created_at.strftime('%d/%m/%Y')}",
            normal,
        )
    )

    elements.append(Spacer(1, 20))

    # ==========================
    # TABLEAU
    # ==========================

    data = [

        ["Champ", "Valeur"],

        ["Numéro",
         f"JC-{invoice.created_at.year}-{invoice.id:05d}"],

        ["Dossier",
         str(invoice.dossier)],

        ["Montant",
         f"{invoice.amount} FCFA"],

        ["Statut",
         invoice.get_status_display()],

        ["Description",
         invoice.description],

    ]

    table = Table(
        data,
        colWidths=[150, 320],
    )

    table.setStyle(
        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#0B1F4D")),

            ("TEXTCOLOR", (0, 0), (-1, 0),
             colors.white),

            ("BACKGROUND", (0, 1), (0, -1),
             colors.HexColor("#F5F7FA")),

            ("GRID", (0, 0), (-1, -1),
             1, colors.HexColor("#CCCCCC")),

            ("FONTNAME", (0, 0), (-1, 0),
             "Helvetica-Bold"),

            ("FONTNAME", (0, 1), (0, -1),
             "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),

            ("TOPPADDING", (0, 1), (-1, -1), 8),

            ("BOTTOMPADDING", (0, 1), (-1, -1), 8),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ])
    )
    elements.append(table)
    elements.append(Spacer(1, 25))
    # ==========================
# TOTAL À PAYER
# ==========================

    total_table = Table(
    [
        ["TOTAL À PAYER"],
        [f"{invoice.amount} FCFA"],
    ],
    colWidths=[470],
)

    total_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1F4D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#0B1F4D")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#0B1F4D")),
    ])
)

    elements.append(total_table)

    elements.append(Spacer(1, 35))

# Signature

    elements.append(
    Paragraph(
        "<b>Signature du cabinet</b>",
        heading,
    )
)

    elements.append(
    Paragraph(
        "JurisCabinet",
        normal,
    )
)

    elements.append(Spacer(1, 25))

# Pied de page

    elements.append(
    Paragraph(
        "<font color='#777777'>"
        "Bamako - Mali<br/>"
        "contact@juriscabinet.com<br/>"
        "+223 XX XX XX XX"
        "</font>",
        normal,
    )
)

    doc.build(elements)

    return response
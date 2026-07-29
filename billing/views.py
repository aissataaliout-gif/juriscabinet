from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Invoice
from .forms import InvoiceForm


@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by("-created_at")

    return render(
        request,
        "billing/invoice_list.html",
        {"invoices": invoices},
    )
@login_required
def invoice_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "La facture a été créée avec succès.")
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
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)

        if form.is_valid():
            form.save()
            messages.success(request, "La facture a été modifiée avec succès.")
            return redirect("invoice_list")
    else:
        form = InvoiceForm(instance=invoice)

    return render(
        request,
        "billing/invoice_form.html",
        {"form": form},
    )
@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == "POST":
        invoice.delete()
        messages.success(request, "La facture a été supprimée avec succès.")
        return redirect("invoice_list")

    return render(
        request,
        "billing/invoice_confirm_delete.html",
        {"invoice": invoice},
    )
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lawyer
from .forms import LawyerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def lawyer_list(request):
    lawyers = Lawyer.objects.all()

    return render(request, "lawyers/lawyer_list.html", {
        "lawyers": lawyers
    })
def lawyer_create(request):
    if request.method == "POST":
        form = LawyerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "L'avocat a été ajouté avec succès.")
            return redirect("lawyer_list")
    else:
        form = LawyerForm()

    return render(request, "lawyers/lawyer_form.html", {
        "form": form
    })
def lawyer_update(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)

    if request.method == "POST":
        form = LawyerForm(request.POST, request.FILES, instance=lawyer)

        if form.is_valid():
            form.save()
            messages.success(request, "L'avocat a été modifié avec succès.")
            return redirect("lawyer_list")
    else:
        form = LawyerForm(instance=lawyer)

    return render(request, "lawyers/lawyer_form.html", {
        "form": form
    })
def lawyer_delete(request, pk):
    lawyer = get_object_or_404(Lawyer, pk=pk)

    if request.method == "POST":
        lawyer.delete()
        messages.success(request, "L'avocat a été modifié avec succès.")
        return redirect("lawyer_list")

    return render(request, "lawyers/lawyer_confirm_delete.html", {
        "lawyer": lawyer
    })
@login_required
def lawyer_dashboard(request):
    return render(
        request,
        "lawyers/lawyer_dashboard.html",
        {
            "lawyer": request.user,
        },
    )
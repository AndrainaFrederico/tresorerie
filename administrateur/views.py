from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tresorerie.decorators import role_required
from django.shortcuts import render, redirect
from tresorerie.models import Caisse
# Create your views here.

@role_required('admin')
def admin_dashboard_view(request):
    return render(request, 'admin/dashboard.html')  # Dashboard spécifique à l'admin

def ajouter_caisse(request):
    if request.method == "POST":
        type_caisse = request.POST.get("typecaisse")
        type_operation = request.POST.get("type")
        date = request.POST.get("date")
        motif = request.POST.get("motif")
        somme = float(request.POST.get("somme"))

        # Ajouter les données
        caisse = Caisse(
            type_caisse=type_caisse,
            type_operation=type_operation,
            date=date,
            motif=motif,
            somme=somme,
        )
        caisse.save()

        # Rediriger vers le tableau de bord après ajout
        return redirect("admin_dashboard")

    # Pré-remplissage pour typecaisse
    type_caisse = request.GET.get("typecaisse", "")
    return render(request, "admin/add_caisse.html", {"typecaisse": type_caisse})

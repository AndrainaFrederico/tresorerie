from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tresorerie.decorators import role_required
# Create your views here.

@role_required('admin')
def admin_dashboard_view(request):
    return render(request, 'admin/dashboard.html')  # Dashboard spécifique à l'admin

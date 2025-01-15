from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tresorerie.decorators import role_required
# Create your views here.

@role_required('utilisateur')
def user_dashboard_view(request):
    return render(request, 'utilisateur/dashboard.html')
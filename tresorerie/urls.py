from django.contrib import admin
from django.urls import path, include
from tresorerie.views import home_view, logout_view, login_view, confirm_code_view
from administrateur.views import admin_dashboard_view, ajouter_caisse
from utilisateur.views import user_dashboard_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Page login + signup
    path('login/', login_view, name='login'),
    path('confirm-code/', confirm_code_view, name='confirm_code'),  # <- 2FA par code
    path('dashboard/admin/', admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/', user_dashboard_view, name='user_dashboard'),
    path('logout/', logout_view, name='logout'),
    path('caisse/ajouter/', ajouter_caisse, name='ajouter_caisse'),
]

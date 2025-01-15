from django.contrib import admin
from django.urls import path, include
from tresorerie.views import home_view, logout_view
from administrateur.views import admin_dashboard_view
from utilisateur.views import user_dashboard_view
from .views import login_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('dashboard/admin/', admin_dashboard_view, name='admin_dashboard'),  # Dashboard admin
    path('dashboard/', user_dashboard_view, name='user_dashboard'),  # Dashboard utilisateur
    path('logout/', logout_view, name='logout'),
]

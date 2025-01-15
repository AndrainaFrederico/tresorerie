from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from tresorerie.models import CustomUser

def home_view(request):
    if request.method == 'POST':
        if 'login_form' in request.POST:
            return login_view(request)
        elif 'signup_form' in request.POST:
            return signup_view(request)
    return render(request, 'home.html')

def signup_view(request):
    if request.method=="POST":
        admin_im = request.POST['imAdmin']
        admin_password = request.POST['mdpAdmin']
        username = request.POST['nom']
        email = request.POST['mail']
        password = request.POST['mdp']
        password2 = request.POST['mdpverif']
        admin_user = authenticate(username=admin_im, password=admin_password)
        if admin_user is not None and admin_user.is_superuser:
            if password == password2:
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "Email déja utilisé")
                else:
                    user = CustomUser.objects.create_user(username=username,email=email, password=password)
                    user.save()
                    messages.success(request, 'Inscription réussie. Vous pouvez maintenant vous connecter.')
                    return redirect('home')
            else:
                messages.error(request, 'Les mots de passe ne correspondent pas.')
        else:
            messages.error(request, 'Authentification administrateur échouée.')
    return render(request, 'home.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('mail')
        password = request.POST.get('mdp')
        
        # Authentifier l'utilisateur avec email et mot de passe
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)  # Connecter l'utilisateur
            if user.is_superuser:
                # Si l'utilisateur est un admin (superuser), redirigez vers le dashboard admin
                messages.success(request, 'Connexion réussie en tant qu\'admin.')
                return redirect('admin_dashboard')  # Nom de la vue de dashboard admin
            else:
                # Si l'utilisateur est un utilisateur normal, redirigez vers son dashboard
                messages.success(request, 'Connexion réussie en tant qu\'utilisateur.')
                return redirect('user_dashboard')  # Nom de la vue de dashboard utilisateur
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')

    return render(request, 'home.html')  # Formulaire de connexion

def logout_view(request):
    logout(request)
    messages.success(request, "Déconnexion Réussi!")
    return redirect('home')
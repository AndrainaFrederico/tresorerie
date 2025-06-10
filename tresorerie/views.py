from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
import random

from .models import CustomUser, VerificationCode


def home_view(request):
    """
    Affiche la page d'accueil qui contient les formulaires de connexion et d'inscription.
    Selon le formulaire soumis, redirige vers la fonction login_view ou signup_view.
    """
    if request.method == 'POST':
        if 'login_form' in request.POST:
            return login_view(request)
        elif 'signup_form' in request.POST:
            return signup_view(request)
    return render(request, 'home.html')


def signup_view(request):
    """
    Gère l'inscription d'un nouvel utilisateur.
    Seul un administrateur peut inscrire un utilisateur (vérification par nom et mdp admin).
    Vérifie que les mots de passe correspondent et que l'email n'est pas déjà utilisé.
    """
    if request.method == "POST":
        admin_im = request.POST['imAdmin']          # Identifiant admin
        admin_password = request.POST['mdpAdmin']  # Mot de passe admin
        username = request.POST['nom']
        email = request.POST['mail']
        password = request.POST['mdp']
        password2 = request.POST['mdpverif']

        # Authentification administrateur
        admin_user = authenticate(username=admin_im, password=admin_password)

        if admin_user is not None and admin_user.is_superuser:
            if password == password2:
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "Email déja utilisé")
                else:
                    # Création du nouvel utilisateur
                    user = CustomUser.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'Inscription réussie. Vous pouvez maintenant vous connecter.')
                    return redirect('home')
            else:
                messages.error(request, 'Les mots de passe ne correspondent pas.')
        else:
            messages.error(request, 'Authentification administrateur échouée.')

    return render(request, 'home.html')


def send_verification_code(user):
    """
    Génère un code de vérification aléatoire à 6 chiffres.
    Sauvegarde ce code en base (table VerificationCode).
    Envoie le code par email à l'utilisateur.
    """
    code = str(random.randint(100000, 999999))
    VerificationCode.objects.create(user=user, code=code)

    send_mail(
        subject="Code de vérification 2FA",
        message=f"Bonjour {user.username},\n\nVotre code de vérification est : {code}. Ce code expire dans 5 minutes.",
        from_email="application_tresorerie@gmail.com",
        recipient_list=[user.email],
        fail_silently=False,
    )


def login_view(request):
    """
    Gère la connexion de l'utilisateur.
    Si les identifiants sont valides, connecte l'utilisateur et lui envoie un code 2FA.
    Redirige vers la page de confirmation du code.
    """
    if request.method == "POST":
        email = request.POST.get('mail')
        password = request.POST.get('mdp')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            send_verification_code(user)  # Envoi du code de vérification 2FA
            request.session['verified'] = False  # Marque l'utilisateur comme non vérifié pour l'accès sécurisé
            return redirect('confirm_code')
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')

    return render(request, 'home.html')


@login_required
def confirm_code_view(request):
    """
    Affiche le formulaire de saisie du code 2FA.
    Gère la validation du code et limite à 3 essais.
    Si code correct et valide => accès autorisé, sinon déconnexion après 3 essais.
    """
    if not request.user.is_authenticated:
        return redirect('home')

    # Initialiser le compteur d’essais dans la session s’il n’existe pas
    if 'attempts' not in request.session:
        request.session['attempts'] = 0

    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            # Récupérer le dernier code envoyé à l'utilisateur
            verification = VerificationCode.objects.filter(user=request.user).latest('created_at')

            # Vérifie si le code est expiré (méthode is_valid dans le modèle)
            if not verification.is_valid():
                messages.error(request, "Code expiré. Veuillez vous reconnecter.")
                logout(request)
                return redirect('home')

            # Vérifie si le code correspond
            if verification.code == code:
                request.session['verified'] = True  # Marque l'utilisateur comme vérifié
                request.session['attempts'] = 0     # Réinitialise les essais

                # Redirige vers le dashboard selon le type d'utilisateur
                if request.user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                # Code incorrect, incrémente les essais
                request.session['attempts'] += 1

                if request.session['attempts'] >= 3:
                    messages.error(request, "Trop de tentatives. Veuillez vous reconnecter.")
                    logout(request)  # Déconnexion forcée après 3 essais
                    return redirect('home')
                else:
                    messages.error(request, f"Code incorrect. Tentative {request.session['attempts']}/3.")

        except VerificationCode.DoesNotExist:
            # Pas de code trouvé en base => forcer la reconnexion
            messages.error(request, "Aucun code trouvé. Veuillez vous reconnecter.")
            logout(request)
            return redirect('home')

    return render(request, 'confirm_code.html')


def logout_view(request):
    """
    Déconnecte l'utilisateur et redirige vers la page d'accueil avec message.
    """
    logout(request)
    messages.success(request, "Déconnexion réussie !")
    return redirect('home')


@login_required
def user_dashboard(request):
    """
    Affiche le dashboard utilisateur uniquement si l'utilisateur est vérifié via 2FA.
    Sinon redirige vers la page de confirmation du code.
    """
    if not request.session.get('verified'):
        return redirect('confirm_code')
    return render(request, 'user_dashboard.html')


@login_required
def admin_dashboard(request):
    """
    Affiche le dashboard administrateur uniquement si l'utilisateur est vérifié via 2FA.
    Sinon redirige vers la page de confirmation du code.
    """
    if not request.session.get('verified'):
        return redirect('confirm_code')
    return render(request, 'admin_dashboard.html')

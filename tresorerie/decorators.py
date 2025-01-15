from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def role_required(role='utilisateur'):
    """
    Décorateur pour vérifier si l'utilisateur est connecté et rediriger
    selon son rôle.
    
    Paramètre:
    role -- Le rôle requis ('utilisateur' ou 'admin') (par défaut 'utilisateur').
    """
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if role == 'admin' and not request.user.is_superuser:
                return redirect('user_dashboard')  # Rediriger vers le dashboard utilisateur si ce n'est pas un admin
            if role == 'utilisateur' and request.user.is_superuser:
                return redirect('admin_dashboard')  # Rediriger vers le dashboard admin si c'est un admin
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator

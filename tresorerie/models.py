from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# ===================================================================
# MANAGER FOR CUSTOM USER (CORRECTED)
# ===================================================================
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        This method is now robust against duplicate username arguments.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)

        # ❗️ FIX: Remove any 'username' that might be passed in extra_fields
        # to avoid the "multiple values for keyword argument" error.
        extra_fields.pop('username', None)

        # We enforce that the username is always the email.
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # This correctly calls the fixed create_user method
        return self.create_user(email, password, **extra_fields)

# ===================================================================
# CUSTOM USER MODEL
# ===================================================================
class CustomUser(AbstractUser):
    # We remove the username field definition from here because AbstractUser already has one.
    # username = None # Optional: if you truly want to remove the username field
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No extra required fields besides email and password

    # Assign the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email


# ===================================================================
# CAISSE MODEL
# ===================================================================
class Caisse(models.Model):
    TYPE_CAISSE_CHOICES = [
        ('Grande Caisse', 'Grande Caisse'),
        ('Petite Caisse', 'Petite Caisse'),
    ]

    TYPE_OPERATION_CHOICES = [
        ('Entrée', 'Entrée'),
        ('Sortie', 'Sortie'),
    ]

    type_caisse = models.CharField(max_length=20, choices=TYPE_CAISSE_CHOICES)
    type_operation = models.CharField(max_length=10, choices=TYPE_OPERATION_CHOICES)
    date = models.DateField()
    motif = models.TextField()
    somme = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Note on total fields is below
    total_grande_caisse = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_petite_caisse = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # The save method has a logical flaw, see note below
    def save(self, *args, **kwargs):
      # Your existing save logic
      super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type_caisse} - {self.type_operation} - {self.somme}"
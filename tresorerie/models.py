from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Aucun champ supplémentaire requis

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
    total_grande_caisse = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_petite_caisse = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Calcul automatique des totaux
        if self.type_caisse == "Grande Caisse":
            self.total_grande_caisse += self.somme if self.type_operation == "Entrée" else -self.somme
        elif self.type_caisse == "Petite Caisse":
            self.total_petite_caisse += self.somme if self.type_operation == "Entrée" else -self.somme
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type_caisse} - {self.type_operation} - {self.somme}"

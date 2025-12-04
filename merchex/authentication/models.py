from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    # ajouté des tabs à partir d'ici pour faire rentrer le code dans la classe, erreur du cours ?
    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné'),
    )

    profile_photo = models.ImageField(verbose_name='Photo de profil')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
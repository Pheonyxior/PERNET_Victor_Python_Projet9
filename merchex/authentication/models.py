from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class User(AbstractUser):
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'
    # IMAGE_MAX_SIZE = (100, 200)

    # ajouté des tabs à partir d'ici pour faire rentrer le code dans la classe, erreur du cours ?
    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné'),
    )

    # profile_photo = models.ImageField(verbose_name='Photo de profil', null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')

    # follows = models.ManyToManyField(
    #     'self',
    #     limit_choices_to={'role': CREATOR},
    #     symmetrical=False,
    #     verbose_name='suit',
    #     blank=True,
    # )
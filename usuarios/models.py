from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Usuarios(AbstractUser):
    
    TIPOS_DE_USUARIO = [
        ('oferecer', 'Ofercer meus serviços'),
        ('contratar', 'Quero contratar um serviço'),
        ('hibrido', 'Quero contratar e oferecer meu serviço')
        ]
    nome_completo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPOS_DE_USUARIO, default='oferecer')
    
    def __str__(self):
        return self.username
    
    
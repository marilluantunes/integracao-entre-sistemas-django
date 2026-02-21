from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AlunoSistema2(models.Model):

    STATUS_CHOICE = [
        ('ativo' , 'Ativo'),
        ('inativo' , 'Inativo'),
        ('suspenso' , 'Suspenso'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100, verbose_name="Nome completo")
    email = models.EmailField(verbose_name="E-mail")
    matricula = models.CharField(max_length=10, unique = True, verbose_name='Matrícula' )
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Usuário sistema 2 - Moodle"
        verbose_name_plural = "Usuários do sistema 2 - Moodle"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.matricula}"

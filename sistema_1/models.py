from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AlunoSistema1(models.Model):

    STATUS_CHOICE = [ 
        ('ativo' , 'Ativo'),
        ('inativo' , 'Inativo'),
        ('pendente' , 'Pendente'),
    ]
    
    #user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100, verbose_name="Nome completo")
    email = models.EmailField(blank= True, verbose_name= "E-mail")
    cpf = models.CharField(max_length=11, verbose_name="CPF")
    matricula = models.CharField(max_length=10, unique=True, verbose_name="Matrícula")
    status = models.CharField(max_length=10, choices=STATUS_CHOICE,  default='ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criando em")

    class Meta:
        verbose_name = "Usuário do Sistema 1"
        verbose_name_plural = "Usuários do Sistema 1"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.matricula}"



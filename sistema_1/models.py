from django.db import models

# Create your models here.

class UsuarioSistema1(models.Model):

    STATUS_CHOICE = [ 
        ('ativo' , 'Ativo'),
        ('inativo' , 'Inativo'),
        ('pendente' , 'Pendente'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome completo")
    email = models.EmailField(unique=True, verbose_name= "E-mail")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    matricula = models.CharField(max_length=10, blank=True, null=True, verbose_name="Matrícula")
    status = models.CharField(max_length=10, choices=STATUS_CHOICE,  default='ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criando em")

    class Meta:
        verbose_name = "Usuário do Sistema 1"
        verbose_name_plural = "Usuários do Sistema 1"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.cpf}"



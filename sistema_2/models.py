from django.db import models

# Create your models here.

class UsuarioSistema2(models.Model):

    STATUS_CHOICE = [
        ('ativo' , 'Ativo'),
        ('inativo' , 'Inativo'),
        ('suspenso' , 'Suspenso'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome completo")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Usuário sistema 2 - Moodle"
        verbose_name_plural = "Usuários do sistema 2 - Moodle"
        ordering = ['nome']

        def __str__(self):
            return f"{self.nome} - {self.email}"

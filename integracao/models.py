from django.db import models
from sistema_1.models import AlunoSistema1
from sistema_2.models import AlunoSistema2

# Create your models here.

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    carga_horaria = models.IntegerField()

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

class Vinculacao(models.Model):
    aluno_sistema1 = models.OneToOneField(AlunoSistema1, on_delete=models.CASCADE, related_name='vinculo') # 1 - 1
    aluno_sistema2 = models.OneToOneField(AlunoSistema2, on_delete=models.CASCADE, related_name='vinculo' ) # 1 - 1
    data_vinculacao = models.DateTimeField(auto_now_add=True) 

    class Meta:
        verbose_name = 'Vinculação'
        verbose_name_plural = 'Vinculaçõess'

    def __str__(self):
        return f"{self.aluno_sistema1.nome} - {self.aluno_sistema2.nome}"   
    
class Nota(models.Model):
    aluno_sistema2 = models.ForeignKey(AlunoSistema2, on_delete=models.CASCADE, related_name='notas') # 1- N
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='notas') # 1 - N 
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    data_lancamento = models.DateTimeField(auto_now_add=True)
    enviada_para_sistema1 = models.BooleanField(default=False)
    data_envio = models.DateTimeField(null=True, blank=True)

    class Meta: 
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        ordering = ['-data_lancamento']

    def __str__(self):
        return f"{self.aluno_sistema2.nome} - {self.disciplina.nome}: {self.valor} "

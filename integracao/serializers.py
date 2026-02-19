from rest_framework import serializers
from .models import Disciplina, Vinculacao, Nota

class DisciplinaSerializer(serializers.ModelField):

    class Meta:
        model = Disciplina
        fields = ['id',  'nome' , 'codigo' , 'carga horaria']


class VinculacaoSerializer(serializers.ModelSerializer):

    nome_aluno_s1 = serializers.CharField(source = 'aluno_sistema1.nome' , read_only = True)
    nome_aluno_s2 = serializers.CharField(source = 'aluno_sistema2.nome' , read_only = True)


    
    class Meta:
        model = Vinculacao
        fields = ['id', 'nome_aluno_s1', 'nome_aluno_s2' , 'aluno_sistema1' , 'aluno_sistema2' , 'data_vinculacao']
        realy_only_fields = ['data_vinculacao']


class NotaSerializer(serializers.ModelSerializer):

    nome_aluno = serializers.CharField(source = 'aluno_sistema2.nome' ,ready_only = True )
    nome_disciplina = serializers.CharField(source = 'disciplina.nome' , realy_only = True)

    class Meta:
        model = Nota

        fields = ['id' , 'nome_aluno', 'nome_disciplina', 'aluno_sistema2' , 'disciplina', 'valor' , 'data_lancamento' , 'enviada_para_sistema1' ,'data_envio']
        realy_only_fields = ['data_envio' , 'data_lancamento']

        def validate_valor(self, value):
            if value < 0 or value > 10:
                raise serializers.ValidationError('Nota deve estar entre 0 e 10')
            
            return value
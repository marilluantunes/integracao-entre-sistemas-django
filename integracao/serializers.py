from rest_framework import serializers
from .models import Disciplina, Vinculacao, Nota
from sistema_1.models import AlunoSistema1
from sistema_2.models import AlunoSistema2
import re


class SolicitacaoAcessoSerializer(serializers.Serializer):
    #aluno fornece dados para a verificacao

    nome = serializers.CharField(max_length = 100)
    email = serializers.EmailField()
    cpf = serializers.CharField(max_length = 14)

    def validate_cpf(self, value):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("CPF deve conter 11 números")
        return value
    
    def validate(self, data): 
        cpf_guarda = data['cpf']
        try:

            #verifica se aluno existe no sistema 1
            aluno_suap = AlunoSistema1.objects.get(cpf=cpf_guarda)

        except AlunoSistema1.DoesNotExist:
            raise serializers.ValidationError("CPF nao encontrado no Sistema 1")

        #verifica se ja possui cadastro no moodle

        if AlunoSistema2.objects.filter(matricula=aluno_suap.matricula).exists():
            raise serializers.ValidationError('Este CPF ja possu cadastro no moodle')
            
        #guarda o objeto do sistema 1 para usar depois
        data['aluno_suap'] = aluno_suap  #aluno_suap nao veio da requisisao , veio do banco de dados
        return data 

 #------------------------------------------------------------------------------------------------------       

class CriarSenhaSerializer(serializers.Serializer):

    #aluno cria sua senha para entrar no moodle 

    cpf = serializers.CharField(max_length=14)
    senha = serializers.CharField()
    confirmar_senha = serializers.CharField()

    def validate(self, data):
        if data['senha'] != data['confirmar_senha']:
            raise serializers.ValidationError('As senhas nao sao iguais')
        
        return data

#---------------------------------------------------------------------------------------------------------

class LoginSerializer(serializers.Serializer):

    cpf = serializers.CharField(max_length=14)
    senha = serializers.CharField()


    def validate_cpf(self, value):
        if not value.isdigit() or len(value) != 11:
            raise NotaSerializer.ValidationError("CPF inválido, digite apenas números")
        return value



class DisciplinaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disciplina
        fields = ['id',  'nome' , 'codigo' , 'carga_horaria']


class VinculacaoSerializer(serializers.ModelSerializer):

    nome_aluno_s1 = serializers.CharField(source = 'aluno_sistema1.nome' , read_only = True)
    matricula_aluno_s1 = serializers.CharField(source='aluno_sistema1.matricula' , read_only = True)
    nome_aluno_s2 = serializers.CharField(source = 'aluno_sistema2.nome' , read_only = True)
    matricula_aluno_s2 = serializers.CharField(source = 'aluno_sistema2.matricula' , read_only = True)

    class Meta:
        model = Vinculacao
        fields = ['id', 'nome_aluno_s1', 'matricula_aluno_s1' , 'nome_aluno_s2' , 'matricula_aluno_s2' , 'aluno_sistema1' , 'aluno_sistema2' , 'data_vinculacao']
        read_only_fields = ['data_vinculacao']

class NotaSerializer(serializers.ModelSerializer):

    nome_aluno = serializers.CharField(source = 'aluno_sistema2.nome' ,read_only = True )
    nome_disciplina = serializers.CharField(source = 'disciplina.nome' , read_only = True)

    class Meta:
        model = Nota

        fields = ['id' , 'nome_aluno', 'nome_disciplina', 'aluno_sistema2' , 'disciplina', 'valor' , 'data_lancamento' , 'enviada_para_sistema1' ,'data_envio']
        read_only_fields = ['data_envio' , 'data_lancamento']

        def validate_valor(self, value):
            if value < 0 or value > 10:
                raise serializers.ValidationError('Nota deve estar entre 0 e 10')
            
            return value
        


class BoletimSerializer(serializers.Serializer):
    aluno = serializers.SerializerMethodField()
    disciplinas = serializers.SerializerMethodField()

    def get_aluno(self, obj):
        return {
        #    'id': obj.id,
            'nome': obj.nome,
            'matricula': obj.matricula, 
            'email': obj.email,
            'status': obj.status
        }
    
    def get_disciplinas(self, obj):
        notas = obj.notas.all().select_related('disciplina') # ja carrega os dados da disciplina JUNTO com a nota
        disciplinas_dict = {}

        for nota in notas:
            disc_id = nota.disciplina.id
            if disc_id not in disciplinas_dict:
                disciplinas_dict[disc_id] = {
                    'id': disc_id,
                    'nome': nota.disciplina.nome,
                    'codigo': nota.disciplina.codigo,
                    'notas': [],
                }
        
            disciplinas_dict[disc_id]['notas'].append(float(nota.valor))

        # calcular a mdia
        for disc in disciplinas_dict.values():
            disc['media'] = sum(disc['notas']) / len(disc['notas']) if disc['notas'] else 0

        return {
            'Lista Da Disciplinas': list(disciplinas_dict.values()), #pega so os valores , sem as chaves
            'total de disicplinas': len(disciplinas_dict)
        }
    



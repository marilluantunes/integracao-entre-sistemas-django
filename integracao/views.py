from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.reverse import reverse
from sistema_1.models import AlunoSistema1
from sistema_2.models import AlunoSistema2
from .models import Vinculacao, Nota, Disciplina
from .serializers import ( VinculacaoSerializer,  NotaSerializer, DisciplinaSerializer, SolicitacaoAcessoSerializer,  CriarSenhaSerializer, LoginSerializer, BoletimSerializer)
from .permissions import PermissaoBase, PermissaoProfessor

# Create your views here.

# primeira etapa , verificar se cpf existe no sistema 1

class VerificarCpfView(generics.GenericAPIView):
    

    serializer_class = SolicitacaoAcessoSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def get(self, request):
        return Response(self.get_serializer().data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'erro': serializer.errors}, status=400)
        
        dados = serializer.validated_data #dados validados pelo serializer

        #salvando dados na sessao do usuario especifico , pode ser usado em outras classes, outras views,  outras requisicoes
        request.session['cpf'] = dados['cpf']
        request.session['email'] = dados['email']
        request.session['nome'] = dados['nome']
        request.session['aluno_suap_id'] = dados['aluno_suap'].id

        criar_senha_url = reverse('criar-senha', request=request) #gera o link para criar a senha 

        return Response({
            'sucesso': True,
            'mensagem': 'CPF verificado! Agora crie uma senha.',
            'matricula': dados['aluno_suap'].matricula,
            'nome': dados['aluno_suap'].nome,
            'proximo_passo': {
            'acao' : 'Crie uma senha para finalizar o cadastro no Moodle , clique no link abaixo',
            'url': criar_senha_url 
            },
        }
        )
    def get_view_name(self):
        return "Solicitar Acesso ao Moodle"


class CriarSenhaView(generics.GenericAPIView):

    serializer_class = CriarSenhaSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def get(self, request):
        serializer = self.get_serializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
       #serializer = CriarSenhaSerializer(data=request.data)
        
        # valida os dados
        if not serializer.is_valid():
            return Response(
                {'Erro': serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        dados = serializer.validated_data #usa os dados ja validados, nao pegos do request
        
        # pega os dados da sessão da view de verificar o cpf
        cpf_sessao = request.session.get('cpf')
        email_sessao = request.session.get('email')
        aluno_suap_id = request.session.get('aluno_suap_id')

        # verifica se sessão é válida
        if not all([cpf_sessao, email_sessao, aluno_suap_id]):
            return Response(
                {'erro': 'Sessão expirada. Faça a verificação do CPF novamente.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # verifica se é o mesmo CPF
        if cpf_sessao != dados['cpf']:
            return Response(
                {'erro': 'CPF não corresponde ao validado na verificação.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # busca aluno no SUAP
            aluno_suap = AlunoSistema1.objects.get(id=aluno_suap_id)

            # atualiza email no SUAP 
            email_atualizado = False
            if not aluno_suap.email:
                aluno_suap.email = email_sessao
                aluno_suap.save()
                email_atualizado = True

            # cria usuario no Django
            user = User.objects.create_user(
                username=aluno_suap.matricula,
                email=email_sessao,
                password=dados['senha'],
                first_name=aluno_suap.nome.split()[0],
            )

            # Adiciona ao grupo Alunos
            grupo_alunos, _ = Group.objects.get_or_create(name='Alunos')
            user.groups.add(grupo_alunos)

            # cria aluno no Moodle
            aluno_moodle = AlunoSistema2.objects.create(
                user=user,
                nome=aluno_suap.nome,
                email=email_sessao,
                matricula=aluno_suap.matricula,
                cpf=aluno_suap.cpf,
                status='ativo'
            )

            # cria vinculação
            Vinculacao.objects.create(
                aluno_sistema1=aluno_suap,
                aluno_sistema2=aluno_moodle
            )

            # limpa sessão
            request.session.flush()

            login_moodle_url = reverse('login-moodle' , request=request)

            return Response({
                'sucesso': True,
                'mensagem': 'Cadastro realizado com sucesso!',
                'email_utilizado': email_sessao,
               # 'email_suap_atualizado': email_atualizado,
               'Proximo Passo' : {
                   'acao' : 'Faça login no Moodle!! , clique no link',
                   'url' : login_moodle_url
               },
                'grupo': 'Aluno'
            }, status=status.HTTP_201_CREATED)
        
        except AlunoSistema1.DoesNotExist:
            return Response(
                {'erro': 'Aluno não encontrado no sistema 1 (SUAP)'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'erro': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    renderer_classes = [BrowsableAPIRenderer , JSONRenderer] 

    def get(self, request):
        serializer = self.get_serializer()
        return Response(serializer.data)
    

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'erro' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        
        dados = serializer.validated_data
        
        cpf = dados['cpf']
        senha = dados['senha']

        try: 
            # tenta buscar aluno no sistema 2 com o mesmo cpf
            aluno = AlunoSistema2.objects.get(cpf=cpf)

            #verififcacao de cpf e senha 
            user = authenticate(username=aluno.matricula  , password= senha)

            if user:
                boletim_url = reverse('boletim', args=[aluno.id], request=request)            

                return Response({
                    'sucesso': True,
                    'mensagem': 'Login realizado com sucesso!',
                    'aluno': {
                        'id': aluno.id,
                        'nome': aluno.nome,
                        'matricula': aluno.matricula,
                        'email': aluno.email,
                        'status': aluno.status
                    },
                    'links': {
                        'boletim': boletim_url
                    }
                })

            return Response({
                'erro' : 'cpf oy senha inválidos'
            } , status = status.HTTP_404_NOT_FOUND)
        
        except AlunoSistema2.DoesNotExist:
            return Response(
                {'erro' : 'Aluno nao cadastrado'} , status= status.HTTP_404_NOT_FOUND
            )

class VinculacaoViewSet(viewsets.ModelViewSet):
    #crud de vinculacoes

    queryset = Vinculacao.objects.all().order_by('-data_vinculacao')
    serializer_class = VinculacaoSerializer
    permission_classes = [PermissaoBase]

class NotaViewSet(viewsets.ModelViewSet):
    # crud de notas - professores

    queryset = Nota.objects.all().order_by('-data_lancamento')
    serializer_class = NotaSerializer
    permission_classes = [PermissaoProfessor]

class DisciplinaViewSet(viewsets.ModelViewSet):
    #crud de disciplinas

    queryset = Disciplina.objects.all().order_by('nome')
    serializer_class = DisciplinaSerializer
    permission_classes = [PermissaoBase]


class BoletimView(generics.GenericAPIView):
    serializer_class = BoletimSerializer
    queryset = AlunoSistema2.objects.all()
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]

    def get(self, request, pk):
        aluno = self.get_object()
        serializer = self.get_serializer(aluno)
        return Response(serializer.data)





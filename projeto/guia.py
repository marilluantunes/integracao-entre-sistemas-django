from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def guia_api(request, format=None):

    base_url = request.build_absolute_uri('/')[:-1]

    return Response({
        "GUIA DE USO DA API": {
            "descricao": "Esta API integra dois sistemas acadêmicos (SUAP e Moodle). "
                         "Abaixo está o fluxo recomendado de utilização e os endpoints disponíveis.",
            "documentacao_tecnica": f"{base_url}/api/docs/",
            "area_admin": f"{base_url}/admin/",
            "observacao": "Para detalhes técnicos completos dos endpoints, consulte a documentação gerada automaticamente.",

        },

        "INFORMACOES GERAIS": {
            "status": "EM DESENVOLVIMENTO",
            "aviso": "API incompleta - Funcionalidades estão sendo implementadas gradualmente",
            "ultima_atualizacao": "Fevereiro/2026",
            "progresso_geral": "Aproximadamente 60% concluído"
        },

        "SOBRE AS VINCULACOES": {
            "descricao": "Vinculação entre alunos do SUAP (Sistema 1) e do Moodle (Sistema 2)",
            "quando_ocorre": "A vinculação é realizada AUTOMATICAMENTE durante o fluxo de cadastro do aluno (etapa de criação de senha).",
            "endpoint_manual": f"{base_url}/api/vinculacoes/",
            "uso_endpoint_manual": "Este endpoint existe apenas para consulta ou correções manuais. Para o fluxo normal, a vinculação acontece automaticamente.",
            "observacao": "O sistema mantém um relacionamento OneToOne, garantindo que cada aluno do SUAP esteja vinculado a um único aluno do Moodle."
        },

             "COMO FUNCIONA O SISTEMA": {
            "etapa_1": "Um funcionário cadastra o aluno no SUAP.",
            "etapa_2": "O aluno solicita acesso ao Moodle utilizando seu CPF.",
            "etapa_3": "Após validação, o aluno cria sua senha.",
            "etapa_4": "O aluno realiza login para acessar o sistema.",
            "etapa_5": "Professores podem lançar notas.",
            "etapa_6": "Alunos podem consultar suas informações acadêmicas."
        },


        "PERFIS DE ACESSO": {
    "funcionario": {
        "descricao": "Gerencia o sistema acadêmico. Pode cadastrar alunos no SUAP, disciplinas e realizar vinculações.",
        "observacao": "Cadastro de professores ainda não implementado.",
        "endpoints": {
            "cadastrar_aluno_suap": f"{base_url}/api/sistema-1/",
            "cadastrar_disciplina": f"{base_url}/api/disciplinas/",
            "vinculacoes": f"{base_url}/api/vinculacoes/"
        }
    },
    "professor": {
        "descricao": "Pode lançar e visualizar notas.",
        "permissao": "Acesso restrito ao endpoint de notas.",
        "endpoints": {
            "lancar_nota": f"{base_url}/api/notas/",
        }
    },
    "superusuario": {
        "descricao": "Acesso administrativo completo.",
        "permissao": "Pode lançar notas, visualizar registros e acessar todas as áreas do sistema.",
        "endpoints": {
            "area_funcionario": f"{base_url}/api/sistema-1/",
            "notas": f"{base_url}/api/notas/",
            "vinculacoes": f"{base_url}/api/vinculacoes/"
        }
    },
    "aluno": {
        "descricao": "Pode solicitar acesso, criar senha, realizar login e consultar informações acadêmicas.",
        "endpoints": {
            "solicitar_acesso": f"{base_url}/api/solicitar-acesso-moodle/",
            "criar_senha": f"{base_url}/api/criar-senha/",
            "login": f"{base_url}/api/login-moodle/",
            "boletim": f"{base_url}/api/boletim/<id>/"
        }
    }
},

    })
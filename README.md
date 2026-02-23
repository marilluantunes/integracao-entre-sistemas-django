# Integração SUAP-Moodle

**Desenvolvido por:** Maria Luiza Antunes  

API REST para integração entre sistema acadêmico SUAP e plataforma Moodle.

## 
## Sobre

Funcionários cadastram alunos no SUAP, que então passam por um fluxo de autoatendimento para acessar o Moodle. A vinculação entre os sistemas é automática. Professores lançam notas, e alunos consultam seu boletim.


## Sistema de Grupos e Permissões

O projeto utiliza o sistema de **grupos do Django** para gerenciar permissões de acesso.

###  Grupos disponíveis

| Grupo | Permissões | Criado por |
|-------|------------|------------|
| **Alunos** | Acesso ao próprio boletim e dados pessoais | ✅ Automático (via fluxo da API) |
| **Professores** | Lançar e visualizar notas | ⚠️ Manual (admin/shell) |
| **Funcionarios** | CRUD de alunos, disciplinas e vinculações | ⚠️ Manual (admin/shell) |
| **Superusuário** | Acesso total ao sistema | `createsuperuser` |

### Fase: Em desenvolvimento
 Funcionalidades novas estão planejadas para versões futuras


 ##  Criando um Superusuário

**⚠️ Nota:** Por enquanto, o cadastro de usuários com permissões (funcionários e professores) precisa ser feito manualmente via admin ou shell. Futuramente isso será automatizado.

### 1. Crie um superusuário
```bash
# No terminal, dentro da pasta do projeto
python manage.py createsuperuser
```

## Tecnologias

- Django 6.0
- Django REST Framework 3.16
- drf-spectacular (documentação)

##  Instalação Rápida

```bash
# Clone
git clone https://github.com/marilluantunes/integracao-entre-sistemas-django.git
cd integracao-entre-sistemas-django


# Ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Dependências
pip install -r requirements.txt

# Migrações e servidor
python manage.py migrate
python manage.py runserver
```

## 📚 Documentação e Guia

Acesse os seguintes endpoints após iniciar o servidor:

| URL | Descrição |
|-----|-----------|
| **http://127.0.0.1:8000/api/** | 📘 **Guia de uso da API** (recomendado para começar) |
| **http://127.0.0.1:8000/api/docs/** | 🔵 Documentação Swagger interativa |
| **http://127.0.0.1:8000/admin/** | ⚙️ Admin Django |

O **guia da API** (`/api/`) contém instruções passo a passo e explicações detalhadas de como utilizar todos os endpoints.

##  Perfis

- **Funcionário**: Cadastra alunos e disciplinas
- **Professor**: Lança notas
- **Aluno**: Cria senha, faz login e consulta boletim


📌 **Consulte o guia em `/api/` para instruções detalhadas de uso.**

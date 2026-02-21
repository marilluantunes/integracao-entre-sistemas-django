from django.shortcuts import render
from .models import AlunoSistema1
from .serializers import AlunoSistema1Serializer
from rest_framework import viewsets, permissions
from integracao.permissions import PermissaoBase, PermissaoProfessor


# Create your views here.

class AlunoSistema1ViewSet(viewsets.ModelViewSet):

    queryset = AlunoSistema1.objects.all().order_by('nome')
    serializer_class = AlunoSistema1Serializer
    permission_classes = [PermissaoBase]

    def get_view_name(self):
        return "Cadastros no SUAP"



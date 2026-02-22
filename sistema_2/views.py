from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import AlunoSistema2
from .serializers import AlunoSistma2Serializers
from integracao.permissions import PermissaoBase, PermissaoProfessor

# Create your views here.

class AlunoMoodleViewSet(viewsets.ModelViewSet):
    queryset = AlunoSistema2.objects.all().order_by('nome')
    serializer_class = AlunoSistma2Serializers
    permission_classes = [PermissaoProfessor]

    def get_view_name(self):
        return "Usuários do Moodle"
    



    


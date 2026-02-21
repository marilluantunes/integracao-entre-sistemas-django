from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AlunoSistema1

class AlunoSistema1Serializer(serializers.ModelSerializer):
    class Meta:
        model =  AlunoSistema1
        fields = ['id'  , 'nome' , 'cpf', 'matricula', 'status','created_at']
        realy_only_fields = ['created_at']

    def validate_cpf(self,value):
        if len(value) != 11:
            raise serializers.ValidationError('CPF deve conter 11 dígitos')
        if not value.isdigit():
            raise serializers.ValidationError('CPF deve conter apenas números')
        
        return value
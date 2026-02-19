from rest_framework import serializers
from .models import AlunoSistema2


class AlunoSistma2Serializers(serializers.ModelSerializer):
    class Meta:
        model = AlunoSistema2
        fields =['id' , 'user' , 'nome' , 'email' , 'status', 'created_at']
        realy_only_fields = ['created_at']
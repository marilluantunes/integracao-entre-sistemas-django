from rest_framework import permissions  as p

class PemissaoBase(p.BasePermission):
   
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        
        # se a requisicao for um metodo de leitura entao permite qualquer autenticado
        if request.method in  p.SAFE_METHODS:
            return True

        #caso nao seja metodo de leitura, só permite funcionários ou superusers - metodo de escrita
        return user.is_superuser or user.groups.filter(name='Funcionários').exists()
    

class PermissaoProfessor(p.BasePermission):
    # so professor pode lancar nota

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        
        # suoeruser ou professor
        return request.user.is_superuser or request.user.groups.filter(name='Professores').exists()
        
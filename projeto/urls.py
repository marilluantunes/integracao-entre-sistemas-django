from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from integracao import views  as integracao_views
from sistema_1 import views as sistema1_views
from sistema_2 import views as sistema2_views



router = DefaultRouter()
router.register(r'vinculacoes' , integracao_views.VinculacaoViewSet)
router.register(r'notas' , integracao_views.NotaViewSet)
router.register(r'disciplinas' , integracao_views.DisciplinaViewSet)
#suap
router.register(r'sistema 1' , sistema1_views.AlunoSistema1ViewSet)
#moodle
router.register(r'sistema 2' , sistema2_views.AlunoMoodleViewSet)


#sistema 1 (suap)
#router_sistema1 = DefaultRouter()
#router_sistema1.register(r'alunos' , sistema1_views.AlunoSistema1ViewSet)





urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

   # path('api/sistema1/', include(router_sistema1.urls)),

     #generics
    path('api/solicitar-acesso-moodle/', integracao_views.VerificarCpfView.as_view()),
    path('api/criar-senha/', integracao_views.CriarSenhaView.as_view()),
    path('api/login-moodle/', integracao_views.LoginView.as_view()),

    path('api-auth/', include('rest_framework.urls')),
]

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from integracao import views as integracao_views
from sistema_1 import views as sistema1_views
from sistema_2 import views as sistema2_views
from . import guia
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.views.generic import RedirectView


router = DefaultRouter()
router.register(r'vinculacoes', integracao_views.VinculacaoViewSet)
router.register(r'notas', integracao_views.NotaViewSet)
router.register(r'disciplinas', integracao_views.DisciplinaViewSet)
router.register(r'sistema-1', sistema1_views.AlunoSistema1ViewSet)
router.register(r'sistema-2', sistema2_views.AlunoMoodleViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', RedirectView.as_view(url='api/docs', permanent=False)),
    
    path('api/',  guia.guia_api, name='api-docs'),
    
    #path('api/', include(router.urls)),
    

    path('api/solicitar-acesso-moodle/', 
         integracao_views.VerificarCpfView.as_view(), name='verificar-cpf'),
    
    path('api/criar-senha/', 
         integracao_views.CriarSenhaView.as_view(), name='criar-senha'),
    
    path('api/login-moodle/', 
         integracao_views.LoginView.as_view(),  name='login-moodle'),
    
    path('api/boletim/<int:pk>/', 
         integracao_views.BoletimView.as_view(),  name='boletim'),
    
    path('api-auth/', include('rest_framework.urls')),

    #documentacao

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
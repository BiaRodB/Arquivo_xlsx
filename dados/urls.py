from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from dados.views import ClientesViewSet, FiltroViewSet
from dados import views

router = routers.DefaultRouter()
router.register('Dados_Clientes_Geral', ClientesViewSet,'Dados ')
router.register('mulheres_de_Meeren', FiltroViewSet,'Mulheres')


urlpatterns = [
    path('', views.cadastrar, name='Cadastro'),
    path('cadastrodados',include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Consumir_arquivo_xlsx
Esse Sistema em Django ira consumir arquivos no formato xlsx, colocando planilhas no banco de dados pelo sistema.

## Preparando o ambiente
Instale o python;
Instale um IDE - editor de código (vs code, pycharm, etc)
Você pode criar uma pasta normalmente: clicando no botão direito do mause e em seguida clicar em novo e pasta.
Porém você também pode criar pelo terminal usando o seguinte codigo:
```python
mkdir Arquivo
```
Após isso, digite:
```python
cd cliente_api
```
Criando ambiente virtual para os pacotes do projeto
Essa parte pode ser criado dentro do terminal/ cmd do IDE
Linux:
```python
virtualenv venv
. venv/bin/activate
```
Windows:
```python
pip install virtualenv
python -m venv env
env\Scripts\activate
```
Instalando o Django e e Django REST framework no ambiente virtual:
```python
pip install django
pip install djangorestframework
pip install markdown       
pip install django-filter  
pip install pandas
pip install openpyxl
```
Criando o projeto e a aplicação:
```python
django-admin startproject core .  
django-admin startapp dados
```
Configurando o settings.py: 
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'dados',
    'django_filters',
    
]
```
Ainda no settings.py mudaremos o idioma para português:
```python
LANGUAGE_CODE = 'pt-br'
```
No arquivo dados/models.py definimos todos os objetos chamados Modelos, tem que apagar tudo dele e escrever o seguinte código:
```python
from django.db import models

class Inserir(models.Model):
    SEXO = (
    ('F', 'F'),
    ('M', 'M'))

    nome = models.CharField('Nome:',max_length=100,null=True)
    sobrenome = models.CharField('Sobrenome:',max_length=150, blank=True,null=True)
    sexo = models.CharField(max_length=1, choices=SEXO, blank=False, null=False, default='M')
    altura = models.CharField(max_length=20,null=True)
    peso = models.CharField(max_length=20,null=True)
    nascimento= models.DateField(null=True)
    bairro = models.CharField(max_length=150,null=True)
    cidade = models.CharField(max_length=200,null=True)
    estado = models.CharField(max_length=200,null=True)
    numero = models.CharField('nome',max_length=30,null=True)

    def __str__(self):
        return self.nome
    objects = models.Manager()

```
Em seguida usaremos o comando makemigrations, pois ele analisa se foram feitas mudanças nos modelos e, em caso positivo, cria novas migrações ( Migrations ) para alterar a estrutura do seu banco de dados, refletindo as alterações feitas:
```python
python manage.py makemigrations dados
```
```python
python manage.py migrate dados
```
```python
python manage.py migrate 
```
Criar um administrador/ superusuario:
```python
python manage.py createsuperuser
```
"Usuário (leave blank to use 'usuario'):

Endereço de email:

Password:

Password (again):

Superuser created successfully."

Vamos abrir dados/admin.py no editor de código, apagar tudo dele e escrever o seguinte código:
````python
from django.contrib import admin
from dados.models import Inserir

class dado(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('sexo',)
    list_per_page = 25
    ordering = ('nome',)


admin.site.register(Inserir, dado)
````
vamos criar um arquivo dentro do app chamado serializers.py e adicionar os seguintes códigos:
````python
from rest_framework import serializers
from dados.models import Inserir
import pandas as pd


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inserir
        fields = '__all__'
````
Vamos abrir dados/views.py no editor de código, apagar tudo dele e escrever o seguinte código:
````python
from dados.Serializers import ClienteSerializer
from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework import viewsets
from dados.models import  Inserir
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
import pandas as pd
from http.client import HTTPResponse
from django.shortcuts import render
import os
from django.core.files.storage import FileSystemStorage
from datetime import datetime


 
class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Inserir.objects.all()
    classe = ClienteSerializer
    filtros = [DjangoFilterBackend, filters.OrderingFilter]
    ordem = ['nascimento'] 


class FiltroViewSet(viewsets.ModelViewSet):
    queryset = Inserir.objects.filter(cidade='Meeren',sexo='F')
    classe = ClienteSerializer
    filtros = [DjangoFilterBackend, filters.OrderingFilter]
    ordem = ['nascimento'] 
  

def cadastrar(request):
        if request.method == 'POST' and request.FILES['myfile']:      
            myfile = request.FILES['myfile']
            arquivo = FileSystemStorage()
            nome_arquivo = arquivo.save(myfile.name, myfile)
            upload = arquivo.url(nome_arquivo) 
            cwd = os.getcwd()             
            exceldata = pd.read_excel(f'{cwd}/media_root/{myfile}',engine="openpyxl")        
            frame = exceldata
            for frame in frame.itertuples():
                objeto = Inserir.objects.create( id=frame.id, nome=frame.nome, sobrenome=frame.sobrenome,sexo=frame.sexo, 
                altura=frame.altura, peso=frame.peso, nascimento=datetime.fromtimestamp(frame.nascimento), 
                bairro=frame.bairro,cidade=frame.cidade,estado=frame.estado,numero=frame.numero)           
            objeto.save()
            return render(request, 'index.html', {
                'upload': upload
            })
         
        return render(request,'index.html',{})
````
Vamos editar core/urls.py no editor de código:
````python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from dados.views import ClientesViewSet
from dados import views

router = routers.DefaultRouter()
router.register('Dados_Clientes', ClientesViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dados.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
````
Vamos criar um aquivo chamado urls.py dentro da pasta/app dados, aqura vamos editar dados/urls.py no editor de código:
````python
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
````
Vamos startar o servidor web:
```python
python manage.py runserver
```
Dentro da pasta dados criaremos uma pasta chemada templates. dentro de templates criaremos o arquivo index.html.
Colocaremos o seguinte código:
````python
{% load static %}

{% block content %}



<!DOCTYPE html>
<html lang="en">
  <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
  <link rel="stylesheet" href="{% static 'navbar-top-fixed.css' %}">
  <link rel="stylesheet" href="{% static 'https://fonts.googleapis.com/css?family=Heebo:400,700|Oxygen:700' %}"> 
  <link rel="stylesheet" href="{% static 'dist/css/style.css' %}">

  <nav class="navbar navbar-expand-lg bg-body-tertiary btn-success">
    <div class="container-fluid">
      <a class="navbar-brand btn-success" href="http://127.0.0.1:8000/cadastr">API_REST</a>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
      
      </div>
    </div>
  </nav>




 <center>
  <form method="POST" enctype="multipart/form-data">
    <br><br><br><br>
    {% csrf_token %}

    <div class="">
        <div class="col-md-7 col-xs-10">
          
          <div class="x_panel">
            <div class="x_title">
              <h2>Import Excel </h2>           
              <div class="clearfix"></div>
            </div>
            <div class="x_content">
           
              <div class="col-md-8 col-sm-12 col-xs-12 form-group">      
              </div>
                    <input type="file" name="myfile" class="form-control"required>
                    <br>
                             <button type="submit" class="btn btn-success" >Upload Com Pandas</button> 
                          
                            </div>
                        </div>
                    </div>
                </div>
             
  </form>  
</center> 
{% endblock %}
````
Ainda dentro de templates criaremos o arquivo erro.html e colocaremos isso:
````python
{% load static %}

{% block content %}



    <head>
<!DOCTYPE html>
<html lang="en">
  <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
  <link rel="stylesheet" href="{% static 'navbar-top-fixed.css' %}">
  <link rel="stylesheet" href="{% static 'https://fonts.googleapis.com/css?family=Heebo:400,700|Oxygen:700' %}"> 
  <link rel="stylesheet" href="{% static 'dist/css/style.css' %}">
 <center>
 <h1> erro</h1>
  
</center> 
{% endblock %}
````

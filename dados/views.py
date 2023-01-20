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
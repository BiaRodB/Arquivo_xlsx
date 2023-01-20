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

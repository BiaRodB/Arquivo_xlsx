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



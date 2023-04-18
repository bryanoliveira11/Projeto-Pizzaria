from django.contrib import admin
from . import models

class TamanhosInline(admin.TabularInline):
    model = models.PizzaTamanhos
    extra = 1

class PizzasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'get_preco_formatado',)
    inlines = [TamanhosInline]
    
admin.site.register(models.Pizza, PizzasAdmin)
admin.site.register(models.PizzaTamanhos)
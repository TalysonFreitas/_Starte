from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuarios
# Register your models here.

class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('informações adicionais', {'fields': ('nome_completo', 'tipo')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informações Adicionais", {"fields": ("nome_completo", "tipo")}),
    )
admin.site.register(Usuarios, UsuarioAdmin)
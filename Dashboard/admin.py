from django.contrib import admin

from .models import (
	Usuario, 
	Materia, 
	Notas_periodos, 
	Periodo, 
	EstudianteUsuario, 
	grado)


class UsuarioInline(admin.TabularInline):
	model = Materia

class NotasAdmin(admin.ModelAdmin):

	list_display = ['periodo',]
	inlines = (UsuarioInline,)

	class Meta:
		model = Periodo

admin.site.register(Periodo, NotasAdmin)
admin.site.register(Notas_periodos)
admin.site.register(EstudianteUsuario)
admin.site.register(Usuario)
admin.site.register(grado)
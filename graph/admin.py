from django.contrib import admin

from .models import Pais, Ciudad


class CiudadTabularInline(admin.TabularInline):
	model = Ciudad
	can_delete=False


class PaisAdmin(admin.ModelAdmin):
	list_display = ['nombre']
	inlines = (CiudadTabularInline,)

	class Meta:
		model = Pais


admin.site.register(Pais, PaisAdmin)
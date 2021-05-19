from django.urls import path

from .views import (
		Periodo, 
		EstudianteRegistro, 
		ProfesorRegistro,
		inicio,
		regitrate_how, 
		ListaPeriodo, 
		periodo_api,
		lista_estudiante,
		looking,

		AuditorR)

urlpatterns = [

	path('inicio/', inicio, name='inicio'),
	path('indicaciones/', regitrate_how, name='regitrate_how'),

	path('registro_estudiante/', EstudianteRegistro.as_view(), name='singup_estu'),
	path('registro_profesor/', ProfesorRegistro.as_view(), name='singup_profe'),

	path('periodo/<int:pk>/', Periodo.as_view(), name='periodo'),
	path('periodo_api/<int:pk>/', periodo_api.as_view(), name='periodo_api'),

	path('ListaPeriodo/', ListaPeriodo.as_view(), name='ListaPeriodo'),

	path('reportes/', lista_estudiante, name='reportes_estudiante'),
	path('reportes/looking/', looking, name='looking'),

	
	path('AuditorR/', AuditorR.as_view(), name='AuditorR'),

]
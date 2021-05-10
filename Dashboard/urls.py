from django.urls import path

from .views import Periodo, EstudianteRegistro, inicio, ListaPeriodo, periodo_api

urlpatterns = [

	path('', inicio, name='inicio'),
	path('registro_estudiante/', EstudianteRegistro.as_view(), name='singup_estu'),
	path('periodo/<int:pk>/', Periodo.as_view(), name='periodo'),
	path('periodo_api/<int:pk>/', periodo_api.as_view(), name='periodo_api'),

	path('ListaPeriodo/', ListaPeriodo.as_view(), name='ListaPeriodo')

]
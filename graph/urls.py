from django.urls import path

from .views import pie_chart, poblacion_chart

urlpatterns = [
	
	path('pais/', pie_chart, name='Poblacion_ciudad'),
	path('pais_ajax/', poblacion_chart, name='pais_ajax'),
	
]
from django.urls import path 

from .views import DatosJsonViewSet, Login, PeriodoDetail, Logout, reporte_estudiante

urlpatterns = [
	
	path('login/', Login.as_view(), name='login'),
	path('json/', DatosJsonViewSet.as_view()),
	path('json/<int:pk>/', DatosJsonViewSet.as_view()),
	path('periodo/<int:pk>/', PeriodoDetail.as_view()),
	path('grado/<int:pk>/', reporte_estudiante.as_view()),
	path('logout/', Logout.as_view(), name='logout'),
	
]
from django.urls import path 

from .views import DatosJsonViewSet, Login, PeriodoDetail, Logout

urlpatterns = [
	
	path('login/', Login.as_view(), name='login'),
	path('json/', DatosJsonViewSet.as_view()),
	path('json/<int:pk>/', DatosJsonViewSet.as_view()),
	path('periodo/<int:pk>/', PeriodoDetail.as_view()),
	path('logout/', Logout.as_view(), name='logout'),
	
]
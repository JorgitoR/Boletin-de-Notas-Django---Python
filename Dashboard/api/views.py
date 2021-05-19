from rest_framework import serializers

from django.urls import reverse_lazy

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.shortcuts import render, get_object_or_404

from rest_framework import generics

from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.http import HttpResponseRedirect

from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token


from  rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from .serializers import NotaSerializer, PeriodoSerializer, EstudianteUserSerializer
from Dashboard.models import Notas_periodos, Usuario, Periodo, EstudianteUsuario, grado

class Login(FormView):
	template_name = 'Usuario/login.html'
	form_class = AuthenticationForm
	success_url = reverse_lazy('inicio')

	@method_decorator(never_cache)
	@method_decorator(csrf_protect)
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(self.get_success_url())
		else:
			return super(Login, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		usuario  = authenticate(username=username, password=password)
		token, created = Token.objects.get_or_create(user=usuario)
		if token:
			login(self.request, form.get_user())
			return super(Login, self).form_valid(form)


class Logout(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		request.user.auth_token.delete()
		logout(request)
		return Response(status=status.HTTP_200_OK)

class DatosJsonViewSet(generics.RetrieveAPIView):
	qs = Periodo.objects.all()
	serializer_class = PeriodoSerializer
	permission_classes =[permissions.AllowAny]

	def get_queryset(self, *args, **kwargs):
		qs = self.get_queryset
		return qs
 
class reporte_estudiante(APIView):
	def get(self, request, pk, format=None):

		labels = []
		if request.user.is_authenticated:
			if request.user.director:

				grado_pk = grado.objects.get(pk=pk)
				estudiante = EstudianteUsuario.objects.filter(grado=grado_pk)
		
				mujer = estudiante.filter(usuario__femenino=True)
				count_m = mujer.count()
				hombre = estudiante.filter(usuario__masculino=True)
				count_h = hombre.count()
				data = [count_m, count_h]

				for estudiante in estudiante:
					print(estudiante.usuario)
					labels.append(estudiante.usuario.username)

				print(labels)

				return Response({

					'jornada':estudiante.jornada.nombre,
					'data':data,
					'labels':labels
		
				})
		return Response({

			'error':"No tienes permiso para aceder"
		
		})
		


class PeriodoDetail(APIView):

	def get(self, request, pk, format=None):
		datos = []

		periodo = Periodo.objects.filter(pk=pk).values('materias__materia', 'materias__nota')
		print(periodo)

		for periodo in periodo:
			datos.append(periodo)


		return Response(data = {

			'data':datos,

		})
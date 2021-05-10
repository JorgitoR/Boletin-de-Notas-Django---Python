from django.shortcuts import render, redirect

from .models import Periodo, Notas_periodos
from django.views.generic import DetailView, CreateView, ListView

from django.db.models import Avg

from .forms import EstudiantesRegistro
from .models import Usuario


from django.contrib.auth import login


def inicio(request):

	if request.user.is_authenticated:

		if request.user.estudiante:
			return redirect('ListaPeriodo')
		else:
			return redirect('inicio')
	

	return render(request, 'inicio.html')

class EstudianteRegistro(CreateView):
	model = Usuario
	form_class = EstudiantesRegistro
	template_name='Usuario/estudiante.html'


	def get_context_data(self, **kwargs):
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		usuario = form.save()
		login(self.request, usuario)
		return redirect('ListaPeriodo')


class ListaPeriodo(ListView):
	model = Periodo
	context_object_name = 'periodos'
	template_name ='estudiante/periodos.html'

	def get_queryset(self):
		qs = self.request.user.estudianteusuario.nota_periodo \
			.select_related('periodo', 'periodo__usuario')
		return qs


##########---SECCION PROFESOR---###############

class periodo_api(DetailView):

	model = Periodo
	context_object_name ='periodo'	
	template_name='Periodo/resultado_api.html'

class Periodo(DetailView):

	model = Periodo
	context_object_name ='periodo'	
	template_name='Periodo/resultado.html'

	def get_context_data(self, **kwargs):
		periodo = self.get_object()

		labels = []
		datos = []

		perido_materia = periodo.materias.select_related('periodo__usuario')
		periodo_final = periodo.nota_periodo.select_related('estudiante__usuario')
		periodo_avg = periodo.nota_periodo.aggregate(promedio=Avg('periodo__nota_periodo'))

		print(periodo_avg)

		for periodo in perido_materia:
			labels.append(periodo.materia)
			datos.append(periodo.nota)

		print(labels, datos)

		context = {
			'perido_materia':perido_materia,
			'periodos':periodo_final,
			'periodo_avg':periodo_avg,

			'labels':labels,
			'data':datos
		}

		kwargs.update(context)
		return super().get_context_data(**kwargs)

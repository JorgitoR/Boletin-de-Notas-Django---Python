from django.shortcuts import render, redirect

from .models import Periodo, Notas_periodos
from django.views.generic import DetailView, CreateView, ListView

from django.db.models import Avg

from .forms import EstudiantesRegistro, profesorRegistro
from .models import Usuario, EstudianteUsuario, grado, jornada


from django.contrib.auth import login


def inicio(request):

	if request.user.is_authenticated:

		if request.user.estudiante:
			return redirect('ListaPeriodo')
		elif request.user.director:
			return redirect('reportes_estudiante')
		else:
			return redirect('inicio')

	return render(request, 'inicio.html')

def regitrate_how(request):

	return render(request, 'Usuario/indicaciones.html')

class ProfesorRegistro(CreateView):
	model = Usuario
	form_class = profesorRegistro
	template_name = 'Usuario/registro.html'

	def get_context_data(self, **kwargs):
		kwargs['keyy'] = 'Profesor'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		usuario = form.save()
		login(self.request, usuario)
		return redirect('reportes_estudiante')

class EstudianteRegistro(CreateView):
	model = Usuario
	form_class = EstudiantesRegistro
	template_name='Usuario/registro.html'


	def get_context_data(self, **kwargs):
		kwargs['keyy'] = 'Estudiante'
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



######## REPORTES #########
def parametro_query(param):
    return param != '' and param is not None

def filtro(request):
    qs                        = EstudianteUsuario.objects.all()
    jornada     = request.GET.get('jornadas')
    grado_qs     = request.GET.get('grados')
    activos = request.GET.get('activos')

    if parametro_query(activos):
        qs = qs.filter(usuario__activo=activos) 

    if parametro_query(grado_qs) and grado_qs != 'Elegir Grado':
        qs = qs.filter(grado__grado__icontains=grado_qs) 

    if parametro_query(jornada):
    	qs = qs.filter(jornada__nombre__icontains=jornada)

    return qs

def lista_estudiante(request):
	qs = filtro(request)

	context = {

		'filtro':qs,
		'jornada':jornada.objects.all(),
		'grados':grado.objects.all(),

	}

	return render(request, 'reportes/estudiante.html', context)


def looking(request):

    qs = filtro(request)
    print(qs)

    mujeres = qs.filter(usuario__femenino=True)
    contador_m = mujeres.count()
    hombres = qs.filter(usuario__masculino=True)
    contador_h = hombres.count()

    labels = ['mujeres', 'hombres']
    data = [contador_m, contador_h]


    context ={
        'estudiantes':qs,
        'labels':labels,
        'data':data
    }

    return render(request, 'reportes/looking.html', context)
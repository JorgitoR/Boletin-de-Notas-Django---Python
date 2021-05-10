from django.shortcuts import render

from .models import Ciudad

from django.http import JsonResponse

from django.db.models import Sum



def pie_chart(request):
	labels = []
	data = []

	qs = Ciudad.objects.order_by('-poblacion')[:5]
	for ciudad in qs:
		labels.append(ciudad.nombre)
		data.append(ciudad.poblacion)


	context = {

		'labels':labels,
		'data':data

	}

	return render(request, 'chart.html', context)


def poblacion_chart(request):
	labels = []
	datos = []


	qs = Ciudad.objects.values('pais__nombre').annotate(pais_poblacion=Sum('poblacion')).order_by('-pais_poblacion')
	for dato in qs:
		labels.append(dato['pais__nombre'])
		datos.append(dato['pais_poblacion'])

	print(labels)
	print(datos)

	return JsonResponse(data = {

		'labels':labels,
		'data':datos

	})

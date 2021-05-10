from django.db import models

class Pais(models.Model):
	nombre = models.CharField(max_length=30)

class Ciudad(models.Model):
	nombre = models.CharField(verbose_name='Nombre de la ciudad', max_length=30)
	pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
	poblacion = models.PositiveIntegerField()


from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import pre_save, post_save

from django.utils.html import mark_safe, escape

class Usuario(AbstractUser):
	director = models.BooleanField(default=False)
	subdirector = models.BooleanField(default=False)
	profesor = models.BooleanField(default=False)
	estudiante = models.BooleanField(default=False)

	activo = models.BooleanField(default=True)

	femenino = models.BooleanField(default=False)
	masculino = models.BooleanField(default=False)

class jornada(models.Model):
	nombre = models.CharField(max_length=20)
	color = models.CharField(default='#99C9FF', max_length=7)

	def __str__(self):
		return self.nombre

	def get_jornada(self):
		nombre = escape(self.nombre)
		color = escape(self.color)
		html =  '<span class="badge" style="color:#fff; background:%s">%s</span>' % (self.color, self.nombre)
		return mark_safe(html)


class grado(models.Model):
	grado = models.CharField(max_length=10)
	color = models.CharField(max_length=7, default='#333')

	def __str__(self):
		return self.grado

	def get_grado(self):
		grado = escape(self.grado)
		color = escape(self.color)
		html = '<span class="badge" style="color:#fff; background:%s">%s</span>' % (self.color, self.grado)
		return mark_safe(html)


class Periodo(models.Model):

	class Periodos(models.TextChoices):
		UNO = "UNO", "Uno",
		DOS = "DOS", "Dos",
		TRES = "TRES", "Tres"

	periodo = models.CharField(max_length=4, choices=Periodos.choices)
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='periodo')

	def __str__(self):
		return self.periodo

class Materia(models.Model):

	class NotasPeriodosMateria(models.TextChoices):
		MATH = "MATEMATICA", "Matematica",
		INGLES = "INGLES", "Ingles",
		SOCIALES = "SOCIALES", "Sociales"

	periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='materias')	
	materia = models.CharField(max_length=10, choices=NotasPeriodosMateria.choices)
	nota = models.FloatField()


class EstudianteUsuario(models.Model):

	class Jornada(models.TextChoices):
		MORNING = "MORNING", "Morning",
		AFTERNOON = "AFTERNOON", "Afternoon"

	usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
	grado  = models.ForeignKey(grado, on_delete=models.CASCADE, null=True)
	jornada = models.ForeignKey(jornada, on_delete=models.CASCADE, null=True)
	periodos = models.ManyToManyField(Periodo, through='Notas_periodos')


	def __str__(self):
		return "Estudiante {}, Grado {}".format(self.usuario.username, self.grado)


class Notas_periodos(models.Model):

	estudiante = models.ForeignKey(EstudianteUsuario, on_delete=models.CASCADE, related_name='nota_periodo')
	periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='nota_periodo')

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import pre_save, post_save

class Usuario(AbstractUser):
	director = models.BooleanField(default=False)
	subdirector = models.BooleanField(default=False)
	profesor = models.BooleanField(default=False)
	estudiante = models.BooleanField(default=False)

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
	usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
	periodos = models.ManyToManyField(Periodo, through='Notas_periodos')


	def __str__(self):
		return self.usuario.username

def instance_user(sender, instance, created, *args, **kwargs):

	if created:
		created = EstudianteUsuario.objects.get_or_create(usuario=instance)

post_save.connect(instance_user, sender=Usuario)

class Notas_periodos(models.Model):

	estudiante = models.ForeignKey(EstudianteUsuario, on_delete=models.CASCADE, related_name='nota_periodo')
	periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='nota_periodo')

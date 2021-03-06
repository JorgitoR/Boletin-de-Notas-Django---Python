from rest_framework import serializers
from Dashboard.models import Notas_periodos, Usuario, Periodo, EstudianteUsuario

class UsuarioSerializer(serializers.ModelSerializer):

	class Meta:
		model = Usuario
		fields = [
			"username",
			"first_name",
			"estudiante"
		]



class EstudianteUserSerializer(serializers.ModelSerializer):
	usuario = UsuarioSerializer(read_only=True)
	class Meta:
		model= EstudianteUsuario
		fields = [
			'usuario',
			'grado',
			
		]

class PeriodoSerializer(serializers.ModelSerializer):
	
	usuario = UsuarioSerializer(read_only=True)
	class Meta:
		model = Periodo
		fields = [

			'periodo',
			'usuario'
		]


class NotaSerializer(serializers.ModelSerializer):

	estudiante = UsuarioSerializer(read_only=True)

	class Meta:
		model = Notas_periodos

		fields = [

			'estudiante',
			'materia',
			'nota'
		]
from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import Usuario, grado, EstudianteUsuario, jornada

class AuditorRegistro(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = Usuario

	def save(self, commit=True):
		usuario = super().save(commit=False)
		usuario.auditor = True
		if commit:
			usuario.save()

		return usuario



class profesorRegistro(UserCreationForm):

	class Meta(UserCreationForm.Meta):
		model = Usuario

	def save(self, commit=True):
		usuario = super().save(commit=False)
		usuario.profesor = True
		if commit:
			usuario.save()

		return usuario

class EstudiantesRegistro(UserCreationForm):

	jornada = forms.ModelChoiceField(
		queryset = jornada.objects.all(),
		widget = forms.RadioSelect(),
		required=True
	)

	grado = forms.ModelChoiceField(
		queryset = grado.objects.all(),
		widget = forms.RadioSelect(),
		required=True
	)

	class Meta(UserCreationForm.Meta):
		model = Usuario
		
	def save(self, commit=True):
		user = super().save(commit=False)
		user.estudiante = True
		if commit:
			user.save()

		grade = self.cleaned_data.get('grado')
		jornada = self.cleaned_data.get('jornada')
		gradoss = EstudianteUsuario.objects.create(usuario=user, grado=grade, jornada=jornada)
		return user
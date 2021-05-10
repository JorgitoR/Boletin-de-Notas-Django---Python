from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class EstudiantesRegistro(UserCreationForm):

	class Meta(UserCreationForm.Meta):
		model = Usuario
		
	def save(self, commit=True):
		user = super().save(commit=False)
		user.estudiante = True
		if commit:
			user.save()
		return user
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Form_user(forms.ModelForm):
	class Meta:
		model = User
		fields = [
		'username',
		'password',
		'email'
		]
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_recaptcha.fields import ReCaptchaField
from captcha.fields import CaptchaField
from .models import *

# Usuario
class UserInfoForm(forms.ModelForm):
    telefono = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Telefono'}), required=False)
    direccion = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección 1'}), required=False)
    direccion_dos = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Dirección 2'}), required=False)
    ciudad = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ciudad'}), required=False)
    comuna = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Comuna'}), required=False)
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=False)
    pais = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Pais'}), required=False)

    class Meta:
        model = Perfil
        fields = ('telefono', 'direccion', 'direccion_dos', 'ciudad', 'comuna', 'zipcode', 'pais',)

# Empleado
class EmpleadoForm(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Empleado
        fields = '__all__'

# Servicio
class ServicioForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Servicio
        fields = '__all__'

# Producto
class ProductoForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Producto
        fields = '__all__'

# Sesión
class UpdateUserForm(UserChangeForm):
    captcha = CaptchaField()

    password = None
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo electronico'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Obligatorio. 150 caracteres o menos. Solo letras, digitos y @/./+/-/_</small></span>'

class SignUpForm(UserCreationForm):
    captcha = CaptchaField()

    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo electronico'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Obligatorio. 150 caracteres o menos. Solo letras, digitos y @/./+/-/_</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Tú contraseña no puede ser muy similar a tu información personal.</li><li>Tu contraseña debe contener al menos 8 caracteres.</li><li>Tu contraseña no puede ser una contraseña común.</li><li>Tu contraseña no puede ser completamente númerica.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar contraseña'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Para verificar, ingresa nuevamente la contraseña.</small></span>'
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from .models import Profile


class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput()
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput()
    )

    security_question = forms.ChoiceField(
        choices=Profile.PREGUNTAS,
        label="Pregunta de seguridad"
    )

    security_answer = forms.CharField(
        label="Respuesta de seguridad"
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
        ]

    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este correo ya está registrado."
            )

        return email

    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError(
                "Las contraseñas no coinciden."
            )

        return cleaned_data


class RecoverUserForm(forms.Form):

    username = forms.CharField(
        label="Usuario"
    )


class SecurityAnswerForm(forms.Form):

    answer = forms.CharField(
        label="Respuesta de seguridad"
    )


class NewPasswordForm(SetPasswordForm):
    pass
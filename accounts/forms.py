from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Contraseña",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirmar contraseña",
            }
        ),
    )

    pregunta_seguridad = forms.ChoiceField(
        label="Pregunta de seguridad",
        choices=[
            ("", "Seleccione una pregunta"),
            *Profile.SECURITY_QUESTIONS,
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    respuesta_seguridad = forms.CharField(
        label="Respuesta de seguridad",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Escriba su respuesta",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombres",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Apellidos",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Usuario",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Correo electrónico",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get(
            "email",
            "",
        ).strip().lower()

        if not email:
            raise forms.ValidationError(
                "El correo electrónico es obligatorio."
            )

        if User.objects.filter(
            email__iexact=email
        ).exists():
            raise forms.ValidationError(
                "Este correo ya está registrado."
            )

        return email

    def clean_respuesta_seguridad(self):
        respuesta = self.cleaned_data.get(
            "respuesta_seguridad",
            "",
        ).strip()

        if len(respuesta) < 2:
            raise forms.ValidationError(
                "La respuesta debe tener al menos 2 caracteres."
            )

        return respuesta

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error(
                    "password2",
                    "Las contraseñas no coinciden.",
                )
            else:
                try:
                    password_validation.validate_password(
                        password1
                    )
                except forms.ValidationError as error:
                    self.add_error(
                        "password1",
                        error,
                    )

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]

        labels = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "email": "Correo electrónico",
        }

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombres",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Apellidos",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Correo electrónico",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get(
            "email",
            "",
        ).strip().lower()

        if not email:
            raise forms.ValidationError(
                "El correo electrónico es obligatorio."
            )

        queryset = User.objects.filter(
            email__iexact=email
        ).exclude(
            pk=self.instance.pk
        )

        if queryset.exists():
            raise forms.ValidationError(
                "Este correo ya pertenece a otro usuario."
            )

        return email


class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = [
            "foto",
        ]

        widgets = {
            "foto": forms.ClearableFileInput(
                attrs={
                    "class": "form-control-file",
                    "accept": "image/jpeg,image/png,image/webp",
                }
            ),
        }

    def clean_foto(self):
        foto = self.cleaned_data.get("foto")

        if not foto:
            return foto

        import os

        extension = os.path.splitext(foto.name)[1].lower()

        if extension not in [".jpg", ".jpeg", ".png", ".webp"]:
            raise forms.ValidationError(
                "La foto debe estar en formato JPG, PNG o WEBP."
            )

        if foto.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "La foto no puede superar los 5 MB."
            )

        return foto


class SecurityQuestionUpdateForm(forms.ModelForm):
    respuesta_seguridad = forms.CharField(
        label="Nueva respuesta de seguridad",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Escriba la nueva respuesta",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = Profile

        fields = [
            "pregunta_seguridad",
            "respuesta_seguridad",
        ]

        widgets = {
            "pregunta_seguridad": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_respuesta_seguridad(self):
        respuesta = self.cleaned_data.get(
            "respuesta_seguridad",
            "",
        ).strip()

        if len(respuesta) < 2:
            raise forms.ValidationError(
                "La respuesta debe tener al menos 2 caracteres."
            )

        return respuesta


class RecoverPasswordForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese su nombre de usuario",
                "autocomplete": "username",
            }
        ),
    )


class SecurityAnswerForm(forms.Form):
    respuesta = forms.CharField(
        label="Respuesta",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Escriba su respuesta",
                "autocomplete": "off",
            }
        ),
    )


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nueva contraseña",
                "autocomplete": "new-password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirmar nueva contraseña",
                "autocomplete": "new-password",
            }
        ),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error(
                    "password2",
                    "Las contraseñas no coinciden.",
                )
            else:
                try:
                    password_validation.validate_password(
                        password1,
                        user=self.user,
                    )
                except forms.ValidationError as error:
                    self.add_error(
                        "password1",
                        error,
                    )

        return cleaned_data
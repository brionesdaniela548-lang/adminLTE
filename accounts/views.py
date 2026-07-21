from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import (
    check_password,
    make_password,
)
from django.contrib.auth.models import User
from django.shortcuts import (
    redirect,
    render,
)

from .forms import (
    ProfilePhotoForm,
    RecoverPasswordForm,
    RegisterForm,
    ResetPasswordForm,
    SecurityAnswerForm,
    SecurityQuestionUpdateForm,
    UserProfileForm,
)
from .models import Profile


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(
                commit=False
            )

            user.set_password(
                form.cleaned_data["password1"]
            )

            user.email = form.cleaned_data[
                "email"
            ].strip().lower()

            user.save()

            Profile.objects.create(
                user=user,
                pregunta_seguridad=form.cleaned_data[
                    "pregunta_seguridad"
                ],
                respuesta_seguridad=make_password(
                    form.cleaned_data[
                        "respuesta_seguridad"
                    ].strip().lower()
                ),
            )

            messages.success(
                request,
                (
                    "Cuenta creada correctamente. "
                    "Ya puedes iniciar sesión."
                ),
            )

            return redirect("login")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get(
            "username",
            "",
        ).strip()

        password = request.POST.get(
            "password",
            "",
        )

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(
                request,
                user,
            )

            return redirect("dashboard")

        messages.error(
            request,
            "Usuario o contraseña incorrectos.",
        )

    return render(
        request,
        "accounts/login.html",
    )


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("login")


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        user_form = UserProfileForm(
            request.POST,
            instance=request.user,
        )

        photo_form = ProfilePhotoForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if user_form.is_valid() and photo_form.is_valid():
            user_form.save()
            photo_form.save()

            messages.success(
                request,
                "Tu perfil fue actualizado correctamente.",
            )

            return redirect("profile")

    else:
        user_form = UserProfileForm(
            instance=request.user
        )

        photo_form = ProfilePhotoForm(
            instance=profile
        )

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "user_form": user_form,
            "photo_form": photo_form,
        },
    )


@login_required
def password_change_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(
            request.user,
            request.POST,
        )

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(
                request,
                user,
            )

            messages.success(
                request,
                "Tu contraseña fue cambiada correctamente.",
            )

            return redirect("profile")

    else:
        form = PasswordChangeForm(
            request.user
        )

    for field in form.fields.values():
        field.widget.attrs.update(
            {
                "class": "form-control",
            }
        )

    return render(
        request,
        "accounts/password_change.html",
        {
            "form": form,
        },
    )


@login_required
def security_question_update_view(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = SecurityQuestionUpdateForm(
            request.POST,
            instance=profile,
        )

        if form.is_valid():
            profile = form.save(
                commit=False
            )

            profile.respuesta_seguridad = make_password(
                form.cleaned_data[
                    "respuesta_seguridad"
                ].strip().lower()
            )

            profile.save()

            messages.success(
                request,
                (
                    "La pregunta y la respuesta de seguridad "
                    "fueron actualizadas correctamente."
                ),
            )

            return redirect("profile")

    else:
        form = SecurityQuestionUpdateForm(
            instance=profile,
            initial={
                "respuesta_seguridad": "",
            },
        )

    return render(
        request,
        "accounts/security_question_update.html",
        {
            "form": form,
        },
    )


def recover_password(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    request.session.pop(
        "recovery_user_id",
        None,
    )

    request.session.pop(
        "recovery_verified",
        None,
    )

    if request.method == "POST":
        form = RecoverPasswordForm(
            request.POST
        )

        if form.is_valid():
            username = form.cleaned_data[
                "username"
            ].strip()

            user = User.objects.filter(
                username__iexact=username,
                is_active=True,
            ).first()

            if user is None:
                messages.error(
                    request,
                    "No existe un usuario activo con ese nombre.",
                )

            else:
                profile, _ = Profile.objects.get_or_create(
                    user=user
                )

                if (
                    not profile.pregunta_seguridad
                    or not profile.respuesta_seguridad
                ):
                    messages.error(
                        request,
                        (
                            "Este usuario no tiene configurada "
                            "una pregunta de seguridad."
                        ),
                    )

                else:
                    request.session[
                        "recovery_user_id"
                    ] = user.id

                    request.session[
                        "recovery_verified"
                    ] = False

                    return redirect(
                        "security_question"
                    )

    else:
        form = RecoverPasswordForm()

    return render(
        request,
        "accounts/recover_password.html",
        {
            "form": form,
        },
    )


def security_question(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    user_id = request.session.get(
        "recovery_user_id"
    )

    if not user_id:
        messages.error(
            request,
            "Primero debes ingresar tu nombre de usuario.",
        )

        return redirect(
            "recover_password"
        )

    user = User.objects.filter(
        id=user_id,
        is_active=True,
    ).first()

    if user is None:
        request.session.pop(
            "recovery_user_id",
            None,
        )

        request.session.pop(
            "recovery_verified",
            None,
        )

        messages.error(
            request,
            "No se pudo encontrar el usuario.",
        )

        return redirect(
            "recover_password"
        )

    profile, _ = Profile.objects.get_or_create(
        user=user
    )

    if (
        not profile.pregunta_seguridad
        or not profile.respuesta_seguridad
    ):
        messages.error(
            request,
            (
                "Este usuario no tiene configurada "
                "una pregunta de seguridad."
            ),
        )

        return redirect(
            "recover_password"
        )

    if request.method == "POST":
        form = SecurityAnswerForm(
            request.POST
        )

        if form.is_valid():
            respuesta = form.cleaned_data[
                "respuesta"
            ].strip().lower()

            respuesta_correcta = check_password(
                respuesta,
                profile.respuesta_seguridad,
            )

            if respuesta_correcta:
                request.session[
                    "recovery_verified"
                ] = True

                return redirect(
                    "reset_password"
                )

            messages.error(
                request,
                "La respuesta de seguridad es incorrecta.",
            )

    else:
        form = SecurityAnswerForm()

    return render(
        request,
        "accounts/security_question.html",
        {
            "form": form,
            "username": user.username,
            "pregunta": profile.get_pregunta_seguridad_display(),
        },
    )


def reset_password(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    user_id = request.session.get(
        "recovery_user_id"
    )

    recovery_verified = request.session.get(
        "recovery_verified",
        False,
    )

    if not user_id or not recovery_verified:
        messages.error(
            request,
            (
                "Debes responder correctamente la "
                "pregunta de seguridad."
            ),
        )

        return redirect(
            "recover_password"
        )

    user = User.objects.filter(
        id=user_id,
        is_active=True,
    ).first()

    if user is None:
        request.session.pop(
            "recovery_user_id",
            None,
        )

        request.session.pop(
            "recovery_verified",
            None,
        )

        messages.error(
            request,
            "No se pudo encontrar el usuario.",
        )

        return redirect(
            "recover_password"
        )

    if request.method == "POST":
        form = ResetPasswordForm(
            request.POST,
            user=user,
        )

        if form.is_valid():
            user.set_password(
                form.cleaned_data[
                    "password1"
                ]
            )

            user.save()

            request.session.pop(
                "recovery_user_id",
                None,
            )

            request.session.pop(
                "recovery_verified",
                None,
            )

            messages.success(
                request,
                (
                    "Tu contraseña fue restablecida "
                    "correctamente. Ya puedes iniciar sesión."
                ),
            )

            return redirect(
                "login"
            )

    else:
        form = ResetPasswordForm(
            user=user
        )

    return render(
        request,
        "accounts/reset_password.html",
        {
            "form": form,
            "username": user.username,
        },
    )
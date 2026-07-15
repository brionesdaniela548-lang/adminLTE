from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import (
    NewPasswordForm,
    RecoverUserForm,
    RegisterForm,
    SecurityAnswerForm,
)
from .models import Profile


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data["password1"]
            )

            user.save()

            Profile.objects.create(
                user=user,
                security_question=form.cleaned_data[
                    "security_question"
                ],
                security_answer=form.cleaned_data[
                    "security_answer"
                ].strip().lower(),
            )

            messages.success(
                request,
                "Cuenta creada correctamente. Ya puedes iniciar sesión.",
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
    profile = Profile.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
        },
    )


def recover_password(request):
    if request.method == "POST":
        form = RecoverUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data[
                "username"
            ].strip()

            try:
                user = User.objects.get(
                    username=username
                )

                request.session[
                    "recover_user"
                ] = user.id

                request.session.pop(
                    "security_answer_verified",
                    None,
                )

                return redirect(
                    "security_question"
                )

            except User.DoesNotExist:
                messages.error(
                    request,
                    "El usuario no existe.",
                )

    else:
        form = RecoverUserForm()

    return render(
        request,
        "accounts/recover_password.html",
        {
            "form": form,
        },
    )


def security_question(request):
    user_id = request.session.get(
        "recover_user"
    )

    if not user_id:
        return redirect(
            "recover_password"
        )

    try:
        user = User.objects.get(
            id=user_id
        )

        profile = Profile.objects.get(
            user=user
        )

    except User.DoesNotExist:
        request.session.pop(
            "recover_user",
            None,
        )

        messages.error(
            request,
            "El usuario ya no existe.",
        )

        return redirect(
            "recover_password"
        )

    except Profile.DoesNotExist:
        request.session.pop(
            "recover_user",
            None,
        )

        messages.error(
            request,
            "El usuario no tiene una pregunta de seguridad configurada.",
        )

        return redirect(
            "recover_password"
        )

    if request.method == "POST":
        form = SecurityAnswerForm(
            request.POST
        )

        if form.is_valid():
            answer = form.cleaned_data[
                "answer"
            ].strip().lower()

            if answer == profile.security_answer:
                request.session[
                    "security_answer_verified"
                ] = True

                return redirect(
                    "reset_password"
                )

            messages.error(
                request,
                "Respuesta incorrecta.",
            )

    else:
        form = SecurityAnswerForm()

    return render(
        request,
        "accounts/security_question.html",
        {
            "form": form,
            "question": profile.get_security_question_display(),
        },
    )


def reset_password(request):
    user_id = request.session.get(
        "recover_user"
    )

    answer_verified = request.session.get(
        "security_answer_verified"
    )

    if not user_id or not answer_verified:
        return redirect(
            "recover_password"
        )

    try:
        user = User.objects.get(
            id=user_id
        )

    except User.DoesNotExist:
        request.session.pop(
            "recover_user",
            None,
        )

        request.session.pop(
            "security_answer_verified",
            None,
        )

        messages.error(
            request,
            "El usuario ya no existe.",
        )

        return redirect(
            "recover_password"
        )

    if request.method == "POST":
        form = NewPasswordForm(
            user,
            request.POST,
        )

        if form.is_valid():
            form.save()

            request.session.pop(
                "recover_user",
                None,
            )

            request.session.pop(
                "security_answer_verified",
                None,
            )

            messages.success(
                request,
                "Contraseña cambiada correctamente.",
            )

            return redirect(
                "login"
            )

    else:
        form = NewPasswordForm(
            user
        )

    return render(
        request,
        "accounts/reset_password.html",
        {
            "form": form,
        },
    )
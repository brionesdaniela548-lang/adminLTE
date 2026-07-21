from django.urls import path

from . import views


urlpatterns = [
    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    path(
        "profile/",
        views.profile_view,
        name="profile",
    ),

    path(
        "change-password/",
        views.password_change_view,
        name="password_change",
    ),

    path(
        "security-question/update/",
        views.security_question_update_view,
        name="security_question_update",
    ),

    path(
        "recover-password/",
        views.recover_password,
        name="recover_password",
    ),

    path(
        "security-question/",
        views.security_question,
        name="security_question",
    ),

    path(
        "reset-password/",
        views.reset_password,
        name="reset_password",
    ),
]
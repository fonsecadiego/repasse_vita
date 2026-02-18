from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from apps.repasse.forms import LoginForm
from apps.repasse.permissions import is_gestor


def _get_dashboard_url(user) -> str:
    if is_gestor(user):
        return reverse("repasse-dashboard-gestor")
    return reverse("repasse-dashboard-medico")


class LoginView(View):
    http_method_names = ["get", "post"]

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect(_get_dashboard_url(request.user))
        return render(request, "repasse/auth/login.html", {"form": LoginForm()})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "repasse/auth/login.html", {"form": form}, status=400)

        user = authenticate(
            request=request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is None:
            form.add_error(None, "Usuário ou senha inválidos.")
            return render(request, "repasse/auth/login.html", {"form": form}, status=400)

        login(request, user)
        return redirect(_get_dashboard_url(user))


@method_decorator(login_required, name="dispatch")
class LogoutView(View):
    http_method_names = ["post"]

    def post(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect("login")

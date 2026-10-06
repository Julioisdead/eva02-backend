from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from solucion import decidir  # la regla de la ES1, intacta (no se copia)
from .models import Reserva
from .permisos import requiere_rol, tiene_rol

HORAS = range(9, 19)


def _leer_form(request):
    """Valida ANTES de escribir: un int() sin try daria error 500."""
    nombre = request.POST.get("nombre", "").strip()
    try:
        hora = int(request.POST.get("hora_solicitada", ""))
        cupos = int(request.POST.get("cupos_disponibles", ""))
    except ValueError:
        return None, "Hora y cupos deben ser numeros enteros."
    if not nombre:
        return None, "El nombre es obligatorio."
    return (nombre, hora, cupos), None


@login_required(login_url="login")
def lista(request):  # READ
    return render(request, "lista.html", {
        "registros": Reserva.objects.filter(eliminado=False),
        "puede_crear": tiene_rol(request.user, "admin", "normal"),
        "es_admin": tiene_rol(request.user, "admin"),
    })


@requiere_rol("admin", "normal")
def crear(request):  # CREATE
    error = None
    if request.method == "POST":
        datos, error = _leer_form(request)
        if not error:
            nombre, hora, cupos = datos
            estado, motivo = decidir(hora, cupos)
            Reserva.objects.create(nombre=nombre, hora_solicitada=hora,
                                   cupos_disponibles=cupos,
                                   estado=estado, motivo=motivo)
            messages.success(request, f"{nombre}: {estado}. {motivo}")
            return redirect("lista")
    return render(request, "form.html",
                  {"accion": "Crear", "error": error, "horas": HORAS})


@requiere_rol("admin")
def editar(request, pk):  # UPDATE
    reg = get_object_or_404(Reserva, pk=pk, eliminado=False)
    error = None
    if request.method == "POST":
        datos, error = _leer_form(request)
        if not error:
            reg.nombre, reg.hora_solicitada, reg.cupos_disponibles = datos
            # recalcular: si no, la ficha queda mintiendo
            reg.estado, reg.motivo = decidir(reg.hora_solicitada,
                                             reg.cupos_disponibles)
            reg.save()
            messages.success(request, "Reserva actualizada.")
            return redirect("lista")
    return render(request, "form.html", {"accion": "Editar", "registro": reg,
                                         "error": error, "horas": HORAS})


@requiere_rol("admin")
def eliminar(request, pk):  # DELETE logico
    reg = get_object_or_404(Reserva, pk=pk, eliminado=False)
    if request.method == "POST":
        reg.soft_delete()
        messages.success(request, "Reserva eliminada.")
        return redirect("lista")
    return render(request, "confirmar.html", {"registro": reg})


def vista_login(request):
    if request.method == "POST":
        user = authenticate(request,
                            username=request.POST.get("username", "").strip(),
                            password=request.POST.get("password", ""))
        if user:
            login(request, user)
            return redirect("lista")
        messages.error(request, "Usuario o contrasena incorrectos.")
    return render(request, "login.html")


def vista_logout(request):
    logout(request)
    return redirect("login")

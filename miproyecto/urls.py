from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="lista")),
    path("login/", views.vista_login, name="login"),
    path("logout/", views.vista_logout, name="logout"),
    path("registros/", views.lista, name="lista"),
    path("registros/crear/", views.crear, name="crear"),
    path("registros/<int:pk>/editar/", views.editar, name="editar"),
    path("registros/<int:pk>/eliminar/", views.eliminar, name="eliminar"),
]

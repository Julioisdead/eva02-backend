"""Crea los grupos y un usuario por rol. Se corre con: python crear_usuarios.py
Las contrasenas salen del .env (PASS_JEFE, PASS_BARBERO, PASS_LECTOR)
o se piden por teclado. NUNCA van escritas en este archivo."""
import os
from getpass import getpass

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "miproyecto.settings")
django.setup()

from decouple import config
from django.contrib.auth.models import Group, User

USUARIOS = [("jefe", "admin"), ("barbero", "normal"), ("lector", "viewer")]

for rol in ("admin", "normal", "viewer"):
    Group.objects.get_or_create(name=rol)

for username, rol in USUARIOS:
    if User.objects.filter(username=username).exists():
        print(f"{username}: ya existe")
        continue
    password = config(f"PASS_{username.upper()}", default="") or \
        getpass(f"Contrasena para {username} ({rol}): ")
    user = User.objects.create_user(username, password=password)
    user.groups.add(Group.objects.get(name=rol))
    print(f"{username}: creado con rol {rol}")

# Plan · Sistema de reserva de horas para barbería (Eva 2)

## 1. Apartado de negocio

**Problema**
Hoy el agendamiento se hace a mano por WhatsApp o Instagram. Los clientes piden turnos cuando el barbero ya está lleno o en horarios en que el local está cerrado, y el dueño responde cruzando cada mensaje con una libreta de papel. Eso produce dobles reservas, clientes que llegan y no son atendidos, y horas mal anotadas.

**Solución**
Una aplicación web que valida la hora pedida y los cupos disponibles antes de confirmar, guarda cada reserva en una base de datos y le da a cada persona solo lo que le corresponde según su rol.

**Alcance (versión Eva 2)**
- Entra: base de datos SQLite, CRUD completo de reservas, borrado lógico, panel de administración de Django, login/logout y tres roles (admin, normal, viewer).
- No entra: pagos, elegir barbero específico, reservas hechas directamente por los clientes.

**MoSCoW**

| Prioridad | Función |
|---|---|
| Must | Regla de decisión con 4 resultados (`decidir()`, reutilizada de la ES1) |
| Must | Guardar las reservas en SQLite mediante un modelo (`Reserva`) |
| Must | CRUD: listar, crear, editar y eliminar (borrado lógico) |
| Must | Login/logout y roles: admin (todo), normal (ve y crea), viewer (solo ve) |
| Must | Panel de administración con columnas, filtro y buscador |
| Should | Mostrar la fecha de eliminación y recuperar reservas eliminadas |
| Could | Exportar las reservas del día a Excel |
| Won't | Pagos en línea y elección de barbero |

## 2. Apartado técnico

**Datos de entrada**

| Dato | Tipo | Descripción |
|---|---|---|
| `nombre` | texto (str) | Nombre del cliente |
| `hora_solicitada` | entero (int) | Hora del corte, de 9 a 18 en el formulario |
| `cupos_disponibles` | entero (int) | Cupos que quedan en ese bloque |

**Regla de decisión (sin cambios respecto a la ES1)**
1. Dato inválido (cupos negativos u hora fuera de 0–23) → Rechazado. Se revisa primero.
2. Fuera de horario (antes de las 9 o desde las 19) → Rechazado.
3. Sin cupos (`cupos_disponibles == 0`) → Rechazado.
4. Dentro de horario y con cupos → Aceptado.

La regla vive solo en `solucion.py`; las vistas la importan. Al editar una reserva se vuelve a calcular.

**Modelo `Reserva`**: nombre, hora_solicitada, cupos_disponibles, estado (con `choices`), motivo, fecha_creacion, eliminado y fecha_eliminacion (borrado lógico).

**Rutas y permisos** (se validan en el servidor con el decorador `requiere_rol`, no solo escondiendo botones)

| Ruta | Qué hace | Quién |
|---|---|---|
| `/registros/` | Listar | Cualquier usuario con sesión |
| `/registros/crear/` | Crear | admin y normal |
| `/registros/<id>/editar/` | Editar | admin |
| `/registros/<id>/eliminar/` | Eliminar (lógico) | admin |
| `/login/` `/logout/` | Entrar y salir | Todos |
| `/admin/` | Panel de Django | Superusuario |

**Paquete externo**: `tabulate`, usado en `solucion.py` para mostrar el resumen en consola (ES1). Contraseñas y `SECRET_KEY` salen del `.env`.

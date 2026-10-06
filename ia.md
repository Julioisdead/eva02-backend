# ia.md · Uso de IA (Eva 2)

## Qué herramienta usé y para qué
Usé Claude (Anthropic). En la ES1 me ayudó con el plan, la regla de decisión y la primera versión en Django. En la Eva 2 la usé para pasar el proyecto de `datos.json` a una base de datos SQLite, y después para completar lo que le faltaba a esa migración: CRUD, borrado lógico, login y roles.

## Una consulta concreta y qué respondió
Le mostré una foto de la pizarra de la clase (Models para el ORM, `createsuperuser` del admin de Django y una base de datos) y le pedí: "Necesito hacer esto con lo que trabajamos antes". Me propuso un modelo `Reserva`, registrarlo en el admin, correr las migraciones y cambiar la vista para guardar con `Reserva.objects.create()` en vez de escribir el JSON.

## Qué estaba mal, sobraba o no entendí, y cómo lo corregí
- **La primera migración quedó incompleta.** La IA la armó solo con la foto de la pizarra, sin la guía de la Eva 2. Cuando conseguí el documento "De la ES1 a la Eva 2" vi que faltaban el CRUD completo, el borrado lógico, el login y los roles, que son lo que más pesa. Revisé el documento contra mi proyecto y las agregué.
- **El ejemplo del documento no calzaba con mi código.** Ahí `decidir()` devuelve un texto, pero la mía devuelve `(estado, motivo)`. En vez de reescribir la regla, adapté las vistas para desempaquetar los dos valores. Así la regla sigue en un solo archivo.
- **Seguridad de los roles.** Entendí que esconder un botón con `{% if %}` no protege nada, porque cualquiera puede escribir la dirección. Por eso los permisos están en el decorador `requiere_rol`, en el servidor. Lo probé entrando con el usuario `lector` y escribiendo `/registros/1/editar/` a mano: me rechaza.
- **Contraseñas fuera del código.** Los usuarios se crean con `crear_usuarios.py`, que pide las contraseñas por teclado o las lee del `.env`; no están escritas en ningún archivo.
- **Validación.** Un `int()` sin `try/except` da error 500 si alguien escribe letras; lo valido antes de guardar.
- **Editar recalcula.** Al editar, se vuelve a llamar a `decidir()`; si no, la reserva quedaba con un resultado viejo.

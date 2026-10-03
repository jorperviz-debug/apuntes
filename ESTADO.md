# Estado del proyecto
Última actualización: 2026-10-03 — Mac: MacBook Air de Jorge

## Objetivo general
Mantener y ampliar la web de apuntes de Física y Química para mis alumnos, pasando poco a poco los PDF de Google Drive al propio proyecto.

## Estado actual
- Web publicada en https://jorperviz-debug.github.io/apuntes/ (repositorio público `jorperviz-debug/apuntes`).
- Las páginas se generan desde `cursos.json` con `build.py`; GitHub las publica solo en cada push a `main`.
- Cursos: 2.º ESO (3 materiales), 3.º ESO (4, tema 1), 1.º Bachillerato (próximamente), 2.º Bachillerato (8),
  FP Básica (la casilla abre directamente su PDF).
- Casillas de la portada con número grande + etapa («2.º / Bachillerato»); ya no hay códigos tipo «2B».
- Los 12 PDF de Jorge están alojados en la web (`pdf/<curso>/<tema>/`, 33,6 MB en total); ya no dependen de Google Drive.
  Solo los 3 recursos de otros profesores (2.º Bach, «Otros resúmenes y formularios») siguen siendo enlaces externos.

## Pendiente
- Preparar el segundo Mac (descargar la web desde GitHub, instalar `gh` e iniciar sesión).

- Opcional: Jorge puede dar permiso a Claude para leer iCloud Drive (Ajustes › Privacidad y seguridad) y así no
  tener que copiar los PDF a mano.

- Rediseño de la web (aparcado por Jorge): quiere ver una propuesta **totalmente distinta** (colores, disposición…),
  no retoques del diseño actual. La primera propuesta («Cuaderno de laboratorio»: mismas casillas con otra letra y
  fondo cuadriculado) no le convenció por parecerse demasiado. Enseñar siempre como vista previa, sin aplicar hasta
  que diga «aplícalo».

## Siguiente paso
Preparar el segundo Mac siguiendo «Primer uso en otro Mac» de CLAUDE.md.

## Decisiones y convenciones vigentes
- Contenido solo en `cursos.json`; no editar HTML a mano. No cambiar el diseño salvo petición expresa.
- PDF en `pdf/<curso>/<seccion>/` con nombres en minúsculas, sin tildes ni espacios.
- La web NO va en iCloud: se sincroniza entre Macs con GitHub (`git pull` al empezar, `git push` al terminar).
- ESTADO.md y BITACORA.md están en el repositorio público: nada privado ni datos de alumnos.
- Commits firmados como «Jorge Pérez Vizcaíno» con el correo anónimo de GitHub (no el Gmail).
- Cuando Jorge quiera ver un enlace, abrirlo en Safari (`open -a Safari <url>`).
- Si un PDF mezcla teoría, ejercicios y soluciones, se separa (con pypdf) y las soluciones van al final.

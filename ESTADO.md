# Estado del proyecto
Última actualización: 2026-11-04 — Mac: MacBook Air de Jorge

## Objetivo general
Mantener y ampliar la web de apuntes de Física y Química para mis alumnos, pasando poco a poco los PDF de Google Drive al propio proyecto.

## Estado actual
- Web publicada en https://jorperviz-debug.github.io/apuntes/ (repositorio público `jorperviz-debug/apuntes`).
  Las páginas se generan desde `cursos.json` con `build.py`; GitHub las publica solo en cada push a `main`.
- Cursos: 2.º ESO (3 materiales), 3.º ESO (4, Tema 1), 1.º Bachillerato (próximamente),
  2.º Bachillerato (12 visibles), FP Básica (la casilla abre directamente su PDF).
- 2.º Bachillerato, organizado en **bloques** (ya no hay sección general «Apuntes y ejercicios»):
  - «Otros resúmenes y formularios» (recursos externos), arriba y en pequeño.
  - Bloque 0: Introducción (formulario y vectores).
  - Bloque 1: Campo gravitatorio — Apuntes, Ejercicios, Boletín PAU para clase, Boletín PAU para casa (+ soluciones),
    Demostraciones.
  - Bloque 2: Electromagnetismo — Apuntes y Ejercicios (PDF del bloque entero: eléctrico, magnético e inducción).
  - Sección «Ejercicios y cuestiones de repaso» oculta de momento.
- Diseño: portada con un color por curso; páginas de curso con índice lateral, número solo en temas/bloques (00, 01, 02),
  secciones generales en verde y temas/bloques en el color del curso.

## Pendiente
- **Dos soluciones OCULTAS** en el Bloque 1 de 2.º Bach, esperando a que Jorge diga «actívalas»:
  «Soluciones Ejercicios Campo Gravitatorio» y «Soluciones boletín ejercicios tipo PAU para clase».
  Los PDF están SOLO en este MacBook Air, en `privado/2-bachillerato/tema-1/` (no están en GitHub).
- Preparar el segundo Mac (descargar la web desde GitHub, instalar `gh` e iniciar sesión).
- Opcional: corregir en el PDF de demostraciones la fecha («October 9, 2025») y la errata «la la».
- Opcional: Jorge puede dar permiso a Claude para leer iCloud Drive (Ajustes › Privacidad y seguridad) y así no
  tener que copiar los PDF a mano a la carpeta PaginaInstituto.

## Siguiente paso
Lo que Jorge traiga (nuevos materiales o activar soluciones); cuando haya tiempo, preparar el segundo Mac.

## Decisiones y convenciones vigentes
- Contenido solo en `cursos.json`; no editar HTML a mano. Cambios de diseño: siempre vista previa antes de publicar.
- Títulos y orden en cada bloque: Apuntes X, Ejercicios X, Boletín ejercicios tipo PAU para clase, Boletín ejercicios
  tipo PAU para casa, Demostraciones; cada soluciones justo detrás de sus ejercicios (ver CLAUDE.md).
- PDF en `pdf/<curso>/<seccion>/` con nombres en minúsculas, sin tildes ni espacios; lo oculto, en `privado/`.
- La web NO va en iCloud: se sincroniza entre Macs con GitHub (`git pull` al empezar, `git push` al terminar).
- ESTADO.md y BITACORA.md están en el repositorio público: nada privado ni datos de alumnos.
- Commits firmados como «Jorge Pérez Vizcaíno» con el correo anónimo de GitHub (no el Gmail).
- Cuando Jorge quiera ver un enlace, abrirlo en Safari (`open -a Safari <url>`).
- Antes de borrar algo que Jorge deja en la carpeta, confirmar qué es: el 2026-11-04 se mandaron por error a la
  Papelera los PDF de Electromagnetismo (se recuperaron).

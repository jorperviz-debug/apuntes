# Web de apuntes de Física y Química

Web de materiales de clase de Jorge Pérez Vizcaíno (IES Don Bosco, Albacete). Jorge es profesor, no programador:
háblale en español, en lenguaje sencillo, y no le pidas que ejecute comandos si puedes hacerlo tú.
Cuando quiera ver una página o un enlace, ábreselo en Safari (`open -a Safari <url>`), no en el navegador interno.

- Repositorio: https://github.com/jorperviz-debug/apuntes
- Web publicada: https://jorperviz-debug.github.io/apuntes/

## Continuidad entre ordenadores

Jorge trabaja desde dos Mac. La web **no** está en iCloud: se sincroniza con GitHub. La memoria interna de Claude no
pasa de un Mac a otro; la fuente de verdad son `ESTADO.md` y `BITACORA.md`, en la raíz del proyecto.

**Al empezar cada sesión (antes de hacer nada):**
1. `git pull`. Si falla (cambios sin subir en este Mac que chocan con los del otro), avisar a Jorge antes de seguir.
2. Leer `ESTADO.md` completo y las 3 últimas entradas de `BITACORA.md`.
3. Si Jorge empieza con «seguimos», «retomamos», «dónde lo dejamos» o sin una tarea concreta: resumirle en 3-5 líneas
   en qué punto estamos, qué quedó pendiente y el siguiente paso, y esperar su confirmación. Si empieza con una tarea
   concreta (p. ej. «sube estos PDF…»), hacerla directamente y mencionar solo lo pendiente que le afecte.

**Al terminar una tarea o cuando diga «cerramos»:**
1. Reescribir `ESTADO.md` (no acumular) con fecha y Mac (`scutil --get ComputerName`).
2. Añadir al final de `BITACORA.md` una entrada con fecha, Mac, qué se hizo y qué quedó a medias.
3. `git add`, `git commit` y `git push`, y confirmarle a Jorge que está guardado y subido.

**Ojo:** el repositorio es público. En `ESTADO.md` y `BITACORA.md` no se escribe nada privado ni datos de alumnos.
No borrar ni mover archivos sin preguntar. Si la bitácora pasa de ~40 entradas, proponer resumir las antiguas.

### Primer uso en otro Mac

Si este Mac todavía no tiene la web (Jorge dirá algo como «descarga mi web de github.com/jorperviz-debug/apuntes»):
1. Preguntar en qué carpeta la quiere (fuera de iCloud) y hacer
   `git clone https://github.com/jorperviz-debug/apuntes.git` ahí (es público: no hace falta iniciar sesión).
2. Configurar la firma en el repositorio: `git config user.name "Jorge Pérez Vizcaíno"` y
   `git config user.email "288128699+jorperviz-debug@users.noreply.github.com"` (nunca el Gmail).
3. Instalar `gh` sin tocar el sistema, pidiendo permiso a Jorge antes de descargar: bajar el zip `macOS_arm64` (o
   `amd64` si `uname -m` dice `x86_64`) de la última versión en github.com/cli/cli/releases, comprobar su suma con
   el archivo `checksums.txt` de esa versión y copiar `bin/gh` a `~/.local/bin/gh`.
4. `~/.local/bin/gh auth login --hostname github.com --git-protocol https --web --scopes workflow` en segundo plano:
   darle a Jorge el código y el enlace https://github.com/login/device, explicarle que lo abra en Safari, escriba el
   código y pulse «Authorize». Comprobar que entra como `jorperviz-debug`. Después `~/.local/bin/gh auth setup-git`.
5. `python3 build.py` para comprobar que todo funciona, y actualizar `ESTADO.md` y `BITACORA.md`.

## Cómo funciona

Las páginas HTML **no se editan a mano**: se generan a partir de un único archivo de datos.

| Archivo | Qué es |
|---|---|
| `cursos.json` | **Todo el contenido**: datos del sitio, cursos, secciones (temas) y materiales. Es lo único que se toca para añadir o cambiar materiales. |
| `pdf/<curso>/<seccion>/` | PDF guardados en el proyecto. Una carpeta por curso y por sección (tema). |
| `build.py` | Genera la web en `_site/` (portada, una página por curso, `style.css` y `pdf/`). Solo usa Python estándar (3.9+). |
| `style.css` | Diseño. No cambiarlo salvo que Jorge lo pida. |
| `.github/workflows/pages.yml` | Al hacer `git push` a `main`, GitHub ejecuta `build.py` y publica `_site/` en GitHub Pages (1–2 minutos). |

`_site/` está en `.gitignore`: nunca se sube. Para ver el resultado en local: `python3 build.py` y abrir `_site/index.html`.

## Formato de `cursos.json`

```jsonc
{
  "sitio": { "titulo", "descripcion", "autor", "correo", "departamento" },
  "cursos": [                       // el orden es el de la portada y el menú
    {
      "id": "2-eso",                // nombre de la página (2-eso.html) y de la carpeta pdf/2-eso/
      "nombre": "2.º ESO",
      "materia": "Física y Química",
      "simbolo": "2E",              // letras grandes de la casilla
      "etiqueta": "ESO",            // texto pequeño de la casilla en la página del curso
      "color": "eso",               // eso | bach1 | bach2 | fpb (colores definidos en style.css)
      "secciones": [
        {
          "id": "tema-4",           // nombre de la carpeta pdf/2-eso/tema-4/
          "titulo": "Tema 4: Fuerzas y movimiento",
          "descripcion": "…",       // opcional, texto gris bajo el título
          "externos": true,         // opcional: recursos de otros profesores; no cuentan en "N materiales"
          "materiales": [
            { "tipo": "Apuntes", "titulo": "Fuerzas", "archivo": "apuntes-fuerzas.pdf" },
            { "tipo": "Ejercicios", "titulo": "Fuerzas", "enlace": "https://drive.google.com/…", "nota": "Sin actualizar" }
          ]
        }
      ]
    }
  ]
}
```

- Cada material lleva `"archivo"` (PDF dentro de `pdf/<curso>/<seccion>/`) **o** `"enlace"` (URL externa, p. ej. Google Drive).
- `"nota"` es opcional (texto pequeño a la derecha).
- Una sección con `"materiales": []` muestra «Pendiente · En construcción».
- Tipos usados: Apuntes, Ejercicios, Soluciones, Presentación, Formulario, Guías, Resúmenes. Se puede usar otro (Examen, Práctica…).
- Cursos especiales: `"proximamente": true` muestra la casilla en gris sin página; un curso con `"enlace"` o `"archivo"`
  a nivel de curso (como FP Básica) no tiene página: la casilla abre directamente ese PDF (`pdf/<curso>/<archivo>`).
- El número «N materiales» de la portada se calcula solo.
- Todos los PDF de Jorge están ya en `pdf/` (se pasaron desde Google Drive el 2026-10-03). Solo siguen como `"enlace"`
  los recursos externos de otros profesores. Si Jorge da un enlace de Drive suyo, descargar el PDF (con su permiso) y
  usar `"archivo"`.

## Receta: «sube estos PDF a 3.º ESO, tema 4»

1. `git pull` y leer `ESTADO.md` (ver «Continuidad entre ordenadores»).
2. **Curso.** Buscar en `cursos.json` el curso (`id` tipo `3-eso`). Si no existe, crearlo en su sitio (orden por nivel:
   ESO → Bachillerato → FP), p. ej. `id "3-eso"`, `nombre "3.º ESO"`, `simbolo "3E"`, `etiqueta "ESO"`, `color "eso"`
   (Bachillerato: `bach1`/`bach2`; FP: `fpb`). Si estaba como `"proximamente"`, quitar esa línea.
3. **Sección.** Buscar la sección `tema-4`. Si no existe, crearla con `"titulo": "Tema 4: <nombre del tema>"`,
   ordenada entre los demás temas. Si Jorge no dice el nombre del tema, deducirlo del PDF (portada o primer título).
4. **Archivos.** Copiar los PDF a `pdf/3-eso/tema-4/` con nombres limpios: minúsculas, sin tildes ni espacios,
   con guiones (`ejercicios-fuerzas.pdf`). Comprobar el tamaño: GitHub rechaza archivos de más de 100 MB y avisa a partir
   de 50 MB; si alguno es enorme, avisar a Jorge antes de subirlo.
5. **Materiales.** Añadir una entrada por PDF con `tipo`, `titulo` y `archivo`. Deducir tipo y título del nombre del
   archivo y de su contenido (leer la primera página). Si hay soluciones, ponerlas después de los ejercicios.
6. `python3 build.py` (debe terminar sin «ERROR») y comprobar en `_site/` que la página queda bien.
7. **Publicar.** «Sube» incluye publicar: `git add`, `git commit` con un mensaje en español
   («3.º ESO, tema 4: añade apuntes y ejercicios de fuerzas») y `git push`. Si has tenido que adivinar algo dudoso
   (tipo, título o nombre del tema), enséñaselo a Jorge y espera su visto bueno antes del push.
8. Comprobar que la publicación ha terminado bien (`gh run watch` o la pestaña Actions del repositorio) y darle a Jorge
   el enlace de la página del curso.
9. Actualizar `ESTADO.md` y `BITACORA.md`, commit y push.

## Otras tareas habituales

- **Corregir un título o enlace:** editar la entrada en `cursos.json`, `python3 build.py`, commit y push.
- **Quitar un material:** borrar su entrada en `cursos.json` y su PDF de `pdf/`.
- **Cambiar textos del pie o la portada:** bloque `"sitio"` de `cursos.json`.
- **Cambiar el diseño o la estructura del HTML:** `style.css` o las plantillas de `build.py` (solo si Jorge lo pide).

## Herramientas en este Mac

- `git` y `python3` vienen con macOS.
- `gh` (GitHub CLI) está en `~/.local/bin/gh` (no está en el PATH: usar la ruta completa). Cuenta: `jorperviz-debug`.
  Si no existe en este Mac, seguir «Primer uso en otro Mac». Si la sesión caduca, repetir el paso 4 de esa sección.

#!/usr/bin/env python3
"""Genera la web a partir de cursos.json.

Uso:  python3 build.py
Crea la carpeta _site/ con index.html, una página por curso, style.css y los PDF.
GitHub lo ejecuta automáticamente en cada subida (.github/workflows/pages.yml).
Solo usa la biblioteca estándar de Python (3.9 o posterior).
"""
import json
import shutil
import sys
from html import escape
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "cursos.json"
PDF = RAIZ / "pdf"
SALIDA = RAIZ / "_site"

FAVICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
           "<text y='.9em' font-size='90'>⚛️</text></svg>")
FUENTES = ("https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700"
           "&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&display=swap")


class ErrorDatos(Exception):
    pass


def e(texto):
    return escape(str(texto), quote=True)


def ruta_pdf(*partes):
    """Ruta relativa (para el enlace) de un archivo dentro de pdf/, comprobando que existe."""
    archivo = PDF.joinpath(*partes)
    if not archivo.is_file():
        raise ErrorDatos("No existe el archivo %s" % archivo.relative_to(RAIZ))
    return quote("/".join(("pdf",) + partes))


def tiene_pagina(curso):
    return not curso.get("proximamente") and not (curso.get("enlace") or curso.get("archivo"))


def contar(curso):
    return sum(len(s["materiales"]) for s in curso["secciones"] if not s.get("externos"))


# ---------- Plantilla común ----------

def pagina(sitio, cursos, titulo, actual, cuerpo):
    nav = ['      <a href="index.html"%s>Inicio</a>' % (' aria-current="page"' if actual == "index" else "")]
    for c in cursos:
        if tiene_pagina(c):
            marca = ' aria-current="page"' if actual == c["id"] else ""
            nav.append('      <a href="%s.html"%s>%s</a>' % (e(c["id"]), marca, e(c["nombre"])))
    return """<!DOCTYPE html>
<html lang="es">
<head>
<title>{titulo}</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fuentes}" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<link rel="icon" href="{favicon}">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html">{sitio_titulo}</a>
    <nav>
{nav}
    </nav>
  </div>
</header>
{cuerpo}
<footer>
  <div class="wrap">
    <p>{autor}</p>
    <p><a href="mailto:{correo}">{correo}</a></p>
    <p>{departamento}</p>
  </div>
</footer>
</body>
</html>
""".format(
        titulo=e(titulo), fuentes=FUENTES, favicon=FAVICON, sitio_titulo=e(sitio["titulo"]),
        nav="\n".join(nav), cuerpo=cuerpo, autor=e(sitio["autor"]), correo=e(sitio["correo"]),
        departamento=e(sitio["departamento"]),
    )


# ---------- Portada ----------

def casilla(curso):
    pie = '<span class="pie"><span class="nom">%s</span><br><span class="sub">%s</span></span>' % (
        e(curso["nombre"]), e(curso["materia"]))
    if curso.get("proximamente"):
        abre, cierra, n = '<div class="el %s off">' % e(curso["color"]), "</div>", "Próximamente"
    else:
        if tiene_pagina(curso):
            href, extra = "%s.html" % e(curso["id"]), ""
            total = contar(curso)
            n = "%d %s" % (total, "material" if total == 1 else "materiales")
        else:
            if curso.get("archivo"):
                href = ruta_pdf(curso["id"], curso["archivo"])
            else:
                href = e(curso["enlace"])
            extra = ' target="_blank" rel="noopener"'
            n = curso.get("texto_casilla", "Apuntes (PDF)")
        abre, cierra = '<a class="el %s" href="%s"%s>' % (e(curso["color"]), href, extra), "</a>"
    return """    {abre}
      <span class="n">{n}</span>
      <span class="sim">{sim}</span>
      {pie}
    {cierra}""".format(abre=abre, n=e(n), sim=e(curso["simbolo"]), pie=pie, cierra=cierra)


def portada(sitio, cursos):
    cuerpo = """<main class="wrap">
  <section class="hero">
    <h1>{titulo}</h1>
    <p>{descripcion}</p>
  </section>

  <section class="tabla" aria-label="Cursos">
{casillas}
  </section>
</main>""".format(titulo=e(sitio["titulo"]), descripcion=e(sitio["descripcion"]),
                  casillas="\n".join(casilla(c) for c in cursos))
    return pagina(sitio, cursos, sitio["titulo"], "index", cuerpo)


# ---------- Página de curso ----------

def fila(curso, seccion, m):
    if m.get("archivo"):
        href = ruta_pdf(curso["id"], seccion["id"], m["archivo"])
    elif m.get("enlace"):
        href = e(m["enlace"])
    else:
        raise ErrorDatos('El material "%s" (%s, %s) no tiene "enlace" ni "archivo"'
                         % (m.get("titulo"), curso["id"], seccion["id"]))
    nota = '<span class="nota">%s</span>' % e(m["nota"]) if m.get("nota") else "<span></span>"
    return ('      <li><a href="%s" target="_blank" rel="noopener"><span class="tipo">%s</span>'
            '<span class="t">%s</span>%s</a></li>' % (href, e(m["tipo"]), e(m["titulo"]), nota))


def bloque(curso, seccion):
    lineas = ['  <section class="bloque">', "    <h2>%s</h2>" % e(seccion["titulo"])]
    if seccion.get("descripcion"):
        lineas.append("    <p>%s</p>" % e(seccion["descripcion"]))
    lineas.append('    <ul class="lista">')
    if seccion["materiales"]:
        lineas += [fila(curso, seccion, m) for m in seccion["materiales"]]
    else:
        lineas.append('      <li><span class="pend"><span class="tipo">Pendiente</span>'
                      '<span>En construcción</span><span></span></span></li>')
    lineas += ["    </ul>", "  </section>"]
    return "\n".join(lineas)


def pagina_curso(sitio, cursos, curso):
    cuerpo = """<main class="wrap {color}">
  <div class="curso">
    <div class="el {color}" aria-hidden="true"><span class="n">{etiqueta}</span><span class="sim">{sim}</span><span></span></div>
    <div><h1>{nombre}</h1><p>{materia}</p></div>
  </div>
{bloques}
</main>""".format(color=e(curso["color"]), etiqueta=e(curso["etiqueta"]), sim=e(curso["simbolo"]),
                  nombre=e(curso["nombre"]), materia=e(curso["materia"]),
                  bloques="\n".join(bloque(curso, s) for s in curso["secciones"]))
    titulo = "%s | %s" % (curso["nombre"], sitio["titulo"])
    return pagina(sitio, cursos, titulo, curso["id"], cuerpo)


# ---------- Comprobaciones y construcción ----------

def comprobar(datos):
    ids = set()
    for c in datos["cursos"]:
        for campo in ("id", "nombre", "materia", "simbolo", "etiqueta", "color", "secciones"):
            if campo not in c:
                raise ErrorDatos('Al curso "%s" le falta el campo "%s"' % (c.get("id", "?"), campo))
        if c["id"] in ids or c["id"] == "index":
            raise ErrorDatos('El id de curso "%s" está repetido o no es válido' % c["id"])
        ids.add(c["id"])
        secciones = set()
        for s in c["secciones"]:
            for campo in ("id", "titulo", "materiales"):
                if campo not in s:
                    raise ErrorDatos('A una sección de "%s" le falta el campo "%s"' % (c["id"], campo))
            if s["id"] in secciones:
                raise ErrorDatos('La sección "%s" está repetida en "%s"' % (s["id"], c["id"]))
            secciones.add(s["id"])
            for m in s["materiales"]:
                for campo in ("tipo", "titulo"):
                    if campo not in m:
                        raise ErrorDatos('A un material de %s/%s le falta "%s"' % (c["id"], s["id"], campo))


def construir():
    try:
        datos = json.loads(DATOS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise ErrorDatos("cursos.json tiene un error de formato en la línea %d, columna %d: %s"
                         % (err.lineno, err.colno, err.msg))
    comprobar(datos)
    sitio, cursos = datos["sitio"], datos["cursos"]

    paginas = {"index.html": portada(sitio, cursos)}
    for c in cursos:
        if tiene_pagina(c):
            paginas["%s.html" % c["id"]] = pagina_curso(sitio, cursos, c)
        elif c.get("archivo"):
            ruta_pdf(c["id"], c["archivo"])

    if SALIDA.exists():
        shutil.rmtree(SALIDA)
    SALIDA.mkdir()
    for nombre, html in paginas.items():
        (SALIDA / nombre).write_text(html, encoding="utf-8")
    shutil.copy2(RAIZ / "style.css", SALIDA / "style.css")
    if PDF.exists():
        shutil.copytree(PDF, SALIDA / "pdf", ignore=shutil.ignore_patterns(".gitkeep", ".DS_Store"))
    print("Web generada en _site/: %s" % ", ".join(paginas))


if __name__ == "__main__":
    try:
        construir()
    except ErrorDatos as err:
        sys.exit("ERROR: %s" % err)

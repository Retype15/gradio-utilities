from my_library.utils import collect_included_files
import os

# Ruta base del proyecto
root_dir = os.path.dirname(os.path.realpath(__file__))

# Archivos y directorios a incluir
includes = [
    "main.py",
    "config/",
]

# Llamada a la función
files = collect_included_files(
    root_dir,
    includes,
    output_json="archivos_incluidos.json",
    verbose=True,
    recursive=True,
    include_extensions=[".py", ".json"],
    exclude=[".env"]
)

print("Archivos recolectados:", files)

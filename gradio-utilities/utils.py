import os
import json
from typing import List, Dict, Optional, Union


def collect_included_files(
    root_dir: str,
    includes: List[str],
    output_json: Optional[str] = None,
    verbose: bool = False,
    recursive: bool = True,
    include_extensions: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None
) -> Dict[str, str]:
    """
    Recopila el contenido de archivos especificados o de directorios en `includes`, con opciones avanzadas de filtro.

    Args:
        root_dir (str): Ruta base desde donde buscar los archivos o directorios.
        includes (List[str]): Lista de rutas relativas a archivos o directorios dentro de `root_dir`.
        output_json (Optional[str]): Ruta para guardar los resultados en un archivo JSON. Si es None, no guarda.
        verbose (bool): Si es True, muestra mensajes detallados de errores y progreso.
        recursive (bool): Si es True, busca archivos de forma recursiva en directorios.
        include_extensions (Optional[List[str]]): Lista de extensiones de archivo permitidas (por ejemplo, ['.py', '.json']).
        exclude (Optional[List[str]]): Lista de archivos o patrones de ruta a excluir.

    Returns:
        Dict[str, str]: Diccionario donde las claves son las rutas relativas de los archivos y los valores son su contenido.
    """
    files_dict = {}

    for include in includes:
        full_path = os.path.join(root_dir, include)

        if os.path.isfile(full_path):  # Si es un archivo
            if _should_include_file(include, include_extensions, exclude):
                _read_file_to_dict(full_path, include, files_dict, verbose)

        elif os.path.isdir(full_path):  # Si es un directorio
            for dirpath, _, filenames in os.walk(full_path):
                for filename in filenames:
                    relative_path = os.path.relpath(os.path.join(dirpath, filename), root_dir)
                    if _should_include_file(relative_path, include_extensions, exclude):
                        _read_file_to_dict(os.path.join(dirpath, filename), relative_path, files_dict, verbose)

                if not recursive:  # Si no es recursivo, detén la búsqueda en subdirectorios
                    break
        else:
            if verbose:
                print(f"Ruta no válida o inexistente: {include}")

    if output_json:
        try:
            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump(files_dict, f, ensure_ascii=False, indent=4)
            if verbose:
                print(f"Datos guardados en {output_json}")
        except Exception as e:
            if verbose:
                print(f"Error al guardar el JSON en {output_json}: {e}")

    return files_dict


def _should_include_file(file_path: str, include_extensions: Optional[List[str]], exclude: Optional[List[str]]) -> bool:
    """
    Evalúa si un archivo debe incluirse según los filtros de extensión y exclusión.

    Args:
        file_path (str): Ruta relativa del archivo.
        include_extensions (Optional[List[str]]): Extensiones permitidas.
        exclude (Optional[List[str]]): Patrones o rutas excluidas.

    Returns:
        bool: True si el archivo debe incluirse, False si no.
    """
    if exclude and any(ex in file_path for ex in exclude):
        return False

    if include_extensions and not any(file_path.endswith(ext) for ext in include_extensions):
        return False

    return True


def _read_file_to_dict(full_path: str, relative_path: str, files_dict: Dict[str, str], verbose: bool) -> None:
    """
    Lee el contenido de un archivo y lo agrega al diccionario.

    Args:
        full_path (str): Ruta completa al archivo.
        relative_path (str): Ruta relativa del archivo desde `root_dir`.
        files_dict (Dict[str, str]): Diccionario donde se almacenará el contenido del archivo.
        verbose (bool): Si es True, muestra mensajes de progreso.
    """
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        files_dict[relative_path] = content
        if verbose:
            print(f"Archivo leído correctamente: {relative_path}")
    except Exception as e:
        if verbose:
            print(f"Error al leer el archivo {relative_path}: {e}")

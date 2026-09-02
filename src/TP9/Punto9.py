"""
Punto9.py

Programa para evaluar un dataset histórico de proyectos de software
mediante correlación por cuadrados mínimos.  Ajusta dos modelos de
estimación de esfuerzo a partir de la complejidad (LOC):

    Modelo lineal:       E = a * LOC + b
    Modelo exponencial:  E = k * LOC^b    (ajustado por regresión OLS
                                            sobre las variables log-transformadas)

Los datos históricos se cargan desde un archivo JSON externo cuya ruta
se indica por línea de comandos (por defecto: dataset.json en el mismo
directorio que el script).

Requisitos:
    pip install numpy pandas matplotlib statsmodels

Uso:
    python Punto9.py -l              # solo modelo lineal
    python Punto9.py -x              # solo modelo exponencial
    python Punto9.py -l -x           # ambos modelos
    python Punto9.py -l --dataset otro.json
"""

import argparse
import json
import os
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import statsmodels.api as sm


# ---------------------------------------------------------------------------
# Configuración del backend gráfico (cross-platform)
# ---------------------------------------------------------------------------

def _configurar_backend_interactivo() -> None:
    """
    Intenta seleccionar un backend interactivo de matplotlib para poder
    mostrar los gráficos en pantalla con plt.show().

    Se prueban varios backends comunes en orden de preferencia, cubriendo
    los más habituales en Linux, macOS y Windows.  Para cada candidato se
    verifica que su módulo pueda importarse realmente (matplotlib.use() por
    sí solo no garantiza que el backend funcione, ya que la importación
    real se difiere hasta el primer uso de pyplot).

    Si ningún backend interactivo está disponible, el script termina con un
    mensaje que indica cómo instalar uno.
    """
    from matplotlib.backends.registry import BackendRegistry

    registry = BackendRegistry()

    # Orden de preferencia: Qt → Tk → GTK → macOS nativo
    candidatos = ("QtAgg", "Qt5Agg", "TkAgg", "GTK3Agg", "GTK4Agg", "macosx")

    for backend in candidatos:
        try:
            # Verificar que el módulo del backend realmente puede importarse
            registry.load_backend_module(backend)
            matplotlib.use(backend)
            return
        except (ImportError, ModuleNotFoundError):
            continue

    sys.exit(
        "No se encontró un backend gráfico interactivo.\n"
        "Instalá alguno de los siguientes para poder ver los gráficos:\n"
        "  Linux:   sudo apt-get install python3-tk\n"
        "  macOS:   brew install python-tk\n"
        "  Cualquier SO: pip install PyQt5"
    )


_configurar_backend_interactivo()

import matplotlib.pyplot as plt  # noqa: E402  (import tras configurar el backend)


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

VERSION = "1.0"
"""Versión del script."""


# ---------------------------------------------------------------------------
# Carga de datos
# ---------------------------------------------------------------------------

def cargar_dataset(ruta: str) -> pd.DataFrame:
    """
    Lee un archivo JSON con el dataset histórico y lo convierte en un
    DataFrame de pandas con columnas 'LOC' y 'Esfuerzo'.

    El JSON esperado tiene la estructura::

        {
            "datos": [
                { "loc": 1000, "esfuerzo_pm": 2 },
                ...
            ]
        }

    Args:
        ruta: Ruta (absoluta o relativa) al archivo JSON del dataset.

    Returns:
        pd.DataFrame con columnas ``LOC`` (int/float) y ``Esfuerzo`` (float).

    Raises:
        SystemExit: Si el archivo no existe o el formato es inválido.
    """
    ruta_path = Path(ruta)

    if not ruta_path.is_file():
        sys.exit(f"Error: no se encontró el archivo de dataset '{ruta}'.")

    try:
        with open(ruta_path, encoding="utf-8") as f:
            contenido = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        sys.exit(f"Error al leer '{ruta}': {e}")

    # Validar estructura mínima
    if "datos" not in contenido or not isinstance(contenido["datos"], list):
        sys.exit(
            f"Error: el archivo '{ruta}' no tiene la estructura esperada.\n"
            "Se espera un objeto JSON con una clave 'datos' que contenga "
            "una lista de objetos con 'loc' y 'esfuerzo_pm'."
        )

    registros = contenido["datos"]
    df = pd.DataFrame({
        "LOC": [r["loc"] for r in registros],
        "Esfuerzo": [r["esfuerzo_pm"] for r in registros],
    })

    return df


# ---------------------------------------------------------------------------
# Modelos de correlación
# ---------------------------------------------------------------------------

def ajustar_modelo_lineal(df: pd.DataFrame) -> tuple[float, float, float]:
    """
    Ajusta un modelo lineal  E = a * LOC + b  por cuadrados mínimos
    (numpy polyfit) y calcula el coeficiente de determinación R².

    Args:
        df: DataFrame con columnas 'LOC' y 'Esfuerzo'.

    Returns:
        Tupla (a, b, r_squared) donde *a* es la pendiente, *b* la
        ordenada al origen y *r_squared* el R² del ajuste.
    """
    a, b = np.polyfit(df["LOC"], df["Esfuerzo"], 1)

    # Coeficiente de determinación R²
    r_matrix = np.corrcoef(df["LOC"], df["Esfuerzo"])
    r_squared = r_matrix[0, 1] ** 2

    return a, b, r_squared


def ajustar_modelo_exponencial(df: pd.DataFrame) -> tuple[float, float, float]:
    """
    Ajusta un modelo exponencial  E = k * LOC^b  mediante regresión OLS
    sobre las variables log-transformadas:

        log(E) = log(k) + b * log(LOC)

    Args:
        df: DataFrame con columnas 'LOC' y 'Esfuerzo'.

    Returns:
        Tupla (k, b, r_squared) donde *k* es el coeficiente
        multiplicativo, *b* el exponente y *r_squared* el R² del ajuste
        OLS en escala logarítmica.
    """
    log_loc = np.log(df["LOC"])
    log_esfuerzo = np.log(df["Esfuerzo"])

    # Regresión OLS con constante (intercepto)
    X = sm.add_constant(log_loc)
    modelo = sm.OLS(log_esfuerzo, X).fit()

    # Recuperar parámetros en escala original
    k = np.exp(modelo.params.iloc[0])   # exp(intercepto)
    b = modelo.params.iloc[1]           # pendiente = exponente

    return k, b, modelo.rsquared


# ---------------------------------------------------------------------------
# Graficación
# ---------------------------------------------------------------------------

def graficar_resultados(
    df: pd.DataFrame,
    lineal: tuple[float, float, float] | None = None,
    exponencial: tuple[float, float, float] | None = None,
) -> None:
    """
    Genera un gráfico con los datos históricos y, opcionalmente, las curvas
    de los modelos lineal y/o exponencial ajustados.

    Args:
        df: DataFrame con columnas 'LOC' y 'Esfuerzo'.
        lineal: Tupla (a, b, r²) del modelo lineal, o None si no se ajustó.
        exponencial: Tupla (k, b, r²) del modelo exponencial, o None.
    """
    plt.figure(figsize=(9, 6))

    # Datos históricos como dispersión
    plt.scatter(
        df["LOC"], df["Esfuerzo"],
        label="Datos históricos", zorder=5, edgecolors="black",
    )

    # Rango suave de LOC para dibujar las curvas
    loc_curva = np.linspace(df["LOC"].min(), df["LOC"].max(), 500)

    if lineal is not None:
        a, b, r2 = lineal
        etiqueta = f"Modelo lineal (R²={r2:.4f})"
        plt.plot(loc_curva, a * loc_curva + b, label=etiqueta, color="red", linewidth=2)

    if exponencial is not None:
        k, b_exp, r2 = exponencial
        etiqueta = f"Modelo exponencial (R²={r2:.4f})"
        plt.plot(loc_curva, k * (loc_curva ** b_exp), label=etiqueta, color="green", linewidth=2)

    plt.title("Esfuerzo vs. Complejidad (LOC) — Dataset histórico")
    plt.xlabel("Complejidad [LOC]")
    plt.ylabel("Esfuerzo [persona-mes]")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Argumentos de línea de comandos
# ---------------------------------------------------------------------------

def parsear_argumentos() -> argparse.Namespace:
    """
    Define y parsea los argumentos de línea de comandos del script.

    Argumentos soportados:
        -v, --version      Muestra la versión del programa y sale.
        -l, --linear       Activa el ajuste del modelo lineal.
        -x, --exponential  Activa el ajuste del modelo exponencial.
        --dataset RUTA     Ruta al archivo JSON del dataset
                           (default: dataset.json junto al script).

    Returns:
        argparse.Namespace con los valores de los argumentos parseados.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Evalúa un dataset histórico de proyectos de software ajustando "
            "modelos de estimación de esfuerzo (lineal y/o exponencial) "
            "por correlación de cuadrados mínimos."
        )
    )
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Muestra la versión del programa y sale.",
    )
    parser.add_argument(
        "-l", "--linear",
        action="store_true",
        help="Ajustar modelo lineal E = a*LOC + b.",
    )
    parser.add_argument(
        "-x", "--exponential",
        action="store_true",
        help="Ajustar modelo exponencial E = k * LOC^b.",
    )

    # Ruta por defecto: dataset.json en el mismo directorio que el script
    dataset_default = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.json")
    parser.add_argument(
        "--dataset",
        type=str,
        default=dataset_default,
        help=f"Ruta al archivo JSON del dataset (default: {dataset_default}).",
    )

    return parser.parse_args()


# ---------------------------------------------------------------------------
# Función principal
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Función principal: procesa argumentos, carga el dataset, ajusta los
    modelos solicitados, imprime los resultados numéricos por consola y
    muestra el gráfico comparativo en pantalla.
    """
    args = parsear_argumentos()

    # Mostrar versión y salir si se pidió
    if args.version:
        print(f"Programa {sys.argv[0]} versión {VERSION}")
        sys.exit(0)

    # Verificar que se seleccionó al menos un modelo
    if not args.linear and not args.exponential:
        print(f"Programa {sys.argv[0]} versión {VERSION}")
        print("Debe indicar modelo lineal (-l) o exponencial (-x) o ambos.")
        sys.exit(1)

    # Cargar dataset desde el archivo JSON
    df = cargar_dataset(args.dataset)

    # Calcular y mostrar la correlación general entre LOC y Esfuerzo
    correlacion = df["LOC"].corr(df["Esfuerzo"])
    print(f"Correlación LOC-Esfuerzo: {correlacion:.4f}")

    resultado_lineal = None
    resultado_exponencial = None

    # Ajuste del modelo lineal
    if args.linear:
        a, b, r2 = ajustar_modelo_lineal(df)
        resultado_lineal = (a, b, r2)
        print(f"Modelo lineal E = {b:.6f} + {a:.6f} * LOC")
        print(f"  R² = {r2:.4f}")

    # Ajuste del modelo exponencial
    if args.exponential:
        k, b_exp, r2 = ajustar_modelo_exponencial(df)
        resultado_exponencial = (k, b_exp, r2)
        print(f"Modelo exponencial E = {k:.6f} * LOC^{b_exp:.6f}")
        print(f"  R² = {r2:.4f}")

    # Graficar datos y modelos ajustados
    graficar_resultados(df, lineal=resultado_lineal, exponencial=resultado_exponencial)


if __name__ == "__main__":
    main()

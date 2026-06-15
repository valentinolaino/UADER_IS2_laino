# ==========================================================
# Archivo: getJson.py
# Autores:
#       Laiño Valentino
#       Mout Santiago
#       Sandillú Axel
#
# copyright UADERFCyT-IS2©2026 todos los derechos reservados
# ==========================================================

"""
Módulo de reingeniería para la automatización y balanceo de pagos.
Implementa patrones de diseño: Singleton, Chain of Responsibility e Iterator.
Versión: 1.2
"""

import json
import sys
from abc import ABC, abstractmethod
from typing import List, Optional

VERSION = "1.2"


# =====================================================================
# LA CLASE ABSTRACTA (Interfaz Base del Procesador)
# =====================================================================
class ProcesadorJSON(ABC):
    """
    Interfaz que define cómo debe interactuar el cliente con las
    diferentes implementaciones del procesador.
    """

    @abstractmethod
    def procesar(self, argv: list):
        """Método abstracto principal de ejecución.

        Args:
            argv (list): Lista de argumentos de la línea de comandos.
        """
        pass


# =====================================================================
# EL COMPONENTE COMPLEMENTARIO (Singleton - Lector de Configuración)
# =====================================================================
class LectorNuevo(ProcesadorJSON):
    """
    Lector de configuración JSON bajo el patrón Singleton.
    Mapea de forma única la relación entre bancos (tokens) y sus claves.
    """

    _instancia = None

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:
            cls._instancia = super(LectorNuevo, cls).__new__(cls)
            cls._instancia.datos_json = {}
        return cls._instancia

    def cargar_json(self, jsonfile: str):
        """Carga el archivo de configuración JSON.

        Args:
            jsonfile (str): Ruta del archivo de configuración.
        """
        try:
            with open(jsonfile, "r", encoding="utf-8") as myfile:
                self.datos_json = json.load(myfile)
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo '{jsonfile}'.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: El archivo '{jsonfile}' no es un JSON válido.")
            sys.exit(1)

    def obtener_clave(self, token: str) -> str:
        """Devuelve la clave asociada a un token o banco.

        Args:
            token (str): Identificador del banco.

        Returns:
            str: Clave criptográfica o token de acceso.
        """
        return self.datos_json.get(token, "Clave no encontrada")

    def procesar(self, argv: list):
        """Cumple con la interfaz, inicializando la lectura del archivo."""
        self.cargar_json(argv[1])


# =====================================================================
# PATRÓN ITERATOR (Estructura para el listado cronológico de pagos)
# =====================================================================
class PagoDTO:
    """Objeto de transferencia de datos que representa un pago realizado."""

    def __init__(self, numero_pedido: int, token: str, monto: float):
        self.numero_pedido = numero_pedido
        self.token = token
        self.monto = monto

    def __str__(self) -> str:
        return f"Pedido N°: {self.numero_pedido} | Banco/Token: {self.token} | Monto: ${self.monto:.2f}"


class PagosIterator:
    """Iterador concreto para recorrer el historial de pagos cronológicamente."""

    def __init__(self, pagos: List[PagoDTO]):
        self._pagos = pagos
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> PagoDTO:
        if self._index < len(self._pagos):
            pago = self._pagos[self._index]
            self._index += 1
            return pago
        raise StopIteration


class RegistroPagos:
    """Colección iterable que almacena el historial cronológico de pagos."""

    def __init__(self):
        self._historial: List[PagoDTO] = []

    def registrar(self, pago: PagoDTO):
        """Añade un nuevo pago realizado al registro."""
        self._historial.append(pago)

    def __iter__(self) -> PagosIterator:
        return PagosIterator(self._historial)


# =====================================================================
# PATRÓN CHAIN OF RESPONSIBILITY (Manejo Balanceado y Automático de Cuentas)
# =====================================================================
class CuentaHandler(ABC):
    """Manejador abstracto de la cadena de cuentas de pago."""

    def __init__(self, token: str, saldo_inicial: float, lector: LectorNuevo):
        self.token = token
        self.saldo = saldo_inicial
        self.lector = lector
        self.siguiente: Optional[CuentaHandler] = None

    def establecer_siguiente(self, siguiente_handler: "CuentaHandler") -> "CuentaHandler":
        """Define el siguiente eslabón de la cadena."""
        self.siguiente = siguiente_handler
        return siguiente_handler

    @abstractmethod
    def procesar_pago(
        self, numero_pedido: int,
        monto: float, turno_token: str,
        registro: RegistroPagos
        ) -> bool:
        """Intenta procesar la transacción según las reglas de balanceo y saldo."""
        pass


class CuentaBancariaConcreta(CuentaHandler):
    """Eslabón específico que administra el saldo y lógica de un token/banco particular."""

    def procesar_pago(
            self, numero_pedido: int,
            monto: float, turno_token: str,
            registro: RegistroPagos
            ) -> bool:
        # Criterio 1: Validar si es el turno asignado por balanceo yposee saldo suficiente
        if self.token == turno_token and self.saldo >= monto:
            return self._ejecutar_debito(numero_pedido, monto, registro)

        # Criterio 2: Forzar procesamiento si la otra cuenta del turno carece de
        # saldo pero esta sí posee
        if self.saldo >= monto and (self.siguiente is None or not self._verificar_saldo_en_cadena(turno_token, monto)):
            return self._ejecutar_debito(numero_pedido, monto, registro)

        # Criterio 3: Derivar la solicitud al siguiente eslabón de la cadena
        if self.siguiente is not None:
            return self.siguiente.procesar_pago(numero_pedido, monto, turno_token, registro)

        return False

    def _ejecutar_debito(self, numero_pedido: int, monto: float, registro: RegistroPagos) -> bool:
        """Resta el saldo, recupera la clave del Singleton y asienta la operación."""
        self.saldo -= monto
        clave_utilizada = self.lector.obtener_clave(self.token)
        
        # Salida requerida: Número de pedido, token utilizado y monto del pago realizado
        print(f"[TRANSACCIÓN EXITOSA] Pedido: {numero_pedido} | Token: {self.token} (Clave: {clave_utilizada}) | Monto: ${monto:.2f}")
        
        # Guardar en el registro cronológico
        registro.registrar(PagoDTO(numero_pedido, self.token, monto))
        return True

    def _verificar_saldo_en_cadena(self, token_buscado: str, monto: float) -> bool:
        """Recorre la cadena para chequear si el token del turno posee fondos."""
        curr = self
        while curr is not None:
            if curr.token == token_buscado:
                return curr.saldo >= monto
            curr = curr.siguiente
        return False


# =====================================================================
# COMPONENTE CENTRAL DE REINGENIERÍA
# =====================================================================
class SistemaAutomatizadoPagos(ProcesadorJSON):
    """
    Nuevo componente que integra el lector Singleton, configura la cadena
    de cuentas balanceadas y ejecuta simulaciones secuenciales de pago.
    """

    def __init__(self):
        self.lector = LectorNuevo()
        self.registro = RegistroPagos()
        self.cadena_cuentas: Optional[CuentaHandler] = None
        # Control de alternancia estricto ("token1" empieza por defecto)
        self.tokens_disponibles = ["token1", "token2"]
        self.indice_turno = 0

    def inicializar_sistema(self, archivo_config: str):
        """Prepara el pool de datos y configura la infraestructura de cuentas."""
        self.lector.cargar_json(archivo_config)

        # Configuración de las cuentas (Consigna d: token1=$1000, token2=$2000)
        cuenta1 = CuentaBancariaConcreta("token1", 1000.0, self.lector)
        cuenta2 = CuentaBancariaConcreta("token2", 2000.0, self.lector)

        # Ensamblado de la cadena de responsabilidad
        cuenta1.establecer_siguiente(cuenta2)
        self.cadena_cuentas = cuenta1

    def simular_pago(self, numero_pedido: int, monto: float):
        """Determina el turno de balanceo y envía el pedido a la cadena."""
        if not self.cadena_cuentas:
            print("Error: El sistema de cuentas no se ha inicializado.")
            return

        turno_actual_token = self.tokens_disponibles[self.indice_turno]

        # Enviar petición a la cabeza de la cadena
        exito = self.cadena_cuentas.procesar_pago(numero_pedido, monto, turno_actual_token, self.registro)

        if exito:
            # Alternar el turno balanceado para la siguiente solicitud únicamente si hubo éxito
            self.indice_turno = (self.indice_turno + 1) % len(self.tokens_disponibles)
        else:
            print(f"[TRANSACCIÓN RECHAZADA] Pedido {numero_pedido}: Fondos insuficientes en el sistema para afrontar el pago de ${monto:.2f}")

    def mostrar_listado_pagos(self):
        """Muestra de manera cronológica los pagos asentados usando el Iterator."""
        print("\n" + "="*60)
        print("          LISTADO CRONOLÓGICO DE PAGOS REALIZADOS")
        print("="*60)
        
        iterador = iter(self.registro)
        hubo_pagos = False
        for pago in iterador:
            print(pago)
            hubo_pagos = True
            
        if not hubo_pagos:
            print("No se registraron transacciones en este ciclo.")
        print("="*60 + "\n")

    def procesar(self, argv: list):
        """Coordina la simulación de ruteo automatizado solicitada."""
        self.inicializar_sistema(argv[1])

        print(f"Iniciando Sistema Automatizado de Pagos v{VERSION}")
        print("Estrategia: Ruteo Balanceado Automático (Monto por pedido fijo: $500.00)\n")

        # Simulación consecutiva de pedidos de pago de $500.- (Consigna e)
        monto_pedido = 500.0
        for nro_pedido in range(1, 8):  # Se simulan 7 pedidos para agotar fondos controladamente
            self.simular_pago(nro_pedido, monto_pedido)

        # Mostrar el reporte final cronológico empleando el iterador
        self.mostrar_listado_pagos()


# =====================================================================
# EL CLIENTE PRINCIPAL
# =====================================================================
def main():
    """Punto de entrada al programa."""
    if len(sys.argv) < 2:
        print("Uso: python get_jason_poo.py <archivo.json>")
        return

    if "-v" in sys.argv:
        print(f"Versión actual del sistema: {VERSION}")
        return

    # Se ejecuta la nueva solución integrada de reingeniería automatizada
    sistema = SistemaAutomatizadoPagos()
    sistema.procesar(sys.argv)


if __name__ == "__main__":
    main()
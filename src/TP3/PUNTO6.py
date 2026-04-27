

import copy
from abc import ABC, abstractmethod


class Prototype(ABC):
    """Interfaz que define el método de clonación."""

    @abstractmethod
    def clone(self):
        pass


class Documento(Prototype):
    """
    Clase concreta que implementa el patrón Prototype.
    Simula un documento con estructura interna compleja.
    """

    def __init__(self, titulo: str, contenido: str, metadata: dict):
        self.titulo = titulo
        self.contenido = contenido
        self.metadata = metadata  # estructura mutable (clave para el ejemplo)

    def clone(self):
        """
        Devuelve una copia profunda del objeto.
        Se utiliza deepcopy para evitar efectos colaterales.
        """
        return copy.deepcopy(self)

    def __str__(self) -> str:
        return (
            f"Documento:\n"
            f"  Título: {self.titulo}\n"
            f"  Contenido: {self.contenido}\n"
            f"  Metadata: {self.metadata}\n"
        )


def main() -> None:
    # Documento original (prototipo)
    doc_original = Documento(
        titulo="Informe Técnico",
        contenido="Resultados preliminares...",
        metadata={
            "autor": "Dr. Colla",
            "version": 1,
            "tags": ["testing", "calidad"]
        }
    )

    print("=== Documento Original ===")
    print(doc_original)

    # Clonación
    doc_clonado = doc_original.clone()

    # Modificamos el clon
    doc_clonado.titulo = "Informe Técnico - Copia"
    doc_clonado.metadata["version"] = 2
    doc_clonado.metadata["tags"].append("revisión")

    doc_clonado_clonado = doc_clonado.clone()

    doc_clonado_clonado.titulo = "Informe Técnico - Copia de la copia"
    doc_clonado_clonado.metadata["version"] = 3
    doc_clonado_clonado.metadata["tags"].append("segunda revisión")


    print("=== Documento Clonado(Segunda vez) Modificado ===")
    print(doc_clonado_clonado)
    print("=== Documento Clonado  Modificado ===")
    print(doc_clonado)
    print("=== Documento Original (debe permanecer intacto) ===")
    print(doc_original)
    



if __name__ == "__main__":
    main()

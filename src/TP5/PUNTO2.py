from __future__ import annotations
from collections.abc import Iterable, Iterator
from typing import Any

class CharIterator(Iterator):
    """Iterador concreto para recorrer caracteres."""
    
    def __init__(self, char_collection: CharCollection, reverse: bool = False) -> None:
        self._collection = char_collection
        self._reverse = reverse
        # Si es reverso, empezamos desde el último índice
        self._position = (len(self._collection) - 1) if reverse else 0

    def __next__(self) -> str:
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()
        return value

class CharCollection(Iterable):
    """Colección que almacena la cadena de caracteres."""
    
    def __init__(self, string_data: str) -> None:
        self._data = string_data

    def __getitem__(self, index: int) -> str:
        # Permite acceso indexado necesario para el iterador
        if 0 <= index < len(self._data):
            return self._data[index]
        raise IndexError

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> CharIterator:
        return CharIterator(self)

    def get_reverse_iterator(self) -> CharIterator:
        return CharIterator(self, reverse=True)

# Ejemplo de uso
if __name__ == "__main__":
    coleccion = CharCollection("IS2-Iterator")
    
    print("Recorrido directo:")
    print("".join(coleccion))
    
    print("\nRecorrido reverso:")
    print("".join(coleccion.get_reverse_iterator()))
import json
import sys

def getKeys(argv):
    """Obtiene una lista con las claves a buscar.

    Args:
        argv (list): lista de argumentos.

    Returns:
        list: Lista con las claves que dse desean verificar,
        token1 si no se ingresaron claves.
    """
    if (len(argv) <= 2):
        return ["token1"]
    
    keys = []
    for i in range(2, len(sys.argv)):
        keys.append(sys.argv[i])
    return keys;

def getData(jsonfile):
    """Obtiene el objeto de datos a partir del json.

    Args:
        jsonfile (str): Ubicación del archivo json.

    Returns:
        dictionary: Diccionario con los valores de cada clave.
    """
    with open(jsonfile, 'r') as myfile:
        data = myfile.read()

    return json.loads(data)

def printResults(data, keys):
    """Muestra los valoers en pantalla.

    Args:
        data (dictioary): Objeto con todos los valores.
        keys (list): Lista de claves a buscar.
    """
    for key in keys:
        print(str(data[key]))

def main():
    """ Dado un .json y claves a travez de argumentos,
        muestra por terminal los valores de las claves recividas.
    """
    jsonkey = getKeys(sys.argv)
    data = getData(sys.argv[1])
    
    printResults(data, jsonkey)

if __name__ == "__main__":
    main()


import unittest
import tempfile
import json
import os
from unittest.mock import patch
import importlib.util

# Cargar dinámicamente el módulo getJason.py
spec = importlib.util.spec_from_file_location("getJason", "getJason.py")
getJason = importlib.util.module_from_spec(spec)
spec.loader.exec_module(getJason)


class TestGetJason(unittest.TestCase):

    def setUp(self):
        # Crear archivo JSON temporal para pruebas
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            delete=False,
            suffix='.json'
        )

        self.test_data = {
            "token1": "C598-ECF9-F0F7-881A",
            "token2": "C598-ECF9-F0F7-881B"
        }

        json.dump(self.test_data, self.temp_file)
        self.temp_file.close()

    def tearDown(self):
        # Eliminar archivo temporal
        os.remove(self.temp_file.name)

    # ---------------------------
    # Pruebas para getKeys()
    # ---------------------------

    def test_getKeys_default(self):
        argv = ["getJason.py", "archivo.json"]

        with patch('sys.argv', argv):
            result = getJason.getKeys(argv)

        self.assertEqual(result, ["token1"])

    def test_getKeys_multiple_keys(self):
        argv = ["getJason.py", "archivo.json", "token1", "token2"]

        with patch('sys.argv', argv):
            result = getJason.getKeys(argv)

        self.assertEqual(result, ["token1", "token2"])

    # ---------------------------
    # Pruebas para getData()
    # ---------------------------

    def test_getData_valid_json(self):
        result = getJason.getData(self.temp_file.name)

        self.assertEqual(result, self.test_data)

    def test_getData_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            getJason.getData("archivo_inexistente.json")

    # ---------------------------
    # Pruebas para printResults()
    # ---------------------------

    def test_printResults_single_key(self):
        data = self.test_data
        keys = ["token1"]

        with patch('builtins.print') as mock_print:
            getJason.printResults(data, keys)

        mock_print.assert_called_once_with("C598-ECF9-F0F7-881A")

    def test_printResults_multiple_keys(self):
        data = self.test_data
        keys = ["token1", "token2"]

        with patch('builtins.print') as mock_print:
            getJason.printResults(data, keys)

        self.assertEqual(mock_print.call_count, 2)

    def test_printResults_invalid_key(self):
        data = self.test_data
        keys = ["token3"]

        with self.assertRaises(KeyError):
            getJason.printResults(data, keys)

    # ---------------------------
    # Prueba integración main()
    # ---------------------------

    def test_main_execution(self):
        argv = [
            "getJason.py",
            self.temp_file.name,
            "token1",
            "token2"
        ]

        with patch('sys.argv', argv):
            with patch('builtins.print') as mock_print:
                getJason.main()

        self.assertEqual(mock_print.call_count, 2)


if __name__ == '__main__':
    unittest.main()

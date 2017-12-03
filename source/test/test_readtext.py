import unittest
from source.ReadTXT.readtext import *
import os

class TestReadText(unittest.TestCase):

    def test_ler_bairros(self):
        print(os.getcwd())
        path = os.getcwd() + "/../ReadTXT/setores.txt"
        estados = ler_setores(path)
        print(path)
        for e in estados:
            print(e)
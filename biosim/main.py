# -*- coding: utf-8 -*-

"""
"""

from biosim.animal import *
import sys
import re

class T:
    var = {
        "a":1,
        "b":2
    }

if __name__ == "__main__":
    liste = eval("tuple({}.var.keys())".format("T"))
    elemets = ["a","b","c"]
    for element in elemets:
        if element not in liste:
            raise ValueError("{} not in liste".format(element))

# -*- coding: utf-8 -*-

"""
"""

from biosim.animal import *
import sys
import re
if __name__ == "__main__":
    print([n for n in dir(sys.modules["biosim.animal"]) if not re.match("(__)|(np)|(ran)|(animal)",n)])

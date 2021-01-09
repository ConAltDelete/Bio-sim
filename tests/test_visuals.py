from biosim.visuals import *
from biosim.simulation import BioSim

import pytest

@pytest.mark.parametrize("valid_cells",['L','D','W','H'])
def test_single_cell(valid_cells):
	string2map("WWW\nW{}W\nWWW".format(valid_cells))

@pytest.mark.parametrize("invalid_cells",[ascii(n) for n in range(65,91) if n not in [76,72,68,87]])
def test_single_invalid_cell(invalid_cells):
	with pytest.raises(ValueError):
		string2map("WWW\nW{}W\nWWW".format(invalid_cells))

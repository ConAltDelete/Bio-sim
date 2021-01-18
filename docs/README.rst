How to use
==========

To use this pakcage you need to do the following

inigiate the simulation
------------------------
You set up the simulation by

.. code-block:: python

	import biosim
	map = "WWW\nWHW\nWWW\n"
	ini_pop = {
		"loc": (2,2),
		"pop": {
			"species": "Herbivore",
			"age": 5,
			"weight": 100 # kg
		}
	}
	sim = biosim.simulation.BioSim(map,ini_pop)

This is the most basic form of a simulation, where nothing gets simulated.

Simulation
----------
To simulate you use the ``biosim.simulate()``. An example of this is

.. code-block:: python

	sim.simulate(num_years = 100, vis_years = 5, img_years = 10)


``num_years`` is the number of years you want to simulate, ``vis_years`` plots every given years, and ``img_years`` is similar to ``vis_years`` however instead of ploting it saves a image, by default the pictures are saved as a ``.png`` file.

Save and load state
-------------------
If you want to save the state of your simulation you can use ``.save()`` and ``.load()``. An example of this is

.. code-block:: python

	sim.save(path="data/")
	sim.load(file)

The ``path`` argument is the directory you want to save your ``*.biosim``. The directory will be created in the root directory.
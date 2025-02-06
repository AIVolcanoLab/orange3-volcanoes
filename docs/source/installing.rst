Installing and Running
----------------------


**Installing Orange**

Follow the procedure on the `Orange download page`_, or read the instructions in `orange3 GitHub`_.

.. _Orange download page: https://orangedatamining.com/download/
.. _orange3 GitHub: https://github.com/biolab/orange3/blob/master/README.md



**Installing Orange-Volcanoes**

Once Orange has been correctly installed in a dedicated environment, we can proceed with installing the Orange-Volcanoes add-on within the same environment.
This can be done via `pip install`_ with the simple command:

.. code-block:: shell

   pip install orange3-volcanoes

.. _pip install: https://pypi.org/project/orange3-volcanoes/


**Running**

Make sure you have activated the correct virtual environment. If you followed the conda instructions in `orange3 GitHub`_:

.. code-block:: shell

   conda activate orange3


Run `orange-canvas` or `python3 -m Orange.canvas`. Add `--help` for a list of program options.

.. code-block:: shell
   
   orange-canvas


Starting up for the first time may take a while.

By running Orange, you will find all the widgets of the Orange-Volcanoes add-on on the left side of the main Orange interface where all the other widgets are, grouped under the name "Volcanoes".



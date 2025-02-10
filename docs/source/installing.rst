Installing and Running
----------------------

We strongly suggest installing Orange-Volcanoes in a Conda environment.


Step 1: Installing Anaconda or Miniconda
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, install `Anaconda`_ or `Miniconda`_ for your OS.  
Should you use Anaconda Distribution or Miniconda? If you are unsure, please refer to the
`Getting Started with Anaconda guide`_.

.. _Anaconda: https://www.anaconda.com/download/success
.. _Miniconda: https://www.anaconda.com/download/success#miniconda
.. _Getting Started with Anaconda guide: https://docs.anaconda.com/getting-started/


Step 2: Installing Orange
~~~~~~~~~~~~~~~~~~~~~~~~~

Then, create a new conda environment, and install `orange3`_:

.. _orange3: https://github.com/biolab/orange3

.. code-block:: shell

   # Add conda-forge to your channels for access to the latest release
   conda config --add channels conda-forge

   # Perhaps enforce strict conda-forge priority
   conda config --set channel_priority strict

   # Create and activate an environment for Orange
   conda create python=3.10 --yes --name orange3
   conda activate orange3

   # Install Orange
   conda install orange3


Step 2: Installing Orange-Volcanoes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once Orange has been correctly installed in a dedicated environment, we can proceed
with installing the Orange-Volcanoes add-on within the same environment.
This can be done via pip install with the simple command:

.. code-block:: shell

   pip install orange3-volcanoes


Running
~~~~~~~

Make sure you have activated the correct virtual environment:

.. code-block:: shell

   conda activate orange3

Then launch Orange:

.. code-block:: shell

   orange-canvas

Alternatively, run ``orange-canvas`` or ``python3 -m Orange.canvas`` (add ``--help`` for a list of program options).

Starting up for the first time may take a while.

By running Orange, you will find all the widgets of the Orange-Volcanoes add-on on the left side of the main Orange interface,
grouped under the name "Volcanoes".

CpxBarometer
============

This widget calculates the pressure of clinopyroxene (cpx) formation using its chemical composition or the composition of clinopyroxene–liquid (cpx–liq) pairs.

The widget uses the `Thermobar <https://www.jvolcanica.org/ojs/index.php/volcanica/article/view/161>`_ tool to function and requires a dataset prepared in a specific way (with specific variable labels). An example of how variables should be renamed before using the widget is shown in Table 1. More details can be found by consulting the Thermobar `documentation <https://thermobar.readthedocs.io/en/latest/>`_.

.. table:: Example of a standard data form for Thermobarometric estimates, from Agreda López et al. (2024)
   :name: tab_my_label



As shown in the Figure, users can select whether to use barometers based on cpx composition only or on cpx–liquid pairs. For each of the two options, users can select the barometry formula that best suits their dataset via a convenient drop-down menu. If the chosen formula is temperature-dependent, the user can choose whether to (i) use temperature values found in a specific column within their dataset, (ii) enter a specific temperature to apply to the entire dataset, or (iii) calculate their own temperature from a specific model.

.. _fig7_CpxBarometer:

.. figure:: ../../images/Fig_7.png
   :width: 90%
   :align: center

   **CpxBarometer**. The widget interface allows users to select whether to use barometers based on cpx composition only or on cpx–liquid pairs. For each option, the appropriate barometry formula can be selected via a drop-down menu. If the formula is temperature-dependent, the user can choose between using a temperature column, entering a specific temperature, or calculating their own temperature.



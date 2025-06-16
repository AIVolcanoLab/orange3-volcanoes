import numpy as np
import pandas as pd
from Orange.data import Table, ContinuousVariable, Domain
from Orange.widgets.settings import Setting, ContextSetting
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from orangewidget.widget import Msg
from OrangeVolcanoes.utils import dataManipulation as dm
from AnyQt.QtCore import Qt
from PyQt5.QtWidgets import QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt # Make sure Qt is imported for options

## Lets load in the functions we need

from Thermobar import calculate_cpx_opx_temp, calculate_cpx_opx_press_temp

# Import all the thermobar stuff we need
from Thermobar import (
    calculate_cpx_opx_temp,calculate_cpx_opx_press, calculate_cpx_opx_press_temp,
    calculate_cpx_only_temp, calculate_cpx_only_press,
    calculate_cpx_liq_temp, calculate_cpx_liq_press,
        calculate_cpx_liq_press_temp, calculate_cpx_liq_press_temp,
         calculate_cpx_only_press_temp, calculate_cpx_only_press_temp,
 calculate_opx_only_press, calculate_opx_liq_temp, calculate_opx_liq_press, calculate_opx_liq_press_temp

)

## Load in the ideal columns
cpx_cols = ['SiO2_Cpx', 'TiO2_Cpx', 'Al2O3_Cpx',
'FeOt_Cpx', 'MnO_Cpx', 'MgO_Cpx', 'CaO_Cpx', 'Na2O_Cpx', 'K2O_Cpx',
'Cr2O3_Cpx']


opx_cols = ['SiO2_Opx', 'TiO2_Opx', 'Al2O3_Opx',
'FeOt_Opx', 'MnO_Opx', 'MgO_Opx', 'CaO_Opx', 'Na2O_Opx', 'K2O_Opx',
'Cr2O3_Opx']


liq_cols = ['SiO2_Liq', 'TiO2_Liq', 'Al2O3_Liq',
'FeOt_Liq', 'MnO_Liq', 'MgO_Liq', 'CaO_Liq', 'Na2O_Liq', 'K2O_Liq',
'Cr2O3_Liq', 'P2O5_Liq', 'H2O_Liq', 'Fe3Fet_Liq', 'NiO_Liq', 'CoO_Liq',
 'CO2_Liq']




## Load in the functions# Opx-Cpx temp
MODELS_CPX_OPX_TEMP = [
    ('T_Put2008_eq36', 'T_Put2008_eq36', True, False),
        ('T_Put2008_eq37', 'T_Put2008_eq37', True, False),
        ('T_Brey1990', 'T_Brey1990', True, False),
        ('T_Wood1973', 'T_Wood1973', False, False),
        ('T_Wells1977', 'T_Wells1977', False, False),

]


MODELS_CPX_OPX_PRESSURE = [
    ('P_Put2008_eq38', 'P_Put2008_eq38', False, False),
    ('P_Put2008_eq39', 'P_Put2008_eq39', True, False),
]

# ------------------- Cpx -----------------------

MODELS_CPX_ONLY_PRESSURE = [
    ('P_Wang2021_eq1', 'P_Wang2021_eq1',False,False),
    ('P_Put2008_eq32a', 'P_Put2008_eq32a',True,False),
    ('P_Put2008_eq32b', 'P_Put2008_eq32b',True,True),
    ('P_Nimis1999_BA', 'P_Nimis1999_BA',False,False)
]


MODELS_CPX_LIQ_PRESSURE = [
    ('P_Put1996_eqP1', 'P_Put1996_eqP1',True,False),
    ('P_Mas2013_eqPalk1', 'P_Mas2013_eqPalk1',True,False),
    ('P_Put1996_eqP2', 'P_Put1996_eqP2',True,False),
    ('P_Mas2013_eqPalk2', 'P_Mas2013_eqPalk2',True,False),
    ('P_Put2003', 'P_Put2003',True,False),
    ('P_Put2008_eq30', 'P_Put2008_eq30',True,True),
    ('P_Put2008_eq31', 'P_Put2008_eq31',True,True),
    ('P_Put2008_eq32c', 'P_Put2008_eq32c',True,True),
    ('P_Mas2013_eqalk32c', 'P_Mas2013_eqalk32c',True,True),
    ('P_Mas2013_Palk2012', 'P_Mas2013_Palk2012',False,True),
    ('P_Neave2017', 'P_Neave2017',True,False)
]


MODELS_CPX_ONLY_TEMPERATURE = [
    ('T_Put2008_eq32d', 'T_Put2008_eq32d',True,False),
    ('T_Put2008_eq32d_subsol', 'T_Put2008_eq32d_subsol',True,False),
    ('T_Wang2021_eq2', 'T_Wang2021_eq2',False,False)
]

MODELS_CPX_LIQ_TEMPERATURE = [
    ('T_Put1996_eqT1', 'T_Put1996_eqT1',False,False),
    ('T_Put1996_eqT2', 'T_Put1996_eqT2',True,False),
    ('T_Put1999', 'T_Put1999',True,False),
    ('T_Put2003', 'T_Put2003',True,False),
    ('T_Put2008_eq33', 'T_Put2008_eq33',True,True),
    ('T_Put2008_eq34_cpx_sat', 'T_Put2008_eq34_cpx_sat',True,True),
    ('T_Mas2013_eqTalk1', 'T_Mas2013_eqTalk1',False,False),
    ('T_Mas2013_eqTalk2', 'T_Mas2013_eqTalk2',True,False),
    ('T_Mas2013_eqalk33', 'T_Mas2013_eqalk33',True,True),
    ('T_Mas2013_Talk2012', 'T_Mas2013_Talk2012',False,True),
    ('T_Brug2019', 'T_Brug2019',False,False)
]

try:
    import Thermobar_onnx

    MODELS_CPX_ONLY_PRESSURE.extend([
        ('T_Jorgenson2022_Cpx_only_(ML)', 'T_Jorgenson2022_Cpx_only_onnx',False,False)
        ])


    MODELS_CPX_LIQ_TEMPERATURE.extend([
        ('T_Petrelli2020_Cpx_Liq_(ML)', 'T_Petrelli2020_Cpx_Liq_onnx',False,False),
        #('T_Jorgenson2022_Cpx_Liq_Norm_(ML)', 'T_Jorgenson2022_Cpx_Liq_Norm',False,False),
       # ('T_Jorgenson2022_Cpx_Liq_(ML)', 'T_Jorgenson2022_Cpx_Liq_onnx',False,False)
        ])

except ImportError:
    print("You cannot use Machile Learning Models. Install Thermobar_onnx.")

        # ------------------------------OPX -----------------------------
# Opx only pressure
MODELS_OPX_ONLY_PRESSURE = [
    ('P_Put2008_eq29c', 'P_Put2008_eq29c', True, False),
]

# Opx-Liq pressure
MODELS_OPX_LIQ_PRESSURE = [
    ('P_Put2008_eq29a', 'P_Put2008_eq29a', True, True),
    ('P_Put2008_eq29b', 'P_Put2008_eq29b', True, True),
    ('P_Put_Global_Opx', 'P_Put_Global_Opx', False, False),
     ('P_Put_Felsic_Opx', 'P_Put_Felsic_Opx', False, False),
]

MODELS_OPX_LIQ_TEMPERATURE = [
    ('T_Put2008_eq28a', 'T_Put2008_eq28a', True, True),
        ('T_Put2008_eq28b_opx_sat', 'T_Put2008_eq28b_opx_sat', True, True),
        ('T_Beatt1993_opx', 'T_Beatt1993_opx', True, False),
]


# Opx only pressure
MODELS_OPX_ONLY_TEMPERATURE = [
 ('None_available','None_available',  True, True),
]

## now into the code
class OWThermobar(OWWidget):
    name = "Thermobar Calculations"
    description = "Perform various thermobarometric calculations on mineral data."
    icon = "icons/thermobar.png" # You'll need a new icon
    priority = 5
    keywords = ['Thermobar', 'Cpx', 'Opx', 'Temperature', 'Pressure']

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        data = Output("Data", Table, dynamic=False)

# --- Context Settings ---
    # Opx-Cpx Thermometry
    cpx_opx_temp_model_idx = ContextSetting(0)
    cpx_opx_temp_pressure_type = ContextSetting(0)
    cpx_opx_temp_pressure_value = ContextSetting(1.0)
    cpx_opx_temp_barometer_model_idx = ContextSetting(0)
    cpx_opx_temp_fixed_h2o = ContextSetting(False)
    cpx_opx_temp_fixed_h2o_value_str = ContextSetting("1.0")

    # Opx-Cpx Barometry
    cpx_opx_press_model_idx = ContextSetting(0)
    cpx_opx_press_temp_type = ContextSetting(0)
    cpx_opx_press_temp_value = ContextSetting(900.0)
    cpx_opx_press_thermometer_model_idx = ContextSetting(0)
    cpx_opx_press_fixed_h2o = ContextSetting(False)
    cpx_opx_press_fixed_h2o_value_str = ContextSetting("1.0")

    # Opx Thermometry
    opx_temp_model_type = ContextSetting(0) # 0 for Opx-only, 1 for Opx-Liq
    opx_temp_model_idx_oo = ContextSetting(0)
    opx_temp_model_idx_ol = ContextSetting(0)
    opx_temp_pressure_type = ContextSetting(0) # 0 for Dataset, 1 for Fixed, 2 for Model
    opx_temp_pressure_value = ContextSetting(1.0)
    opx_temp_barometer_choice = ContextSetting(1) # 0 for Opx-only, 1 for Opx-Liq
    opx_temp_barometer_model_idx_oo = ContextSetting(0)
    opx_temp_barometer_model_idx_ol = ContextSetting(0)
    opx_temp_fixed_h2o = ContextSetting(False)
    opx_temp_fixed_h2o_value_str = ContextSetting("1.0")

    # Opx Barometry
    opx_press_model_type = ContextSetting(0)
    opx_press_model_idx_oo = ContextSetting(0)
    opx_press_model_idx_ol = ContextSetting(0)
    opx_press_temp_type = ContextSetting(0)
    opx_press_temp_value = ContextSetting(900.0)
    opx_press_thermometer_choice = ContextSetting(0)
    opx_press_thermometer_model_idx_oo = ContextSetting(0)
    opx_press_thermometer_model_idx_ol = ContextSetting(0)
    opx_press_fixed_h2o = ContextSetting(False)
    opx_press_fixed_h2o_value_str = ContextSetting("1.0")

    # Main calculation type selection
    calculation_type = ContextSetting(0) # Default to 'None'

    resizing_enabled = False
    want_main_area = False
    auto_apply = Setting(True)

    class Error(OWWidget.Error):
        value_error = Msg("{}")

    class Warning(OWWidget.Warning):
        value_error = Msg("{}")


    def __init__(self):
        super().__init__()

        # Initialize data attribute FIRST
        self.data = None

        # Then initialize all other attributes
        self._initialize_attributes()

        # Build the GUI
        self._build_main_gui()

        # Set initialization flag and update controls
        self._initialized = True
        self._update_all_controls()

    def _initialize_attributes(self):

        # Opx-Cpx Thermometry
        self.cpx_opx_temp_model_idx = 0
        self.cpx_opx_temp_pressure_type = 0
        self.cpx_opx_temp_pressure_value = 1.0
        self.cpx_opx_temp_barometer_model_idx = 0
        self.cpx_opx_temp_fixed_h2o = False
        self.cpx_opx_temp_fixed_h2o_value_str = "1.0"

        # Opx-Cpx Barometry
        self.cpx_opx_press_model_idx = 0
        self.cpx_opx_press_temp_type = 0
        self.cpx_opx_press_temp_value = 900.0
        self.cpx_opx_press_thermometer_model_idx = 0
        self.cpx_opx_press_fixed_h2o = False
        self.cpx_opx_press_fixed_h2o_value_str = "1.0"

        # Opx Thermometry
        self.opx_temp_model_type = 0
        self.opx_temp_model_idx_oo = 0
        self.opx_temp_model_idx_ol = 0
        self.opx_temp_pressure_type = 0
        self.opx_temp_pressure_value = 1.0
        self.opx_temp_barometer_choice = 1
        self.opx_temp_barometer_model_idx_oo = 0
        self.opx_temp_barometer_model_idx_ol = 0
        self.opx_temp_fixed_h2o = False
        self.opx_temp_fixed_h2o_value_str = "1.0"

        # Opx Barometry
        self.opx_press_model_type = 0
        self.opx_press_model_idx_oo = 0
        self.opx_press_model_idx_ol = 0
        self.opx_press_temp_type = 0
        self.opx_press_temp_value = 900.0
        self.opx_press_thermometer_choice = 0
        self.opx_press_thermometer_model_idx_oo = 0
        self.opx_press_thermometer_model_idx_ol = 0
        self.opx_press_fixed_h2o = False
        self.opx_press_fixed_h2o_value_str = "1.0"

    def _build_main_gui(self):
        """Build the main GUI structure"""
        gui.label(self.controlArea, self, "<i>Calculations performed using Thermobar...</i>")
        gui.separator(self.controlArea)

        # Calculation type dropdown
        calc_type_box = gui.vBox(self.controlArea, "Select Calculation Type")
        self.calculation_type_combo = gui.comboBox(
            calc_type_box, self, "calculation_type",
            items=["None", "Cpx-Opx Thermometry", "Cpx-Opx Barometry",
                "Opx Thermometry", "Opx Barometry"],
            callback=self._update_all_controls
        )
        gui.separator(self.controlArea)

        # Build all calculation sections
        self._build_calculation_sections()

        gui.auto_apply(self.buttonsArea, self)

    def _build_calculation_sections(self):
        """Build all calculation type sections"""
        self.cpx_opx_temp_box = gui.vBox(self.controlArea, "Cpx-Opx Thermometry Settings")
        self._build_cpx_opx_temp_gui(self.cpx_opx_temp_box)
        self.cpx_opx_temp_box.setVisible(False)

        self.cpx_opx_press_box = gui.vBox(self.controlArea, "Cpx-Opx Barometry Settings")
        self._build_cpx_opx_press_gui(self.cpx_opx_press_box)
        self.cpx_opx_press_box.setVisible(False)

        self.opx_temp_box = gui.vBox(self.controlArea, "Opx Thermometry Settings")
        self._build_opx_temp_gui(self.opx_temp_box)
        self.opx_temp_box.setVisible(False)

        self.opx_press_box = gui.vBox(self.controlArea, "Opx Barometry Settings")
        self._build_opx_press_gui(self.opx_press_box)
        self.opx_press_box.setVisible(False)


    def _build_cpx_opx_temp_gui(self, parent_box):
        """Builds the GUI elements for Cpx-Opx Thermometry."""

        # Models selection
        temp_model_box = gui.vBox(parent_box, "Models")
        self.cpx_opx_temp_models_combo = gui.comboBox(
            temp_model_box, self, "cpx_opx_temp_model_idx",
            items=[m[0] for m in MODELS_CPX_OPX_TEMP],
            callback=self.__update_controls_cpx_opx)

        # Pressure settings
        pressure_box = gui.radioButtons(
            parent_box, self, "cpx_opx_temp_pressure_type", box="Pressure Input",
            callback=self.__update_controls_cpx_opx)
        gui.appendRadioButton(pressure_box, "Dataset as Pressure (kbar)")

        rb_fixed_p = gui.appendRadioButton(pressure_box, "Fixed Pressure")
        self.cpx_opx_temp_pressure_value_box = gui.doubleSpin(
            gui.indentedBox(pressure_box, gui.checkButtonOffsetHint(rb_fixed_p)), self,
            "cpx_opx_temp_pressure_value", 1.0, 10000.0, step=0.1, label="Pressure Value (kbar)",
            alignment=Qt.AlignRight, callback=self.__update_controls_cpx_opx, controlWidth=80, decimals=1)

        rb_model_p = gui.appendRadioButton(pressure_box, "Model as Pressure")
        model_as_p_box = gui.indentedBox(pressure_box, gui.checkButtonOffsetHint(rb_model_p))

        self.cpx_opx_temp_barometer_model_box = gui.comboBox(
            model_as_p_box, self, "cpx_opx_temp_barometer_model_idx", items=[m[0] for m in MODELS_CPX_OPX_PRESSURE],
            callback=self.__update_controls_cpx_opx)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        gui.checkBox(h2o_box, self, "cpx_opx_temp_fixed_h2o", "Fixed H₂O", callback=self.__update_controls_cpx_opx)
        # Correctly assign the lineEdit to self.cpx_opx_temp_fixed_h2o_input
        self.cpx_opx_temp_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "cpx_opx_temp_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)

    def _build_cpx_opx_press_gui(self, parent_box):
        """Builds the GUI elements for Cpx-Opx Barometry."""
        # Models selection
        press_model_box = gui.vBox(parent_box, "Models")
        self.cpx_opx_press_models_combo = gui.comboBox(
            press_model_box, self, "cpx_opx_press_model_idx",
            items=[m[0] for m in MODELS_CPX_OPX_PRESSURE],
            callback=self.__update_controls_cpx_opx)

        # Temperature settings
        temp_box = gui.radioButtons(
            parent_box, self, "cpx_opx_press_temp_type", box="Temperature Input",
            callback=self.__update_controls_cpx_opx)
        gui.appendRadioButton(temp_box, "Dataset as Temperature (K)")

        rb_fixed_t = gui.appendRadioButton(temp_box, "Fixed Temperature")
        self.cpx_opx_press_temp_value_box = gui.doubleSpin(
            gui.indentedBox(temp_box, gui.checkButtonOffsetHint(rb_fixed_t)), self,
            "cpx_opx_press_temp_value", 500.0, 2000.0, step=1.0, label="Temperature Value (K)",
            alignment=Qt.AlignRight, callback=self.__update_controls_cpx_opx, controlWidth=80, decimals=0)

        rb_model_t = gui.appendRadioButton(temp_box, "Model as Temperature")
        model_as_t_box = gui.indentedBox(temp_box, gui.checkButtonOffsetHint(rb_model_t))

        self.cpx_opx_press_thermometer_model_box = gui.comboBox(
            model_as_t_box, self, "cpx_opx_press_thermometer_model_idx", items=[m[0] for m in MODELS_CPX_OPX_TEMP],
            callback=self.__update_controls_cpx_opx)

        # H2O settings (if Cpx-Opx Pressure models require H2O)
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        gui.checkBox(h2o_box, self, "cpx_opx_press_fixed_h2o", "Fixed H₂O", callback=self.__update_controls_cpx_opx)
        # Correctly assign the lineEdit to self.cpx_opx_press_fixed_h2o_input
        self.cpx_opx_press_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "cpx_opx_press_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)

            ## Now Opx

    def _build_opx_temp_gui(self, parent_box):
        """Builds the Opx Thermometry GUI section using only existing callbacks"""
        # Set default to Opx-Liq thermometers
        self.opx_temp_model_type = 1

        # Thermometer Type selection
        model_type_box = gui.vBox(parent_box, "Thermometer Type")
        self.opx_thermometer_type_radiobuttons = gui.radioButtons(
            model_type_box, self, "opx_temp_model_type",
            btnLabels=["Opx-only thermometers", "Opx-Liq thermometers"],
            callback=self._update_opx_temp_selection_vis  # Existing callback
        )
        self.opx_thermometer_type_radiobuttons.buttons[0].setEnabled(False)

        # Opx-only models
        self.opx_only_temp_model_box = gui.vBox(parent_box, "Opx-Only Thermometers")
        self.opx_only_temp_model_combo = gui.comboBox(
            self.opx_only_temp_model_box, self, "opx_temp_model_idx_oo",
            items=[m[0] for m in MODELS_OPX_ONLY_TEMPERATURE],
            callback=self._update_opx_temp_selection_vis  # Existing callback
        )
        self.opx_only_temp_model_box.setVisible(False)

        # Opx-Liq models
        self.opx_liq_temp_model_box = gui.vBox(parent_box, "Opx-Liq Thermometers")
        self.opx_liq_temp_model_combo = gui.comboBox(
            self.opx_liq_temp_model_box, self, "opx_temp_model_idx_ol",
            items=[m[0] for m in MODELS_OPX_LIQ_TEMPERATURE],
            callback=self._update_opx_temp_selection_vis  # Existing callback
        )
        self.opx_liq_temp_model_box.setVisible(True)

        # Pressure input
        pressure_input_box = gui.vBox(parent_box, "Pressure Input")
        self.opx_pressure_input_radiobuttons = gui.radioButtons(
            pressure_input_box, self, "opx_temp_pressure_type",
            btnLabels=["From Dataset", "Fixed Value", "From Model (Iterative)"],
            callback=self._update_opx_temp_pressure_controls  # Existing callback
        )

        # Fixed pressure value
        self.opx_fixed_pressure_box = gui.hBox(pressure_input_box)
        gui.lineEdit(self.opx_fixed_pressure_box, self, "opx_temp_pressure_value",
                    label="kbar", valueType=float, controlWidth=80,
                    callback=self._on_fixed_pressure_change)  # Existing callback
        self.opx_fixed_pressure_box.setVisible(False)

        # Barometer selection
        self.opx_barometer_choice_box = gui.vBox(parent_box, "Barometer Model")
        self.opx_barometer_type_radiobuttons = gui.radioButtons(
            self.opx_barometer_choice_box, self, "opx_temp_barometer_choice",
            btnLabels=["Opx-only barometer", "Opx-Liq barometer"],
            callback=self._update_opx_barometer_selection  # Existing callback
        )
        self.opx_barometer_choice_box.setVisible(False)

        # Barometer models
        self.opx_only_barometer_model_box = gui.vBox(self.opx_barometer_choice_box, "Opx-Only Barometers")
        self.opx_only_barometer_model_combo = gui.comboBox(
            self.opx_only_barometer_model_box, self, "opx_temp_barometer_model_idx_oo",
            items=[m[0] for m in MODELS_OPX_ONLY_PRESSURE],
            callback=self.commit.deferred
        )
        self.opx_only_barometer_model_box.setVisible(False)

        self.opx_liq_barometer_model_box = gui.vBox(self.opx_barometer_choice_box, "Opx-Liq Barometers")
        self.opx_liq_barometer_model_combo = gui.comboBox(
            self.opx_liq_barometer_model_box, self, "opx_temp_barometer_model_idx_ol",
            items=[m[0] for m in MODELS_OPX_LIQ_PRESSURE],
            callback=self.commit.deferred
        )
        self.opx_liq_barometer_model_box.setVisible(False)

        # H2O settings
        self.opx_temp_h2o_box = gui.vBox(parent_box, "H2O Content for Thermometer")
        self.opx_temp_fixed_h2o_checkbox = gui.checkBox(
            self.opx_temp_h2o_box, self, "opx_temp_fixed_h2o", "Use Fixed H2O",
            callback=self._update_opx_temp_h2o_input  # Existing callback
        )
        self.opx_temp_fixed_h2o_input_box = gui.hBox(self.opx_temp_h2o_box)
        gui.lineEdit(self.opx_temp_fixed_h2o_input_box, self, "opx_temp_fixed_h2o_value_str",
                    label="Fixed H2O (wt%)", controlWidth=80,
                    callback=self._on_fixed_h2o_change)  # Existing callback
        self.opx_temp_fixed_h2o_input_box.setVisible(False)

    def _on_fixed_pressure_change(self):
        # This function is called when the fixed pressure value is changed.
        # You don't necessarily need to call commit here if auto_apply handles it.
        # But if you want immediate calculation, and you are not already in a
        # deferred context, you could consider self.commit.now() IF you really need it.
        # For most cases with auto_apply, simply changing the value is enough.
        # Let's just pass for now and rely on auto_apply.
        pass

    def _on_fixed_h2o_change(self):
        # This function is called when the fixed H2O value is changed.
        # As with _on_fixed_pressure_change, we just 'pass' here.
        # auto_apply (if True) will handle triggering the main commit.
        pass

    def _build_opx_press_gui(self, parent_box):
        """Builds the GUI elements for Opx Barometry."""
        # This function would be similar to _build_cpx_opx_press_gui but for Opx
        # based on MODELS_OPX_ONLY_PRESSURE and MODELS_OPX_LIQ_PRESSURE
        # and respective temperature models if iterative calc is supported.
        pass # Placeholder for now

    def _update_all_controls(self):
        """Update visibility of all calculation sections."""
        # Hide all sections first
        self.cpx_opx_temp_box.setVisible(False)
        self.cpx_opx_press_box.setVisible(False)
        self.opx_temp_box.setVisible(False)
        self.opx_press_box.setVisible(False)

        # Show the selected section
        if self.calculation_type == 1:  # Cpx-Opx Thermometry
            self.cpx_opx_temp_box.setVisible(True)
            self.__update_controls_cpx_opx()
        elif self.calculation_type == 2:  # Cpx-Opx Barometry
            self.cpx_opx_press_box.setVisible(True)
            self.__update_controls_cpx_opx()
        elif self.calculation_type == 3:  # Opx Thermometry
            self.opx_temp_box.setVisible(True)
            self._update_controls_opx()  # This now calls the corrected version
        elif self.calculation_type == 4:  # Opx Barometry
            self.opx_press_box.setVisible(True)
            self._update_controls_opx_press()

        # Only commit if we're fully initialized
        if hasattr(self, '_initialized') and self._initialized:
            self.commit.deferred()


    def __update_controls_cpx_opx(self):
        # Hide all calculation sections first
        self.cpx_opx_temp_box.setVisible(False)
        self.cpx_opx_press_box.setVisible(False)


        # Show the selected calculation section
        if self.calculation_type == 1: # Cpx-Opx Thermometry
            self.cpx_opx_temp_box.setVisible(True)
            # You'll likely want to call these helper updates specific to the visible section:
            # self._update_cpx_opx_temp_models()
            # self._update_cpx_opx_temp_pressure_input() # This method needs to exist and handle input fields
        elif self.calculation_type == 2: # Cpx-Opx Barometry
            self.cpx_opx_press_box.setVisible(True)
            # self._update_cpx_opx_press_models()
            # self._update_cpx_opx_press_temp_input() # This method needs to exist and handle input fields


        # Update the state of H2O input fields based on their respective fixed_h2o checkboxes
        if hasattr(self, 'cpx_opx_temp_fixed_h2o_input'):
             self.cpx_opx_temp_fixed_h2o_input.setEnabled(self.cpx_opx_temp_fixed_h2o)
        if hasattr(self, 'cpx_opx_press_fixed_h2o_input'):
            self.cpx_opx_press_fixed_h2o_input.setEnabled(self.cpx_opx_press_fixed_h2o)

        # Enable/disable pressure value spin box based on pressure_type == 1 (Fixed)
        if hasattr(self, 'cpx_opx_temp_pressure_value_box'):
            self.cpx_opx_temp_pressure_value_box.setEnabled(self.cpx_opx_temp_pressure_type == 1)


        # Enable/disable barometer model combo box based on pressure_type == 2 (Model)
        if hasattr(self, 'cpx_opx_temp_barometer_model_box'):
            self.cpx_opx_temp_barometer_model_box.setEnabled(self.cpx_opx_temp_pressure_type == 2)


        # Enable/disable temperature value spin box based on temp_type == 1 (Fixed)
        if hasattr(self, 'cpx_opx_press_temp_value_box'):
            self.cpx_opx_press_temp_value_box.setEnabled(self.cpx_opx_press_temp_type == 1)

        # Enable/disable thermometer model combo box based on temp_type == 2 (Model)
        if hasattr(self, 'cpx_opx_press_thermometer_model_box'):
            self.cpx_opx_press_thermometer_model_box.setEnabled(self.cpx_opx_press_temp_type == 2)

        # Now, for the radio buttons, you need to find QRadioButtons
        # and ensure the correct visibility/enabled state
        for rb in self.cpx_opx_temp_box.findChildren(QRadioButton):
            pass

        for rb in self.cpx_opx_press_box.findChildren(QRadioButton):
            pass


        self.commit.now() # Trigger the output sending immediately

    # Opx
# --- Opx Thermometry Specific Update Functions ---

    def _update_controls_opx(self):
        """Main update function for Opx Thermometry settings."""
        # Replace call to non-existent function with existing one
        self._update_opx_temp_selection_vis()  # This is the function you actually have

        # These are your existing functions that should work
        self._update_opx_temp_pressure_controls()
        self._update_opx_barometer_selection()
        self._update_opx_temp_h2o_input()

    def _update_opx_temp_selection_vis(self):
        """Handle all model selection updates for Opx thermometry"""
        try:
            # Determine current model type and requirements
            if self.opx_temp_model_type == 0:  # Opx-only
                model_info = MODELS_OPX_ONLY_TEMPERATURE[self.opx_temp_model_idx_oo]
                self.opx_only_temp_model_box.setVisible(True)
                self.opx_liq_temp_model_box.setVisible(False)
            else:  # Opx-Liq
                model_info = MODELS_OPX_LIQ_TEMPERATURE[self.opx_temp_model_idx_ol]
                self.opx_only_temp_model_box.setVisible(False)
                self.opx_liq_temp_model_box.setVisible(True)

            _, _, needs_p, needs_h2o = model_info

            # Update pressure model button state
            if hasattr(self, 'opx_pressure_input_radiobuttons'):
                model_rb = self.opx_pressure_input_radiobuttons.buttons[2]  # "From Model" button
                model_rb.setEnabled(needs_p)
                if not needs_p and self.opx_temp_pressure_type == 2:
                    self.opx_temp_pressure_type = 0  # Revert to dataset

            # Update H2O controls
            if hasattr(self, 'opx_temp_fixed_h2o_checkbox'):
                self.opx_temp_fixed_h2o_checkbox.setEnabled(needs_h2o)
                self.opx_temp_fixed_h2o_input_box.setEnabled(
                    needs_h2o and self.opx_temp_fixed_h2o)

        except Exception as e:
            print(f"Error updating Opx temp selection: {e}")

    def _update_opx_temp_pressure_controls(self):
        """Controls visibility of fixed pressure input and barometer model selection."""
        is_fixed_pressure_selected = (self.opx_temp_pressure_type == 1)
        is_model_pressure_selected = (self.opx_temp_pressure_type == 2)

        self.opx_fixed_pressure_box.setVisible(is_fixed_pressure_selected)
        self.opx_barometer_choice_box.setVisible(is_model_pressure_selected)

        # If "From Model" is selected, update the barometer choices
        if is_model_pressure_selected:
            self._update_opx_barometer_selection()


    def _update_opx_barometer_selection(self):
        """Controls visibility of Opx-only vs Opx-Liq barometer model combos."""
        if self.opx_temp_barometer_choice == 0: # Opx-only barometer
            self.opx_only_barometer_model_box.setVisible(True)
            self.opx_liq_barometer_model_box.setVisible(False)
        else: # Opx-Liq barometer
            self.opx_only_barometer_model_box.setVisible(False)
            self.opx_liq_barometer_model_box.setVisible(True)


    def _update_opx_temp_h2o_input(self):
        """Controls visibility of fixed H2O input for Opx Thermometry."""
        self.opx_temp_fixed_h2o_input_box.setVisible(self.opx_temp_fixed_h2o)



    @Inputs.data
    def set_data(self, data):
        self.data = data
        self.commit.now()

    @gui.deferred



    def commit(self):
        self.clear_messages()
        self.Error.value_error.clear()
        self.Warning.value_error.clear()

        # Safeguard against missing data attribute
        if not hasattr(self, 'data') or self.data is None:
            self.Outputs.data.send(None)
            return

        # Rest of your existing commit logic...
        if len(self.data.domain.attributes) <= 1:
            self.Warning.value_error("Not enough attributes in the dataset for calculations.")
            self.Outputs.data.send(None)
            return

        df = pd.DataFrame(data=np.array(self.data.X), columns=[a.name for a in self.data.domain.attributes])

        # Initialize variables with safe default values
        result_df = pd.DataFrame()
        prefix = ""
        temp_col_name_suffix = ""
        press_col_name_suffix = ""

        # Perform calculation based on the selected type
        if self.calculation_type == 1: # Cpx-Opx Thermometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_cpx_opx_temp(df.copy())
            except Exception as e:
                # --- TEMPORARY DEBUGGING CHANGE HERE ---
                import traceback
                error_traceback = traceback.format_exc()
                self.Error.value_error(f"Error in Cpx-Opx Thermometry: {e}\nFull Traceback:\n{error_traceback}")
                # --- END TEMPORARY DEBUGGING CHANGE ---
                self.Outputs.data.send(None)
                return

        elif self.calculation_type == 2: # Cpx-Opx Barometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_cpx_opx_press(df.copy())
            except Exception as e:
                # --- TEMPORARY DEBUGGING CHANGE HERE ---
                import traceback
                error_traceback = traceback.format_exc()
                self.Error.value_error(f"Error in Cpx-Opx Barometry: {e}\nFull Traceback:\n{error_traceback}")
                # --- END TEMPORARY DEBUGGING CHANGE ---
                self.Outputs.data.send(None)
                return

        elif self.calculation_type == 3: # Opx Thermometry - NEW
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_opx_temp(df.copy())
            except Exception as e:
                # --- TEMPORARY DEBUGGING CHANGE HERE ---
                import traceback
                error_traceback = traceback.format_exc()
                self.Error.value_error(f"Error in Opx Thermometry: {e}\nFull Traceback:\n{error_traceback}")
                # --- END TEMPORARY DEBUGGING CHANGE ---
                self.Outputs.data.send(None)
                return

        elif self.calculation_type == 4: # Opx Barometry - Placeholder for future implementation
            self.Warning.value_error("Opx Barometry calculation not yet implemented.")
            # Variables are already initialized, so no further action needed here
            # They will remain empty/default, leading to send(None) below.


        # If a calculation was performed and resulted in a DataFrame
        # This check will now always work because result_df is always initialized
        if not result_df.empty:
            output_table = self._create_output_table(
                self.data, result_df, prefix, temp_col_name_suffix, press_col_name_suffix)
            self.Outputs.data.send(output_table)
        else:
            self.Outputs.data.send(None)

    def _create_output_table(self, original_table, results_df, prefix, temp_col_suffix, press_col_suffix):
        """Creates a new Orange Table with calculated results as meta attributes."""
        # This current_meta_df is useful for checking existing names, but not directly for combining metas
        current_meta_names = set([m.name for m in original_table.domain.metas])

        new_meta_variables = []
        new_meta_values = []

        base_output_temp_name = f"{prefix}_{temp_col_suffix}"
        base_output_press_name = f"{prefix}_{press_col_suffix}"

        # Get existing attribute and meta names to ensure unique new names
        existing_names = set([a.name for a in original_table.domain.attributes] + list(current_meta_names))

        # --- Handle Temperature Output ---
        output_temp_calc_name = ""
        output_temp_input_name = ""

        if 'T_K_calc' in results_df.columns and not results_df['T_K_calc'].isnull().all():
            # If a calculated temperature exists and is not all NaNs
            output_temp_calc_name = base_output_temp_name
            suffix = 0
            while output_temp_calc_name in existing_names:
                suffix += 1
                output_temp_calc_name = f"{base_output_temp_name}_{suffix}"

            new_meta_variables.append(ContinuousVariable(output_temp_calc_name))
            new_meta_values.append(results_df['T_K_calc'].values)
            existing_names.add(output_temp_calc_name) # Add to prevent naming conflicts with input name

        if 'T_K_input' in results_df.columns and not results_df['T_K_input'].isnull().all():
            # If an input temperature exists and is not all NaNs
            # We want to differentiate if both calc and input are present (e.g., for comparison)
            # Or if only input is present.
            output_temp_input_name = base_output_temp_name + "_Input"
            suffix = 0
            while output_temp_input_name in existing_names:
                suffix += 1
                output_temp_input_name = f"{base_output_temp_name}_Input_{suffix}"

            new_meta_variables.append(ContinuousVariable(output_temp_input_name))
            new_meta_values.append(results_df['T_K_input'].values)
            existing_names.add(output_temp_input_name)


        # --- Handle Pressure Output ---
        output_press_calc_name = ""
        output_press_input_name = ""

        if 'P_kbar_calc' in results_df.columns and not results_df['P_kbar_calc'].isnull().all():
            # If a calculated pressure exists and is not all NaNs
            output_press_calc_name = base_output_press_name
            suffix = 0
            while output_press_calc_name in existing_names:
                suffix += 1
                output_press_calc_name = f"{base_output_press_name}_{suffix}"

            new_meta_variables.append(ContinuousVariable(output_press_calc_name))
            new_meta_values.append(results_df['P_kbar_calc'].values)
            existing_names.add(output_press_calc_name)


        if 'P_kbar_input' in results_df.columns and not results_df['P_kbar_input'].isnull().all():
            # If an input pressure exists and is not all NaNs
            output_press_input_name = base_output_press_name + "_Input"
            suffix = 0
            while output_press_input_name in existing_names:
                suffix += 1
                output_press_input_name = f"{base_output_press_name}_Input_{suffix}"

            new_meta_variables.append(ContinuousVariable(output_press_input_name))
            new_meta_values.append(results_df['P_kbar_input'].values)
            existing_names.add(output_press_input_name)


        # Convert the list of 1D new_meta_values into a 2D array (columns)
        if new_meta_values: # Check if there are any new meta values to add
            new_metas_array = np.column_stack(new_meta_values)
        else:
            new_metas_array = np.empty((len(original_table.X), 0)) # Ensure 2D empty array with correct rows


        # Combine existing metas with new ones
        if original_table.metas is not None and original_table.metas.size > 0:
            combined_metas_array = np.hstack([original_table.metas, new_metas_array])
        else:
            combined_metas_array = new_metas_array

        # Ensure combined_metas_array has the correct shape for from_numpy
        # It must be 2D, even if empty.
        if combined_metas_array.ndim == 1:
             combined_metas_array = combined_metas_array[:, np.newaxis]
        elif combined_metas_array.size == 0 and len(original_table.X) > 0:
            combined_metas_array = np.empty((len(original_table.X), 0))


        # Construct the new domain
        new_domain = Domain(original_table.domain.attributes, original_table.domain.class_vars,
                            original_table.domain.metas + tuple(new_meta_variables))

        return Table.from_numpy(new_domain, original_table.X, original_table.Y, combined_metas_array)

    def _get_h2o_value(self, df, requires_h2o, fixed_h2o, fixed_h2o_value_str, calculation_name):
        """Helper to get H2O value, handling fixed value or column."""
        if requires_h2o:
            if fixed_h2o:
                try:
                    return float(fixed_h2o_value_str)
                except ValueError:
                    self.Error.value_error(f"Invalid H₂O value entered for {calculation_name}.")
                    return None
            elif 'H2O_Liq' in df.columns:
                return df['H2O_Liq']
            else:
                self.Warning.value_error(f"'H2O_Liq' column not in Dataset for {calculation_name}, H₂O set to zero.")
                return 0 # Default to 0 if required but not found and not fixed
        return 0 # Return 0 if H2O is not required

    def _get_pressure_value(self, df, requires_pressure, pressure_type, pressure_value, calculation_name):
        """Helper to get Pressure value, handling dataset, fixed, or None."""
        if requires_pressure:
            if pressure_type == 0: # Dataset
                if 'P_kbar' in df.columns:
                    return df['P_kbar']
                else:
                    self.Warning.value_error(f"'P_kbar' column not in Dataset for {calculation_name}. Using default 1 kbar.")
                    return 1.0 # Default to 1 kbar if required and not found in dataset
            elif pressure_type == 1: # Fixed
                return pressure_value
        return None # Return None if pressure is not required

    def _get_temperature_value(self, df, requires_temp, temp_type, temp_value, calculation_name):
        """Helper to get Temperature value, handling dataset, fixed, or None."""
        if requires_temp:
            if temp_type == 0: # Dataset
                if 'T_K' in df.columns:
                    return df['T_K']
                else:
                    self.Warning.value_error(f"'T_K' column not in Dataset for {calculation_name}. Using default 900 K.")
                    return 900.0 # Default to 900 K if required and not found in dataset
            elif temp_type == 1: # Fixed
                return temp_value
        return None # Return None if temperature is not required


## Into the actual functions do the math, not just the GUI buttons
    def _calculate_cpx_opx_temp(self, df):
        """Encapsulates the Cpx-Opx Thermometry calculation logic."""
        _, current_model_func_name, requires_pressure_by_model, requires_h2o_by_model = MODELS_CPX_OPX_TEMP[self.cpx_opx_temp_model_idx]
        current_barometer_func_name = MODELS_CPX_OPX_PRESSURE[self.cpx_opx_temp_barometer_model_idx][1]

        df = dm.preprocessing(df, my_output='cpx_opx')

        water = self._get_h2o_value(df, requires_h2o_by_model,
                                    self.cpx_opx_temp_fixed_h2o,
                                    self.cpx_opx_temp_fixed_h2o_value_str,
                                    "Cpx-Opx Thermometry")
        if water is None: return pd.DataFrame(), "", "", "" # Error occurred in H2O fetching

        P_input = self._get_pressure_value(df, requires_pressure_by_model,
                                           self.cpx_opx_temp_pressure_type,
                                           self.cpx_opx_temp_pressure_value,
                                           "Cpx-Opx Thermometry")

        temperature = None
        pressure_output = None # This is for when pressure is calculated iteratively with temp

        if requires_pressure_by_model and self.cpx_opx_temp_pressure_type == 2: # Model as Pressure
            calc = calculate_cpx_opx_press_temp(
                opx_comps=df[opx_cols], cpx_comps=df[cpx_cols],
                equationT=current_model_func_name, equationP=current_barometer_func_name)
            temperature = calc['T_K_calc']
            pressure_output = calc['P_kbar_calc']
        else: # No pressure, fixed, or dataset pressure
            temperature = calculate_cpx_opx_temp(
                opx_comps=df[opx_cols], cpx_comps=df[cpx_cols],
                equationT=current_model_func_name, P=P_input)


        results_df = pd.DataFrame()
        results_df['T_K_calc'] = temperature

        if pressure_output is not None:
            results_df['P_kbar_calc'] = pressure_output
        elif P_input is not None:
            results_df['P_kbar_input'] = P_input # Store the input pressure if used
        else:
            results_df['P_kbar_input'] = np.full(len(df), np.nan) # Placeholder if no P input

        return results_df, "CpxOpx", "T_K", "P_kbar"

    def _calculate_cpx_opx_press(self, df):
        """Encapsulates the Cpx-Opx Barometry calculation logic."""
        _, current_model_func_name, requires_temp_by_model, requires_h2o_by_model = MODELS_CPX_OPX_PRESSURE[self.cpx_opx_press_model_idx]
        current_thermometer_func_name = MODELS_CPX_OPX_TEMP[self.cpx_opx_press_thermometer_model_idx][1]

        df = dm.preprocessing(df, my_output='cpx_opx')

        water = self._get_h2o_value(df, requires_h2o_by_model,
                                    self.cpx_opx_press_fixed_h2o,
                                    self.cpx_opx_press_fixed_h2o_value_str,
                                    "Cpx-Opx Barometry")
        if water is None: return pd.DataFrame(), "", "", ""

        T_input = self._get_temperature_value(df, requires_temp_by_model,
                                              self.cpx_opx_press_temp_type,
                                              self.cpx_opx_press_temp_value,
                                              "Cpx-Opx Barometry")

        pressure = None
        temperature_output = None # This is for when temp is calculated iteratively with pressure

        if requires_temp_by_model and self.cpx_opx_press_temp_type == 2: # Model as Temperature
            # For Cpx-Opx, it's calculate_cpx_opx_press_temp, but the primary output is pressure
            calc = calculate_cpx_opx_press_temp(
                opx_comps=df[opx_cols], cpx_comps=df[cpx_cols],
                equationP=current_model_func_name, equationT=current_thermometer_func_name)
            pressure = calc['P_kbar_calc']
            temperature_output = calc['T_K_calc']
        else: # No temperature, fixed, or dataset temperature
            pressure = calculate_cpx_opx_press(
                opx_comps=df[opx_cols], cpx_comps=df[cpx_cols],
                equationP=current_model_func_name, T=T_input)


        results_df = pd.DataFrame()
        results_df['P_kbar_calc'] = pressure

        if temperature_output is not None:
            results_df['T_K_calc'] = temperature_output
        elif T_input is not None:
            results_df['T_K_input'] = T_input # Store the input temperature if used
        else:
            results_df['T_K_input'] = np.full(len(df), np.nan) # Placeholder if no T input

        return results_df, "CpxOpx", "T_K", "P_kbar"


    def _calculate_opx_temp(self, df):
        """Encapsulates the Opx Thermometry calculation logic."""
        self.Warning.value_error.clear()
        self.Error.value_error.clear()

        # 1. MODEL SELECTION AND DATA PREP
        try:
            if self.opx_temp_model_type == 0:  # Opx-only
                model_info = MODELS_OPX_ONLY_TEMPERATURE[self.opx_temp_model_idx_oo]
                df = dm.preprocessing(df, my_output='opx_only')
                comps = {'opx_comps': df[opx_cols]}
            else:  # Opx-Liq
                model_info = MODELS_OPX_LIQ_TEMPERATURE[self.opx_temp_model_idx_ol]
                df = dm.preprocessing(df, my_output='opx_liq')
                comps = {'opx_comps': df[opx_cols], 'liq_comps': df[liq_cols]}
        except Exception as e:
            self.Error.value_error(f"Data prep failed: {str(e)}")
            return pd.DataFrame(), "", "", ""

        model_name, therm_func, needs_p, needs_h2o = model_info

        # 2. H2O HANDLING
        h2o = 0.0
        if needs_h2o:
            if self.opx_temp_fixed_h2o:
                try:
                    h2o = float(self.opx_temp_fixed_h2o_value_str)
                except ValueError:
                    self.Error.value_error("Invalid H2O value")
                    return pd.DataFrame(), "", "", ""
            elif 'H2O_Liq' in df.columns:
                h2o = df['H2O_Liq']
            else:
                self.Warning.value_error("H2O required but column missing")

        # 3. PRESSURE HANDLING - FIXED ERROR STICKING
        p_kbar = None
        if needs_p:
            if self.opx_temp_pressure_type == 0:  # From dataset
                if 'P_kbar' in df.columns:
                    p_kbar = df['P_kbar']
                else:
                    # Only show warning but continue with fixed pressure
                    self.Warning.value_error("'P_kbar' column missing - using fixed pressure value")
                    p_kbar = self.opx_temp_pressure_value
            elif self.opx_temp_pressure_type == 1:  # Fixed
                p_kbar = self.opx_temp_pressure_value
            elif self.opx_temp_pressure_type == 2:  # From model
                # No warning needed for model pressure
                pass  # Handled in calculation section

        # 4. PERFORM CALCULATION
        results = {}
        try:
            if needs_p and self.opx_temp_pressure_type == 2:  # Iterative
                calc = calculate_opx_liq_press_temp(
                    **comps,
                    equationT=therm_func,
                    equationP=baro_func,
                    H2O_Liq=h2o
                )
                results.update({
                    'T_K_calc': calc['T_K_calc'],
                    'P_kbar_calc': calc['P_kbar_calc']
                })
            else:  # Standard calculation
                temp = calculate_opx_liq_temp(
                    **comps,
                    equationT=therm_func,
                    P=p_kbar,
                    H2O_Liq=h2o
                )
                results.update({
                    'T_K_calc': temp,
                    'P_kbar_input': p_kbar if p_kbar is not None else np.nan
                })
        except Exception as e:
            self.Error.value_error(f"Calculation error: {str(e)}")
            return pd.DataFrame(), "", "", ""

        return pd.DataFrame(results), "Opx", "T_K", "P_kbar"


    def _build_opx_press_gui(self, parent_box):
        """Builds the GUI elements for Opx Barometry."""
        # For now, this can be empty or just display a message
        gui.label(parent_box, self, "Opx Barometry GUI will go here.")
        # Or, start building it out with the structure for models, temp input, H2O, etc.
        pass
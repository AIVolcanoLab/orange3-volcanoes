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
from PyQt5.QtCore import Qt

# Import all thermobar functions
from Thermobar import (
    calculate_cpx_opx_temp, calculate_cpx_opx_press, calculate_cpx_opx_press_temp,
    calculate_cpx_only_temp, calculate_cpx_only_press,
    calculate_cpx_liq_temp, calculate_cpx_liq_press,
    calculate_cpx_liq_press_temp,
    calculate_opx_only_press, calculate_opx_liq_temp,
    calculate_opx_liq_press, calculate_opx_liq_press_temp,
    calculate_amp_only_press,  calculate_amp_only_temp, calculate_amp_liq_temp,
    calculate_amp_liq_press, calculate_amp_liq_press_temp
)

# Define column names
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

amp_cols = ['SiO2_Amp', 'TiO2_Amp', 'Al2O3_Amp',
 'FeOt_Amp', 'MnO_Amp', 'MgO_Amp', 'CaO_Amp', 'Na2O_Amp', 'K2O_Amp',
 'Cr2O3_Amp', 'F_Amp', 'Cl_Amp']

## CPX-OPX models
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

## Cpx Models

MODELS_CPX_ONLY_PRESSURE = [
    ('P_Wang2021_eq1', 'P_Wang2021_eq1', False, False),
    ('P_Put2008_eq32a', 'P_Put2008_eq32a', True, False),
    ('P_Put2008_eq32b', 'P_Put2008_eq32b', True, True),
    ('P_Nimis1999_BA', 'P_Nimis1999_BA', False, False)
]

MODELS_CPX_LIQ_PRESSURE = [
    ('P_Put1996_eqP1', 'P_Put1996_eqP1', True, False),
    ('P_Mas2013_eqPalk1', 'P_Mas2013_eqPalk1', True, False),
    ('P_Put1996_eqP2', 'P_Put1996_eqP2', True, False),
    ('P_Mas2013_eqPalk2', 'P_Mas2013_eqPalk2', True, False),
    ('P_Put2003', 'P_Put2003', True, False),
    ('P_Put2008_eq30', 'P_Put2008_eq30', True, True),
    ('P_Put2008_eq31', 'P_Put2008_eq31', True, True),
    ('P_Put2008_eq32c', 'P_Put2008_eq32c', True, True),
    ('P_Mas2013_eqalk32c', 'P_Mas2013_eqalk32c', True, True),
    ('P_Mas2013_Palk2012', 'P_Mas2013_Palk2012', False, True),
    ('P_Neave2017', 'P_Neave2017', True, False)
]

MODELS_CPX_ONLY_TEMPERATURE = [
    ('T_Put2008_eq32d', 'T_Put2008_eq32d', True, False),
    ('T_Put2008_eq32d_subsol', 'T_Put2008_eq32d_subsol', True, False),
    ('T_Wang2021_eq2', 'T_Wang2021_eq2', False, False)
]

MODELS_CPX_LIQ_TEMPERATURE = [
    ('T_Put1996_eqT1', 'T_Put1996_eqT1', False, False),
    ('T_Put1996_eqT2', 'T_Put1996_eqT2', True, False),
    ('T_Put1999', 'T_Put1999', True, False),
    ('T_Put2003', 'T_Put2003', True, False),
    ('T_Put2008_eq33', 'T_Put2008_eq33', True, True),
    ('T_Put2008_eq34_cpx_sat', 'T_Put2008_eq34_cpx_sat', True, True),
    ('T_Mas2013_eqTalk1', 'T_Mas2013_eqTalk1', False, False),
    ('T_Mas2013_eqTalk2', 'T_Mas2013_eqTalk2', True, False),
    ('T_Mas2013_eqalk33', 'T_Mas2013_eqalk33', True, True),
    ('T_Mas2013_Talk2012', 'T_Mas2013_Talk2012', False, True),
    ('T_Brug2019', 'T_Brug2019', False, False)
]

##  Opx models
MODELS_OPX_ONLY_PRESSURE = [
    ('P_Put2008_eq29c', 'P_Put2008_eq29c', True, False),
]

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

MODELS_OPX_ONLY_TEMPERATURE = [
    ('None_available', 'None_available', True, True),
]

##  AMP models
# could add Kraw later.
MODELS_AMP_ONLY_PRESSURE = [
    ('P_Ridolfi2021', 'P_Ridolfi2021', False, False),
    ('P_Medard2022_RidolfiSites', 'P_Medard2022_RidolfiSites', False, False),
    ('P_Medard2022_LeakeSites', 'P_Medard2022_LeakeSites', False, False),
    ('P_Hammarstrom1986_eq1', 'P_Hammarstrom1986_eq1', False, False),
    ('P_Hammarstrom1986_eq2', 'P_Hammarstrom1986_eq2', False, False),
    ('P_Hammarstrom1986_eq3', 'P_Hammarstrom1986_eq3', False, False),
    ('P_Hollister1987', 'P_Hollister1987', False, False),
    ('P_Johnson1989', 'P_Johnson1989', False, False),
    ('P_Anderson1995', 'P_Anderson1995', True, False),
    ('P_Blundy1990', 'P_Blundy1990', False, False),
    ('P_Schmidt1992', 'P_Schmidt1992', False, False),
     ('P_Mutch2016', 'P_Schmidt1992', False, False),

]


MODELS_AMP_LIQ_PRESSURE = [
    ('P_Put2016_eq7a', 'P_Put2016_eq7a', False, True),
    ('P_Put2016_eq7b', 'P_Put2016_eq7b', False, True),
    ('P_Put2016_eq7c', 'P_Put2016_eq7c', False, True),
]

MODELS_AMP_LIQ_TEMPERATURE = [
    ('T_Put2016_eq4b', 'T_Put2016_eq4b', False, True),
    ('T_Put2016_eq4a_amp_sat', 'T_Put2016_eq4a_amp_sat', False, True),
    ('T_Put2016_eq9', 'T_Put2016_eq9', False, True),
    ('T_Put2016_eq9', 'T_Put2016_eq9', False, True),
]

MODELS_AMP_ONLY_TEMPERATURE = [
    ('T_Put2016_eq5', 'T_Put2016_eq5', False, False),
    ('T_Put2016_eq6', 'T_Put2016_eq6', True, False),
    ('T_Put2016_SiHbl', 'T_Put2016_SiHbl', False, False),
    ('T_Ridolfi2012', 'T_Ridolfi2012', True, False),
    ('T_Put2016_eq8', 'T_Put2016_eq8', True, False),
]

##

try:
    import Thermobar_onnx
    MODELS_CPX_ONLY_PRESSURE.extend([
        ('T_Jorgenson2022_Cpx_only_(ML)', 'T_Jorgenson2022_Cpx_only_onnx', False, False)
    ])
    MODELS_CPX_LIQ_TEMPERATURE.extend([
        ('T_Petrelli2020_Cpx_Liq_(ML)', 'T_Petrelli2020_Cpx_Liq_onnx', False, False),
    ])
except ImportError:
    print("You cannot use Machine Learning Models. Install Thermobar_onnx.")

class OWThermobar(OWWidget):
    name = "Thermobar Calculations"
    description = "Perform various thermobarometric calculations on mineral data."
    icon = "icons/thermobar.png"
    priority = 5
    keywords = ['Thermobar', 'Cpx', 'Opx', 'Amp', 'Liquid', 'Temperature', 'Pressure']

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        data = Output("Data", Table, dynamic=False)

    # Settings for all calculation types
    calculation_type = ContextSetting(0)
    auto_apply = Setting(True)

    # Cpx-Opx Thermometry settings
    cpx_opx_temp_model_idx = ContextSetting(0)
    cpx_opx_temp_pressure_type = ContextSetting(0)
    cpx_opx_temp_pressure_value = ContextSetting(1.0)
    cpx_opx_temp_barometer_model_idx = ContextSetting(0)
    cpx_opx_temp_fixed_h2o = ContextSetting(False)
    cpx_opx_temp_fixed_h2o_value_str = ContextSetting("1.0")

    # Cpx-Opx Barometry settings
    cpx_opx_press_model_idx = ContextSetting(0)
    cpx_opx_press_temp_type = ContextSetting(0)
    cpx_opx_press_temp_value = ContextSetting(900.0)
    cpx_opx_press_thermometer_model_idx = ContextSetting(0)
    cpx_opx_press_fixed_h2o = ContextSetting(False)
    cpx_opx_press_fixed_h2o_value_str = ContextSetting("1.0")

    # Opx-Liq Thermometry settings
    opx_liq_temp_model_idx = ContextSetting(0)
    opx_liq_temp_pressure_type = ContextSetting(0)
    opx_liq_temp_pressure_value = ContextSetting(1.0)
    opx_liq_temp_barometer_choice = ContextSetting(1)  # 0=Opx-only, 1=Opx-Liq
    opx_liq_temp_barometer_model_idx_oo = ContextSetting(0)
    opx_liq_temp_barometer_model_idx_ol = ContextSetting(0)
    opx_liq_temp_fixed_h2o = ContextSetting(False)
    opx_liq_temp_fixed_h2o_value_str = ContextSetting("1.0")

    # Opx-Liq Barometry settings
    opx_barometry_mode = ContextSetting(0)  # 0=Opx-Liq, 1=Opx-only
    opx_liq_press_model_idx = ContextSetting(0)
    opx_liq_press_temp_type = ContextSetting(0)
    opx_liq_press_temp_value = ContextSetting(900.0)
    opx_liq_press_thermometer_choice = ContextSetting(1)  # 0=Opx-only, 1=Opx-Liq
    opx_liq_press_thermometer_model_idx_oo = ContextSetting(0)
    opx_liq_press_thermometer_model_idx_ol = ContextSetting(0)
    opx_liq_press_fixed_h2o = ContextSetting(False)
    opx_liq_press_fixed_h2o_value_str = ContextSetting("1.0")

    # amp-Liq Thermometry settings
    amp_thermometry_mode = ContextSetting(0)  # 0=Amp-Liq, 1=Amp-only
    amp_liq_temp_model_idx = ContextSetting(0)
    amp_liq_temp_pressure_type = ContextSetting(0)
    amp_liq_temp_pressure_value = ContextSetting(1.0)
    amp_liq_temp_barometer_choice = ContextSetting(1)  # 0=amp-only, 1=amp-Liq
    amp_liq_temp_barometer_model_idx_ao = ContextSetting(0)
    amp_liq_temp_barometer_model_idx_al = ContextSetting(0)
    amp_liq_temp_fixed_h2o = ContextSetting(False)
    amp_liq_temp_fixed_h2o_value_str = ContextSetting("1.0")

    # amp-Liq Barometry settings
    amp_barometry_mode = ContextSetting(0)  # 0=amp-Liq, 1=amp-only
    amp_liq_press_model_idx = ContextSetting(0)
    amp_liq_press_temp_type = ContextSetting(0)
    amp_liq_press_temp_value = ContextSetting(900.0)
    amp_liq_press_thermometer_choice = ContextSetting(1)  # 0=amp-only, 1=amp-Liq
    amp_liq_press_thermometer_model_idx_ao = ContextSetting(0)
    amp_liq_press_thermometer_model_idx_al = ContextSetting(0)
    amp_liq_press_fixed_h2o = ContextSetting(False)
    amp_liq_press_fixed_h2o_value_str = ContextSetting("1.0")


    # cpx-Liq Thermometry settings
    cpx_thermometry_mode = ContextSetting(0)  # 0=Cpx-Liq, 1=Cpx-only
    cpx_liq_temp_model_idx = ContextSetting(0)
    cpx_liq_temp_pressure_type = ContextSetting(0)
    cpx_liq_temp_pressure_value = ContextSetting(1.0)
    cpx_liq_temp_barometer_choice = ContextSetting(1)  # 0=cpx-only, 1=cpx-Liq
    cpx_liq_temp_barometer_model_idx_co = ContextSetting(0)
    cpx_liq_temp_barometer_model_idx_cl = ContextSetting(0)
    cpx_liq_temp_fixed_h2o = ContextSetting(False)
    cpx_liq_temp_fixed_h2o_value_str = ContextSetting("1.0")

    # cpx-Liq Barometry settings
    cpx_barometry_mode = ContextSetting(0)  # 0=cpx-Liq, 1=cpx-only
    cpx_liq_press_model_idx = ContextSetting(0)
    cpx_liq_press_temp_type = ContextSetting(0)
    cpx_liq_press_temp_value = ContextSetting(900.0)
    cpx_liq_press_thermometer_choice = ContextSetting(1)  # 0=cpx-only, 1=cpx-Liq
    cpx_liq_press_thermometer_model_idx_co = ContextSetting(0)
    cpx_liq_press_thermometer_model_idx_cl = ContextSetting(0)
    cpx_liq_press_fixed_h2o = ContextSetting(False)
    cpx_liq_press_fixed_h2o_value_str = ContextSetting("1.0")


    resizing_enabled = False
    want_main_area = False

    class Error(OWWidget.Error):
        value_error = Msg("{}")

    class Warning(OWWidget.Warning):
        value_error = Msg("{}")

    def __init__(self):
        super().__init__()
        self.data = None

        # Info label
        gui.label(self.controlArea, self, "<i>Calculations performed using Thermobar...</i>")
        gui.separator(self.controlArea)

        # Calculation type selection
        calc_type_box = gui.vBox(self.controlArea, "Select Calculation Type")
        self.calculation_type_combo = gui.comboBox(
            calc_type_box, self, "calculation_type",
            items=[
                "None",
                "Cpx-Opx Thermometry",
                "Cpx-Opx Barometry",
                "Opx Thermometry",
                "Opx Barometry",
                "Amp Thermometry",
                "Amp Barometry",
                "Cpx Thermometry",
                "Cpx Barometry",
            ],
            callback=self._update_controls)

        gui.separator(self.controlArea)

        # Create all calculation boxes (initially hidden)
        self.cpx_opx_temp_box = gui.vBox(self.controlArea, "Cpx-Opx Thermometry Settings")
        self._build_cpx_opx_temp_gui(self.cpx_opx_temp_box)
        self.cpx_opx_temp_box.setVisible(False)

        self.cpx_opx_press_box = gui.vBox(self.controlArea, "Cpx-Opx Barometry Settings")
        self._build_cpx_opx_press_gui(self.cpx_opx_press_box)
        self.cpx_opx_press_box.setVisible(False)

        self.opx_liq_temp_box = gui.vBox(self.controlArea, "Opx Thermometry Settings")
        self._build_opx_liq_temp_gui(self.opx_liq_temp_box)
        self.opx_liq_temp_box.setVisible(False)

        self.opx_liq_press_box = gui.vBox(self.controlArea, "Opx Barometry Settings")
        self._build_opx_liq_press_gui(self.opx_liq_press_box)
        self.opx_liq_press_box.setVisible(False)

        self.amp_liq_temp_box = gui.vBox(self.controlArea, "Opx Thermometry Settings")
        self._build_amp_liq_temp_gui(self.amp_liq_temp_box)
        self.amp_liq_temp_box.setVisible(False)

        self.amp_liq_press_box = gui.vBox(self.controlArea, "Amp Barometry Settings")
        self._build_amp_liq_press_gui(self.amp_liq_press_box)
        self.amp_liq_press_box.setVisible(False)


        self.cpx_liq_temp_box = gui.vBox(self.controlArea, "Opx Thermometry Settings")
        self._build_cpx_liq_temp_gui(self.cpx_liq_temp_box)
        self.cpx_liq_temp_box.setVisible(False)

        self.cpx_liq_press_box = gui.vBox(self.controlArea, "Cpx Barometry Settings")
        self._build_cpx_liq_press_gui(self.cpx_liq_press_box)
        self.cpx_liq_press_box.setVisible(False)

        gui.auto_apply(self.buttonsArea, self)
        self._update_controls()
## Cpx_Liq functions

    ## Cpx-only and Cpx-Liq stuff

    def _build_cpx_liq_temp_gui(self, parent_box):
        """Build GUI for Cpx Thermometry"""
        # Mode selection
        mode_box = gui.hBox(parent_box)
        gui.label(mode_box, self, "Thermometry Mode:")
        self.cpx_thermometry_mode_buttons = gui.radioButtons(
            mode_box, self, "cpx_thermometry_mode",
            callback=self._update_controls)
        gui.appendRadioButton(self.cpx_thermometry_mode_buttons, "Cpx-Liq")
        gui.appendRadioButton(self.cpx_thermometry_mode_buttons, "Cpx-only")

        # Models selection
        temp_model_box = gui.vBox(parent_box, "Models")
        self.cpx_liq_temp_models_combo = gui.comboBox(
            temp_model_box, self, "cpx_liq_temp_model_idx",
            items=[],  # Populated later
            callback=self._update_controls)

        # Pressure settings
        self.cpx_liq_temp_pressure_box = gui.radioButtons(
            parent_box, self, "cpx_liq_temp_pressure_type", box="Pressure Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.cpx_liq_temp_pressure_box, "Dataset as Pressure (kbar)")

        rb_fixed_p = gui.appendRadioButton(self.cpx_liq_temp_pressure_box, "Fixed Pressure")


        self.cpx_liq_temp_pressure_value_box = gui.doubleSpin(
            gui.indentedBox(self.cpx_liq_temp_pressure_box, gui.checkButtonOffsetHint(rb_fixed_p)), self,
            "cpx_liq_temp_pressure_value", 0, 1000, step=1.0, label="Pressure Value (kbar)",
            alignment=Qt.AlignRight, callback=self.commit.deferred, controlWidth=80, decimals=0)

        rb_model_p = gui.appendRadioButton(self.cpx_liq_temp_pressure_box, "Model as Pressure")
        model_as_p_box = gui.indentedBox(self.cpx_liq_temp_pressure_box, gui.checkButtonOffsetHint(rb_model_p))

        self.cpx_liq_temp_barometer_choice_buttons = gui.radioButtons(
            model_as_p_box, self, "cpx_liq_temp_barometer_choice",
            callback=self._update_controls)

        rb_co = gui.appendRadioButton(self.cpx_liq_temp_barometer_choice_buttons, "Use Cpx-only barometer")
        self.cpx_liq_temp_barometer_model_box_co = gui.comboBox(
            gui.indentedBox(self.cpx_liq_temp_barometer_choice_buttons, gui.checkButtonOffsetHint(rb_co)),
            self, "cpx_liq_temp_barometer_model_idx_co",
            items=[m[0] for m in MODELS_CPX_ONLY_PRESSURE],
            callback=self._update_controls)

        rb_cl = gui.appendRadioButton(self.cpx_liq_temp_barometer_choice_buttons, "Use Cpx-Liq barometer")
        self.cpx_liq_temp_barometer_model_box_cl = gui.comboBox(
            gui.indentedBox(self.cpx_liq_temp_barometer_choice_buttons, gui.checkButtonOffsetHint(rb_cl)),
            self, "cpx_liq_temp_barometer_model_idx_cl",
            items=[m[0] for m in MODELS_CPX_LIQ_PRESSURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.cpx_liq_temp_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "cpx_liq_temp_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.cpx_liq_temp_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "cpx_liq_temp_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _build_cpx_liq_press_gui(self, parent_box):
        """Build GUI for Cpx Barometry"""
        # Mode selection
        mode_box = gui.hBox(parent_box)
        gui.label(mode_box, self, "Barometry Mode:")
        self.cpx_barometry_mode_buttons = gui.radioButtons(
            mode_box, self, "cpx_barometry_mode",
            callback=self._update_controls)
        gui.appendRadioButton(self.cpx_barometry_mode_buttons, "Cpx-Liq")
        gui.appendRadioButton(self.cpx_barometry_mode_buttons, "Cpx-only")

        # Models selection
        press_model_box = gui.vBox(parent_box, "Models")
        self.cpx_liq_press_models_combo = gui.comboBox(
            press_model_box, self, "cpx_liq_press_model_idx",
            items=[],  # Populated later
            callback=self._update_controls)

        # Temperature settings
        self.cpx_liq_press_temp_box = gui.radioButtons(
            parent_box, self, "cpx_liq_press_temp_type", box="Temperature Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.cpx_liq_press_temp_box, "Dataset as Temperature (K)")

        rb_fixed_t = gui.appendRadioButton(self.cpx_liq_press_temp_box, "Fixed Temperature")
        self.cpx_liq_press_temp_value_box = gui.doubleSpin(
            gui.indentedBox(self.cpx_liq_press_temp_box, gui.checkButtonOffsetHint(rb_fixed_t)), self,
            "cpx_liq_press_temp_value", 500.0, 2000.0, step=1.0, label="Temperature Value (K)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=0)

        rb_model_t = gui.appendRadioButton(self.cpx_liq_press_temp_box, "Model as Temperature")
        model_as_t_box = gui.indentedBox(self.cpx_liq_press_temp_box, gui.checkButtonOffsetHint(rb_model_t))

        self.cpx_liq_press_thermometer_choice_buttons = gui.radioButtons(
            model_as_t_box, self, "cpx_liq_press_thermometer_choice",
            callback=self._update_controls)

        rb_co = gui.appendRadioButton(self.cpx_liq_press_thermometer_choice_buttons, "Use Cpx-only thermometer")
        self.cpx_liq_press_thermometer_model_box_co = gui.comboBox(
            gui.indentedBox(self.cpx_liq_press_thermometer_choice_buttons, gui.checkButtonOffsetHint(rb_co)),
            self, "cpx_liq_press_thermometer_model_idx_co",
            items=[m[0] for m in MODELS_CPX_ONLY_TEMPERATURE],
            callback=self._update_controls)

        rb_cl = gui.appendRadioButton(self.cpx_liq_press_thermometer_choice_buttons, "Use Cpx-Liq thermometer")
        self.cpx_liq_press_thermometer_model_box_cl = gui.comboBox(
            gui.indentedBox(self.cpx_liq_press_thermometer_choice_buttons, gui.checkButtonOffsetHint(rb_cl)),
            self, "cpx_liq_press_thermometer_model_idx_cl",
            items=[m[0] for m in MODELS_CPX_LIQ_TEMPERATURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.cpx_liq_press_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "cpx_liq_press_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.cpx_liq_press_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "cpx_liq_press_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _update_cpx_liq_temp_controls(self):
        """Update controls for Cpx-Liq/Cpx-only Thermometry"""
        # Get the appropriate model list based on current mode
        if hasattr(self, 'cpx_thermometry_mode') and self.cpx_thermometry_mode == 1:  # Cpx-only mode
            model_list = MODELS_CPX_ONLY_TEMPERATURE
        else:  # Default to Cpx-Liq mode
            model_list = MODELS_CPX_LIQ_TEMPERATURE

        _, _, requires_press, requires_h2o = model_list[self.cpx_liq_temp_model_idx]

        # Enable/disable pressure input group
        self.cpx_liq_temp_pressure_box.setEnabled(requires_press)

        # Enable/disable pressure value box
        self.cpx_liq_press_temp_value_box.setEnabled(
            requires_press and self.cpx_liq_temp_pressure_type == 1)

        # Enable/disable barometer choice and model boxes
        model_as_p_active = requires_press and self.cpx_liq_temp_pressure_type == 2
        self.cpx_liq_temp_barometer_choice_buttons.setEnabled(model_as_p_active)

        if model_as_p_active:
            self.cpx_liq_temp_barometer_model_box_co.setEnabled(
                self.cpx_liq_temp_barometer_choice == 0)
            self.cpx_liq_temp_barometer_model_box_cl.setEnabled(
                self.cpx_liq_temp_barometer_choice == 1)
        else:
            self.cpx_liq_temp_barometer_model_box_co.setEnabled(False)
            self.cpx_liq_temp_barometer_model_box_cl.setEnabled(False)

        # Enable/disable H2O controls
        self.cpx_liq_temp_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.cpx_liq_temp_fixed_h2o_input.setEnabled(
            requires_h2o and self.cpx_liq_temp_fixed_h2o)

    def _update_cpx_liq_press_controls(self):
        """Update controls for Cpx-Liq/Cpx-only Barometry"""
        # Get the appropriate model list based on current mode
        if hasattr(self, 'cpx_barometry_mode') and self.cpx_barometry_mode == 1:  # Cpx-only mode
            model_list = MODELS_CPX_ONLY_PRESSURE
        else:  # Default to Cpx-Liq mode
            model_list = MODELS_CPX_LIQ_PRESSURE

        _, _, requires_temp, requires_h2o = model_list[self.cpx_liq_press_model_idx]

        # Enable/disable temperature input group
        self.cpx_liq_press_temp_box.setEnabled(requires_temp)

        # Enable/disable temperature value box
        self.cpx_liq_press_temp_value_box.setEnabled(
            requires_temp and self.cpx_liq_press_temp_type == 1)

        # Enable/disable thermometer choice and model boxes
        model_as_t_active = requires_temp and self.cpx_liq_press_temp_type == 2
        self.cpx_liq_press_thermometer_choice_buttons.setEnabled(model_as_t_active)

        if model_as_t_active:
            self.cpx_liq_press_thermometer_model_box_co.setEnabled(
                self.cpx_liq_press_thermometer_choice == 0)
            self.cpx_liq_press_thermometer_model_box_cl.setEnabled(
                self.cpx_liq_press_thermometer_choice == 1)
        else:
            self.cpx_liq_press_thermometer_model_box_co.setEnabled(False)
            self.cpx_liq_press_thermometer_model_box_cl.setEnabled(False)

        # Enable/disable H2O controls
        self.cpx_liq_press_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.cpx_liq_press_fixed_h2o_input.setEnabled(
            requires_h2o and self.cpx_liq_press_fixed_h2o)











    def _calculate_cpx_liq_press(self, df):
        """Calculate Cpx-Liq or Cpx-only pressures based on current mode"""
        # Determine which model set to use
        if hasattr(self, 'cpx_barometry_mode') and self.cpx_barometry_mode == 1:  # Cpx-only mode
            model_list = MODELS_CPX_ONLY_PRESSURE
            mode_name = "Cpx-only Barometry"
            print(f"DEBUG: Using Cpx-only mode with model index {self.cpx_liq_press_model_idx}")
        else:  # Default to Cpx-Liq mode
            model_list = MODELS_CPX_LIQ_PRESSURE
            mode_name = "Cpx-Liq Barometry"
            print(f"DEBUG: Using Cpx-Liq mode with model index {self.cpx_liq_press_model_idx}")

        _, current_model_func_name, requires_temp, requires_h2o = model_list[self.cpx_liq_press_model_idx]
        print(f"DEBUG: Selected model function: {current_model_func_name}")

        # Determine thermometer function if using model temperature
        if requires_temp and self.cpx_liq_press_temp_type == 2:
            if self.cpx_liq_press_thermometer_choice == 0:  # Cpx-only
                current_thermometer_func_name = MODELS_CPX_ONLY_TEMPERATURE[self.cpx_liq_press_thermometer_model_idx_co][1]
                print(f"DEBUG: Using Cpx-only thermometer model: {current_thermometer_func_name}")
            else:  # Cpx-Liq
                current_thermometer_func_name = MODELS_CPX_LIQ_TEMPERATURE[self.cpx_liq_press_thermometer_model_idx_cl][1]
                print(f"DEBUG: Using Cpx-Liq thermometer model: {current_thermometer_func_name}")

        df = dm.preprocessing(df, my_output='cpx_liq')

        water = self._get_h2o_value(df, requires_h2o,
                                self.cpx_liq_press_fixed_h2o,
                                self.cpx_liq_press_fixed_h2o_value_str,
                                mode_name)
        if water is None:
            return pd.DataFrame(), "", "", ""

        T_input = self._get_temperature_value(df, requires_temp,
                                            self.cpx_liq_press_temp_type,
                                            self.cpx_liq_press_temp_value,
                                            mode_name)

        pressure = None
        temperature_output = None

        if requires_temp and self.cpx_liq_press_temp_type == 2:  # Model as Temperature
            if self.cpx_barometry_mode == 1:  # Cpx-only mode
                calc = calculate_cpx_liq_press_temp(
                    cpx_comps=df[cpx_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name)
            else:  # Cpx-Liq mode
                calc = calculate_cpx_liq_press_temp(
                    cpx_comps=df[cpx_cols], liq_comps=df[liq_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name,
                    H2O_Liq=water)
            pressure = calc['P_kbar_calc']
            temperature_output = calc['T_K_calc']
        else:  # Fixed or dataset temperature
            if self.cpx_barometry_mode == 1:  # Cpx-only mode
                pressure_result = calculate_cpx_only_press(
                    cpx_comps=df[cpx_cols],
                    equationP=current_model_func_name,
                    T=T_input)
                # Handle cases where the function returns a DataFrame (like Ridolfi2021)
                if isinstance(pressure_result, pd.DataFrame):
                    pressure = pressure_result['P_kbar_calc']
                else:
                    pressure = pressure_result
            else:  # Cpx-Liq mode
                pressure = calculate_cpx_liq_press(
                    cpx_comps=df[cpx_cols], liq_comps=df[liq_cols],
                    equationP=current_model_func_name,
                    T=T_input,
                    H2O_Liq=water)

        results_df = pd.DataFrame()
        results_df['P_kbar_calc'] = pressure

        if temperature_output is not None:
            results_df['T_K_calc'] = temperature_output
        elif T_input is not None:
            results_df['T_K_input'] = T_input
        else:
            results_df['T_K_input'] = np.full(len(df), np.nan)

        return results_df, "CpxLiq", "T_K", "P_kbar"

    def _calculate_cpx_liq_temp(self, df):
        """Calculate Cpx-Liq or Cpx-only temperatures based on current mode"""



        # Determine which model set to use
        if hasattr(self, 'cpx_thermometry_mode') and self.cpx_thermometry_mode == 1:  # Cpx-only mode
            model_list = MODELS_CPX_ONLY_TEMPERATURE
            mode_name = "Cpx-only Thermometry"
        else:  # Default to Cpx-Liq mode
            model_list = MODELS_CPX_LIQ_TEMPERATURE
            mode_name = "Cpx-Liq Thermometry"

        _, current_model_func_name, requires_pressure, requires_h2o = model_list[self.cpx_liq_temp_model_idx]

        print(">>> Entered _calculate_cpx_liq_temp")
        print(f"Model index: {self.cpx_liq_temp_model_idx}")
        print(f"Mode: {'Cpx-only' if self.cpx_thermometry_mode == 1 else 'Cpx-Liq'}")
        print(f"Returned df length: {len(df)}")
        print(f"Requires pressure: {requires_pressure}, requires H2O: {requires_h2o}")


        # Determine barometer function if using model pressure
        if requires_pressure and self.cpx_liq_temp_pressure_type == 2:
            if self.cpx_liq_temp_barometer_choice == 0:  # Cpx-only
                current_barometer_func_name = MODELS_CPX_ONLY_PRESSURE[self.cpx_liq_temp_barometer_model_idx_co][1]
            else:  # Cpx-Liq
                current_barometer_func_name = MODELS_CPX_LIQ_PRESSURE[self.cpx_liq_temp_barometer_model_idx_cl][1]

        df = dm.preprocessing(df, my_output='cpx_liq')

        water = self._get_h2o_value(df, requires_h2o,
                                self.cpx_liq_temp_fixed_h2o,
                                self.cpx_liq_temp_fixed_h2o_value_str,
                                mode_name)
        if water is None: return pd.DataFrame(), "", "", ""

        P_input = self._get_pressure_value(df, requires_pressure,
                                        self.cpx_liq_temp_pressure_type,
                                        self.cpx_liq_temp_pressure_value,
                                        mode_name)


        temperature = None
        pressure_output = None

        if requires_pressure and self.cpx_liq_temp_pressure_type == 2:  # Model as Pressure
            if self.cpx_thermometry_mode == 1:  # Cpx-only mode
                calc = calculate_cpx_only_press_temp(
                    cpx_comps=df[cpx_cols],
                    equationT=current_model_func_name,
                    equationP=current_barometer_func_name)
            else:  # Cpx-Liq mode
                calc = calculate_cpx_liq_press_temp(
                    cpx_comps=df[cpx_cols], liq_comps=df[liq_cols],
                    equationT=current_model_func_name,
                    equationP=current_barometer_func_name,
                    H2O_Liq=water)
            temperature = calc['T_K_calc']
            pressure_output = calc['P_kbar_calc']
        else:  # Fixed or dataset pressure
            if self.cpx_thermometry_mode == 1:  # Cpx-only mode
                temperature = calculate_cpx_only_temp(
                    cpx_comps=df[cpx_cols],
                    equationT=current_model_func_name,
                    P=P_input)
            else:  # Cpx-Liq mode
                temperature = calculate_cpx_liq_temp(
                    cpx_comps=df[cpx_cols], liq_comps=df[liq_cols],
                    equationT=current_model_func_name,
                    P=P_input,
                    H2O_Liq=water)

        results_df = pd.DataFrame()
        results_df['T_K_calc'] = temperature

        if pressure_output is not None:
            results_df['P_kbar_calc'] = pressure_output
        elif P_input is not None:
            results_df['P_kbar_input'] = P_input
        else:
            results_df['P_kbar_input'] = np.full(len(df), np.nan)

        print(">>> Result columns:", results_df.columns)

        return results_df, "CpxLiq", "T_K", "P_kbar"



    ## Opx-Cpx functions

    def _build_cpx_opx_temp_gui(self, parent_box):
        """Build GUI for Cpx-Opx Thermometry"""
        # Models selection
        temp_model_box = gui.vBox(parent_box, "Models")
        self.cpx_opx_temp_models_combo = gui.comboBox(
            temp_model_box, self, "cpx_opx_temp_model_idx",
            items=[m[0] for m in MODELS_CPX_OPX_TEMP],
            callback=self._update_controls)

        # Pressure settings
        self.cpx_opx_temp_pressure_box = gui.radioButtons(
            parent_box, self, "cpx_opx_temp_pressure_type", box="Pressure Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.cpx_opx_temp_pressure_box, "Dataset as Pressure (kbar)")

        rb_fixed_p = gui.appendRadioButton(self.cpx_opx_temp_pressure_box, "Fixed Pressure")
        self.cpx_opx_temp_pressure_value_box = gui.doubleSpin(
            gui.indentedBox(self.cpx_opx_temp_pressure_box, gui.checkButtonOffsetHint(rb_fixed_p)), self,
            "cpx_opx_temp_pressure_value", 1.0, 10000.0, step=0.1, label="Pressure Value (kbar)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=1)

        rb_model_p = gui.appendRadioButton(self.cpx_opx_temp_pressure_box, "Model as Pressure")
        model_as_p_box = gui.indentedBox(self.cpx_opx_temp_pressure_box, gui.checkButtonOffsetHint(rb_model_p))

        self.cpx_opx_temp_barometer_model_box = gui.comboBox(
            model_as_p_box, self, "cpx_opx_temp_barometer_model_idx",
            items=[m[0] for m in MODELS_CPX_OPX_PRESSURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.cpx_opx_temp_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "cpx_opx_temp_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.cpx_opx_temp_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "cpx_opx_temp_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)

    def _build_cpx_opx_press_gui(self, parent_box):
        """Build GUI for Cpx-Opx Barometry"""
        # Models selection
        press_model_box = gui.vBox(parent_box, "Models")
        self.cpx_opx_press_models_combo = gui.comboBox(
            press_model_box, self, "cpx_opx_press_model_idx",
            items=[m[0] for m in MODELS_CPX_OPX_PRESSURE],
            callback=self._update_controls)

        # Temperature settings
        self.cpx_opx_press_temp_box = gui.radioButtons(
            parent_box, self, "cpx_opx_press_temp_type", box="Temperature Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.cpx_opx_press_temp_box, "Dataset as Temperature (K)")

        rb_fixed_t = gui.appendRadioButton(self.cpx_opx_press_temp_box, "Fixed Temperature")
        self.cpx_opx_press_temp_value_box = gui.doubleSpin(
            gui.indentedBox(self.cpx_opx_press_temp_box, gui.checkButtonOffsetHint(rb_fixed_t)), self,
            "cpx_opx_press_temp_value", 500.0, 2000.0, step=1.0, label="Temperature Value (K)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=0)

        rb_model_t = gui.appendRadioButton(self.cpx_opx_press_temp_box, "Model as Temperature")
        model_as_t_box = gui.indentedBox(self.cpx_opx_press_temp_box, gui.checkButtonOffsetHint(rb_model_t))

        self.cpx_opx_press_thermometer_model_box = gui.comboBox(
            model_as_t_box, self, "cpx_opx_press_thermometer_model_idx",
            items=[m[0] for m in MODELS_CPX_OPX_TEMP],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.cpx_opx_press_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "cpx_opx_press_fixed_h2o", "Fixed H₂O", callback=self._update_controls)

        self.cpx_opx_press_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "cpx_opx_press_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _update_cpx_opx_temp_controls(self):
        """Update controls for Cpx-Opx Thermometry"""
        _, _, requires_pressure, requires_h2o = MODELS_CPX_OPX_TEMP[self.cpx_opx_temp_model_idx]

        # Enable/disable pressure radio group
        self.cpx_opx_temp_pressure_box.setEnabled(requires_pressure)

        # Enable/disable pressure value box
        self.cpx_opx_temp_pressure_value_box.setEnabled(
            requires_pressure and self.cpx_opx_temp_pressure_type == 1)

        # Enable/disable barometer model box
        self.cpx_opx_temp_barometer_model_box.setEnabled(
            requires_pressure and self.cpx_opx_temp_pressure_type == 2)

        # Enable/disable H2O input
        self.cpx_opx_temp_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.cpx_opx_temp_fixed_h2o_input.setEnabled(requires_h2o and self.cpx_opx_temp_fixed_h2o)

    def _update_cpx_opx_press_controls(self):
        """Update controls for Cpx-Opx Barometry"""
        _, _, requires_temp, requires_h2o = MODELS_CPX_OPX_PRESSURE[self.cpx_opx_press_model_idx]

        # Enable/disable temperature radio group
        self.cpx_opx_press_temp_box.setEnabled(requires_temp)

        # Enable/disable temperature value box
        self.cpx_opx_press_temp_value_box.setEnabled(
            requires_temp and self.cpx_opx_press_temp_type == 1)

        # Enable/disable thermometer model box
        self.cpx_opx_press_thermometer_model_box.setEnabled(
            requires_temp and self.cpx_opx_press_temp_type == 2)

        # Enable/disable H2O input
        self.cpx_opx_press_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.cpx_opx_press_fixed_h2o_input.setEnabled(requires_h2o and self.cpx_opx_press_fixed_h2o)



    def _calculate_cpx_opx_press(self, df):
        """Calculate Cpx-Opx pressures"""
        _, current_model_func_name, requires_temp, requires_h2o = MODELS_CPX_OPX_PRESSURE[self.cpx_opx_press_model_idx]
        current_thermometer_func_name = MODELS_CPX_OPX_TEMP[self.cpx_opx_press_thermometer_model_idx][1]

        df = dm.preprocessing(df, my_output='cpx_opx')

        water = self._get_h2o_value(df, requires_h2o,
                                self.cpx_opx_press_fixed_h2o,
                                self.cpx_opx_press_fixed_h2o_value_str,
                                "Cpx-Opx Barometry")
        if water is None:
            return pd.DataFrame(), "", "", ""

        T_input = self._get_temperature_value(df, requires_temp,
                                            self.cpx_opx_press_temp_type,
                                            self.cpx_opx_press_temp_value,
                                            "Cpx-Opx Barometry")

        # Initialize results
        results_df = pd.DataFrame()

        if requires_temp and self.cpx_opx_press_temp_type == 2:  # Model as Temperature
            try:
                calc = calculate_cpx_opx_press_temp(
                    opx_comps=df[opx_cols],
                    cpx_comps=df[cpx_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name)

                # Ensure we're getting the expected columns
                if 'P_kbar_calc' in calc:
                    results_df['P_kbar_calc'] = calc['P_kbar_calc']
                else:
                    self.Error.value_error("Pressure calculation failed - no 'P_kbar_calc' in results")
                    return pd.DataFrame(), "", "", ""

                if 'T_K_calc' in calc:
                    results_df['T_K_calc'] = calc['T_K_calc']
                else:
                    results_df['T_K_calc'] = np.nan  # Fill with NaN if missing

            except Exception as e:
                self.Error.value_error(f"Calculation failed: {str(e)}")
                return pd.DataFrame(), "", "", ""

        else:  # Fixed or dataset temperature
            try:
                pressure = calculate_cpx_opx_press(
                    opx_comps=df[opx_cols],
                    cpx_comps=df[cpx_cols],
                    equationP=current_model_func_name,
                    T=T_input)

                results_df['P_kbar_calc'] = pressure

                # Store the input temperature if provided
                if T_input is not None:
                    if isinstance(T_input, (int, float)):
                        results_df['T_K_input'] = np.full(len(df), T_input)
                    else:  # Assume it's a pandas Series
                        results_df['T_K_input'] = T_input.values
                else:
                    results_df['T_K_input'] = np.nan

            except Exception as e:
                self.Error.value_error(f"Pressure calculation failed: {str(e)}")
                return pd.DataFrame(), "", "", ""

        return results_df, "CpxOpx", "T_K", "P_kbar"

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




    ## Opx Liq and Opx-only stuff

    def _build_opx_liq_temp_gui(self, parent_box):
        """Build GUI for Opx-Liq Thermometry"""
        # Models selection
        temp_model_box = gui.vBox(parent_box, "Models")
        self.opx_liq_temp_models_combo = gui.comboBox(
            temp_model_box, self, "opx_liq_temp_model_idx",
            items=[m[0] for m in MODELS_OPX_LIQ_TEMPERATURE],
            callback=self._update_controls)

        # Pressure settings
        pressure_box = gui.radioButtons(
            parent_box, self, "opx_liq_temp_pressure_type", box="Pressure Input",
            callback=self._update_controls)
        gui.appendRadioButton(pressure_box, "Dataset as Pressure (kbar)")

        rb_fixed_p = gui.appendRadioButton(pressure_box, "Fixed Pressure")
        self.opx_liq_temp_pressure_value_box = gui.doubleSpin(
            gui.indentedBox(pressure_box, gui.checkButtonOffsetHint(rb_fixed_p)), self,
            "opx_liq_temp_pressure_value", 1.0, 10000.0, step=0.1, label="Pressure Value (kbar)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=1)

        rb_model_p = gui.appendRadioButton(pressure_box, "Model as Pressure")
        model_as_p_box = gui.indentedBox(pressure_box, gui.checkButtonOffsetHint(rb_model_p))

        # Barometer choice (Opx-only or Opx-Liq)
        self.opx_liq_temp_barometer_choice_buttons = gui.radioButtons(
            model_as_p_box, self, "opx_liq_temp_barometer_choice",
            callback=self._update_controls)

        rb_oo = gui.appendRadioButton(self.opx_liq_temp_barometer_choice_buttons, "Use Opx-only barometer")
        self.opx_liq_temp_barometer_model_box_oo = gui.comboBox(
            gui.indentedBox(self.opx_liq_temp_barometer_choice_buttons, gui.checkButtonOffsetHint(rb_oo)),
            self, "opx_liq_temp_barometer_model_idx_oo",
            items=[m[0] for m in MODELS_OPX_ONLY_PRESSURE],
            callback=self._update_controls)

        rb_ol = gui.appendRadioButton(self.opx_liq_temp_barometer_choice_buttons, "Use Opx-Liq barometer")
        self.opx_liq_temp_barometer_model_box_ol = gui.comboBox(
            gui.indentedBox(self.opx_liq_temp_barometer_choice_buttons, gui.checkButtonOffsetHint(rb_ol)),
            self, "opx_liq_temp_barometer_model_idx_ol",
            items=[m[0] for m in MODELS_OPX_LIQ_PRESSURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.opx_liq_temp_fixed_h2o_checkbox = gui.checkBox(h2o_box, self, "opx_liq_temp_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.opx_liq_temp_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "opx_liq_temp_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _build_opx_liq_press_gui(self, parent_box):
        """Build GUI for Opx Barometry"""
        # Mode selection
        mode_box = gui.hBox(parent_box)
        gui.label(mode_box, self, "Barometry Mode:")
        self.opx_barometry_mode_buttons = gui.radioButtons(
            mode_box, self, "opx_barometry_mode",
            callback=self._update_controls)
        gui.appendRadioButton(self.opx_barometry_mode_buttons, "Opx-Liq")
        gui.appendRadioButton(self.opx_barometry_mode_buttons, "Opx-only")

        # Models selection (initially empty, will be populated in _update_controls)
        press_model_box = gui.vBox(parent_box, "Models")
        self.opx_liq_press_models_combo = gui.comboBox(
            press_model_box, self, "opx_liq_press_model_idx",
            items=[],  # Start empty
            callback=self._update_controls)

        # Temperature settings
        self.opx_liq_press_temp_box = gui.radioButtons(
            parent_box, self, "opx_liq_press_temp_type", box="Temperature Input",
            callback=self._update_controls)

        rb_fixed_t = gui.appendRadioButton(self.opx_liq_press_temp_box, "Fixed Temperature")
        self.opx_liq_press_temp_value_box = gui.doubleSpin(
            gui.indentedBox(self.opx_liq_press_temp_box, gui.checkButtonOffsetHint(rb_fixed_t)), self,
            "opx_liq_press_temp_value", 500.0, 2000.0, step=1.0, label="Temperature Value (K)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=0)

        rb_model_t = gui.appendRadioButton(self.opx_liq_press_temp_box, "Model as Temperature")
        model_as_t_box = gui.indentedBox(self.opx_liq_press_temp_box, gui.checkButtonOffsetHint(rb_model_t))

        # Thermometer choice (Opx-only or Opx-Liq)
        self.opx_liq_press_thermometer_choice_buttons = gui.radioButtons(
            model_as_t_box, self, "opx_liq_press_thermometer_choice",
            callback=self._update_controls)

        rb_oo = gui.appendRadioButton(self.opx_liq_press_thermometer_choice_buttons, "Use Opx-only thermometer")
        self.opx_liq_press_thermometer_model_box_oo = gui.comboBox(
            gui.indentedBox(self.opx_liq_press_thermometer_choice_buttons, gui.checkButtonOffsetHint(rb_oo)),
            self, "opx_liq_press_thermometer_model_idx_oo",
            items=[m[0] for m in MODELS_OPX_ONLY_TEMPERATURE],
            callback=self._update_controls)

        rb_ol = gui.appendRadioButton(self.opx_liq_press_thermometer_choice_buttons, "Use Opx-Liq thermometer")
        self.opx_liq_press_thermometer_model_box_ol = gui.comboBox(
            gui.indentedBox(self.opx_liq_press_thermometer_choice_buttons, gui.checkButtonOffsetHint(rb_ol)),
            self, "opx_liq_press_thermometer_model_idx_ol",
            items=[m[0] for m in MODELS_OPX_LIQ_TEMPERATURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.opx_liq_press_fixed_h2o_checkbox = gui.checkBox(h2o_box, self, "opx_liq_press_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.opx_liq_press_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "opx_liq_press_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)

    def _update_opx_liq_temp_controls(self):
        """Update controls for Opx-Liq Thermometry"""
        _, _, requires_pressure, requires_h2o = MODELS_OPX_LIQ_TEMPERATURE[self.opx_liq_temp_model_idx]

        # Enable/disable pressure value box
        self.opx_liq_temp_pressure_value_box.setEnabled(
            requires_pressure and self.opx_liq_temp_pressure_type == 1)

        # Enable/disable barometer choice and model boxes
        model_as_p_active = requires_pressure and self.opx_liq_temp_pressure_type == 2
        self.opx_liq_temp_barometer_choice_buttons.setEnabled(model_as_p_active)

        if model_as_p_active:
            self.opx_liq_temp_barometer_model_box_oo.setEnabled(
                self.opx_liq_temp_barometer_choice == 0)
            self.opx_liq_temp_barometer_model_box_ol.setEnabled(
                self.opx_liq_temp_barometer_choice == 1)

        # Enable/disable H2O input
        self.opx_liq_temp_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.opx_liq_temp_fixed_h2o_input.setEnabled(
            requires_h2o and self.opx_liq_temp_fixed_h2o)

    def _update_opx_liq_press_controls(self):
        """Update controls for Opx-Liq/Opx-only Barometry"""
        # Get the appropriate model list based on current mode
        if hasattr(self, 'opx_barometry_mode') and self.opx_barometry_mode == 1:  # Opx-only mode
            model_list = MODELS_OPX_ONLY_PRESSURE
        else:  # Default to Opx-Liq mode
            model_list = MODELS_OPX_LIQ_PRESSURE

        _, _, requires_temp, requires_h2o = model_list[self.opx_liq_press_model_idx]

        # Enable/disable temperature value box
        self.opx_liq_press_temp_box.setEnabled(requires_temp)
        self.opx_liq_press_temp_value_box.setEnabled(
            requires_temp and self.opx_liq_press_temp_type == 1)

        # Enable/disable thermometer choice and model boxes
        model_as_t_active = requires_temp and self.opx_liq_press_temp_type == 2
        self.opx_liq_press_thermometer_choice_buttons.setEnabled(model_as_t_active)

        if model_as_t_active:
            self.opx_liq_press_thermometer_model_box_oo.setEnabled(
                self.opx_liq_press_thermometer_choice == 0)
            self.opx_liq_press_thermometer_model_box_ol.setEnabled(
                self.opx_liq_press_thermometer_choice == 1)

        # Enable/disable H2O input
        self.opx_liq_press_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.opx_liq_press_fixed_h2o_input.setEnabled(
            requires_h2o and self.opx_liq_press_fixed_h2o)

    def _calculate_opx_liq_temp(self, df):
        """Calculate Opx-Liq temperatures"""
        _, current_model_func_name, requires_pressure, requires_h2o = MODELS_OPX_LIQ_TEMPERATURE[self.opx_liq_temp_model_idx]

        # Determine barometer function if using model pressure
        if requires_pressure and self.opx_liq_temp_pressure_type == 2:
            if self.opx_liq_temp_barometer_choice == 0:  # Opx-only
                current_barometer_func_name = MODELS_OPX_ONLY_PRESSURE[self.opx_liq_temp_barometer_model_idx_oo][1]
            else:  # Opx-Liq
                current_barometer_func_name = MODELS_OPX_LIQ_PRESSURE[self.opx_liq_temp_barometer_model_idx_ol][1]

        df = dm.preprocessing(df, my_output='opx_liq')

        water = self._get_h2o_value(df, requires_h2o,
                                   self.opx_liq_temp_fixed_h2o,
                                   self.opx_liq_temp_fixed_h2o_value_str,
                                   "Opx-Liq Thermometry")
        if water is None: return pd.DataFrame(), "", "", ""

        P_input = self._get_pressure_value(df, requires_pressure,
                                         self.opx_liq_temp_pressure_type,
                                         self.opx_liq_temp_pressure_value,
                                         "Opx-Liq Thermometry")

        temperature = None
        pressure_output = None

        if requires_pressure and self.opx_liq_temp_pressure_type == 2:  # Model as Pressure
            calc = calculate_opx_liq_press_temp(
                opx_comps=df[opx_cols], liq_comps=df[liq_cols],
                equationT=current_model_func_name, equationP=current_barometer_func_name,
                H2O_Liq=water)
            temperature = calc['T_K_calc']
            pressure_output = calc['P_kbar_calc']
        else:  # Fixed or dataset pressure
            temperature = calculate_opx_liq_temp(
                opx_comps=df[opx_cols], liq_comps=df[liq_cols],
                equationT=current_model_func_name, P=P_input, H2O_Liq=water)

        results_df = pd.DataFrame()
        results_df['T_K_calc'] = temperature

        if pressure_output is not None:
            results_df['P_kbar_calc'] = pressure_output
        elif P_input is not None:
            results_df['P_kbar_input'] = P_input
        else:
            results_df['P_kbar_input'] = np.full(len(df), np.nan)

        return results_df, "OpxLiq", "T_K", "P_kbar"

    def _calculate_opx_liq_press(self, df):
        """Calculate Opx-Liq or Opx-only pressures based on current mode"""
        # Determine which model set to use
        if hasattr(self, 'opx_barometry_mode') and self.opx_barometry_mode == 1:  # Opx-only mode
            model_list = MODELS_OPX_ONLY_PRESSURE
            mode_name = "Opx-only Barometry"
        else:  # Default to Opx-Liq mode
            model_list = MODELS_OPX_LIQ_PRESSURE
            mode_name = "Opx-Liq Barometry"

        _, current_model_func_name, requires_temp, requires_h2o = model_list[self.opx_liq_press_model_idx]

        # Determine thermometer function if using model temperature
        if requires_temp and self.opx_liq_press_temp_type == 2:
            if self.opx_liq_press_thermometer_choice == 0:  # Opx-only
                current_thermometer_func_name = MODELS_OPX_ONLY_TEMPERATURE[self.opx_liq_press_thermometer_model_idx_oo][1]
            else:  # Opx-Liq
                current_thermometer_func_name = MODELS_OPX_LIQ_TEMPERATURE[self.opx_liq_press_thermometer_model_idx_ol][1]

        df = dm.preprocessing(df, my_output='opx_liq')

        water = self._get_h2o_value(df, requires_h2o,
                                self.opx_liq_press_fixed_h2o,
                                self.opx_liq_press_fixed_h2o_value_str,
                                mode_name)
        if water is None:
            return pd.DataFrame(), "", "", ""

        T_input = self._get_temperature_value(df, requires_temp,
                                            self.opx_liq_press_temp_type,
                                            self.opx_liq_press_temp_value,
                                            mode_name)

        pressure = None
        temperature_output = None

        if requires_temp and self.opx_liq_press_temp_type == 2:  # Model as Temperature
            if self.opx_barometry_mode == 1:  # Opx-only mode
                calc = calculate_opx_only_press_temp(
                    opx_comps=df[opx_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name)
            else:  # Opx-Liq mode
                calc = calculate_opx_liq_press_temp(
                    opx_comps=df[opx_cols], liq_comps=df[liq_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name,
                    H2O_Liq=water)
            pressure = calc['P_kbar_calc']
            temperature_output = calc['T_K_calc']
        else:  # Fixed or dataset temperature
            if self.opx_barometry_mode == 1:  # Opx-only mode
                pressure = calculate_opx_only_press(
                    opx_comps=df[opx_cols],
                    equationP=current_model_func_name,
                    T=T_input)
            else:  # Opx-Liq mode
                pressure = calculate_opx_liq_press(
                    opx_comps=df[opx_cols], liq_comps=df[liq_cols],
                    equationP=current_model_func_name,
                    T=T_input,
                    H2O_Liq=water)

        results_df = pd.DataFrame()
        results_df['P_kbar_calc'] = pressure

        if temperature_output is not None:
            results_df['T_K_calc'] = temperature_output
        elif T_input is not None:
            results_df['T_K_input'] = T_input
        else:
            results_df['T_K_input'] = np.full(len(df), np.nan)

        return results_df, "OpxLiq", "T_K", "P_kbar"

    ## Amp-only and Amp-Liq stuff

    def _build_amp_liq_temp_gui(self, parent_box):
        """Build GUI for Amp Thermometry"""
        # Mode selection
        mode_box = gui.hBox(parent_box)
        gui.label(mode_box, self, "Thermometry Mode:")
        self.amp_thermometry_mode_buttons = gui.radioButtons(
            mode_box, self, "amp_thermometry_mode",
            callback=self._update_controls)
        gui.appendRadioButton(self.amp_thermometry_mode_buttons, "Amp-Liq")
        gui.appendRadioButton(self.amp_thermometry_mode_buttons, "Amp-only")

        # Models selection
        temp_model_box = gui.vBox(parent_box, "Models")
        self.amp_liq_temp_models_combo = gui.comboBox(
            temp_model_box, self, "amp_liq_temp_model_idx",
            items=[],  # Populated later
            callback=self._update_controls)

        # Pressure settings
        self.amp_liq_temp_pressure_box = gui.radioButtons(
            parent_box, self, "amp_liq_temp_pressure_type", box="Pressure Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.amp_liq_temp_pressure_box, "Dataset as Pressure (kbar)")




        rb_fixed_p = gui.appendRadioButton(self.amp_liq_temp_pressure_box, "Fixed Pressure")


        self.amp_liq_temp_pressure_value_box = gui.doubleSpin(
            gui.indentedBox(self.amp_liq_temp_pressure_box, gui.checkButtonOffsetHint(rb_fixed_p)), self,
            "amp_liq_temp_pressure_value", 0, 1000, step=1.0, label="Pressure Value (kbar)",
            alignment=Qt.AlignRight, callback=self.commit.deferred, controlWidth=80, decimals=0)

        rb_model_p = gui.appendRadioButton(self.amp_liq_temp_pressure_box, "Model as Pressure")
        model_as_p_box = gui.indentedBox(self.amp_liq_temp_pressure_box, gui.checkButtonOffsetHint(rb_model_p))

        self.amp_liq_temp_barometer_choice_buttons = gui.radioButtons(
            model_as_p_box, self, "amp_liq_temp_barometer_choice",
            callback=self._update_controls)

        rb_ao = gui.appendRadioButton(self.amp_liq_temp_barometer_choice_buttons, "Use Amp-only barometer")
        self.amp_liq_temp_barometer_model_box_ao = gui.comboBox(
            gui.indentedBox(self.amp_liq_temp_barometer_choice_buttons, gui.checkButtonOffsetHint(rb_ao)),
            self, "amp_liq_temp_barometer_model_idx_ao",
            items=[m[0] for m in MODELS_AMP_ONLY_PRESSURE],
            callback=self._update_controls)

        rb_al = gui.appendRadioButton(self.amp_liq_temp_barometer_choice_buttons, "Use Amp-Liq barometer")
        self.amp_liq_temp_barometer_model_box_al = gui.comboBox(
            gui.indentedBox(self.amp_liq_temp_barometer_choice_buttons, gui.checkButtonOffsetHint(rb_al)),
            self, "amp_liq_temp_barometer_model_idx_al",
            items=[m[0] for m in MODELS_AMP_LIQ_PRESSURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.amp_liq_temp_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "amp_liq_temp_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.amp_liq_temp_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "amp_liq_temp_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _build_amp_liq_press_gui(self, parent_box):
        """Build GUI for Amp Barometry"""
        # Mode selection
        mode_box = gui.hBox(parent_box)
        gui.label(mode_box, self, "Barometry Mode:")
        self.amp_barometry_mode_buttons = gui.radioButtons(
            mode_box, self, "amp_barometry_mode",
            callback=self._update_controls)
        gui.appendRadioButton(self.amp_barometry_mode_buttons, "Amp-Liq")
        gui.appendRadioButton(self.amp_barometry_mode_buttons, "Amp-only")

        # Models selection
        press_model_box = gui.vBox(parent_box, "Models")
        self.amp_liq_press_models_combo = gui.comboBox(
            press_model_box, self, "amp_liq_press_model_idx",
            items=[],  # Populated later
            callback=self._update_controls)

        # Temperature settings
        self.amp_liq_press_temp_box = gui.radioButtons(
            parent_box, self, "amp_liq_press_temp_type", box="Temperature Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.amp_liq_press_temp_box, "Dataset as Temperature (K)")

        rb_fixed_t = gui.appendRadioButton(self.amp_liq_press_temp_box, "Fixed Temperature")
        self.amp_liq_press_temp_value_box = gui.doubleSpin(
            gui.indentedBox(self.amp_liq_press_temp_box, gui.checkButtonOffsetHint(rb_fixed_t)), self,
            "amp_liq_press_temp_value", 500.0, 2000.0, step=1.0, label="Temperature Value (K)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=0)

        rb_model_t = gui.appendRadioButton(self.amp_liq_press_temp_box, "Model as Temperature")
        model_as_t_box = gui.indentedBox(self.amp_liq_press_temp_box, gui.checkButtonOffsetHint(rb_model_t))

        self.amp_liq_press_thermometer_choice_buttons = gui.radioButtons(
            model_as_t_box, self, "amp_liq_press_thermometer_choice",
            callback=self._update_controls)

        rb_ao = gui.appendRadioButton(self.amp_liq_press_thermometer_choice_buttons, "Use Amp-only thermometer")
        self.amp_liq_press_thermometer_model_box_ao = gui.comboBox(
            gui.indentedBox(self.amp_liq_press_thermometer_choice_buttons, gui.checkButtonOffsetHint(rb_ao)),
            self, "amp_liq_press_thermometer_model_idx_ao",
            items=[m[0] for m in MODELS_AMP_ONLY_TEMPERATURE],
            callback=self._update_controls)

        rb_al = gui.appendRadioButton(self.amp_liq_press_thermometer_choice_buttons, "Use Amp-Liq thermometer")
        self.amp_liq_press_thermometer_model_box_al = gui.comboBox(
            gui.indentedBox(self.amp_liq_press_thermometer_choice_buttons, gui.checkButtonOffsetHint(rb_al)),
            self, "amp_liq_press_thermometer_model_idx_al",
            items=[m[0] for m in MODELS_AMP_LIQ_TEMPERATURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.amp_liq_press_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "amp_liq_press_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.amp_liq_press_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "amp_liq_press_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _update_amp_liq_temp_controls(self):
        """Update controls for Amp-Liq/Amp-only Thermometry"""
        # Get the appropriate model list based on current mode
        if hasattr(self, 'amp_thermometry_mode') and self.amp_thermometry_mode == 1:  # Amp-only mode
            model_list = MODELS_AMP_ONLY_TEMPERATURE
        else:  # Default to Amp-Liq mode
            model_list = MODELS_AMP_LIQ_TEMPERATURE

        _, _, requires_press, requires_h2o = model_list[self.amp_liq_temp_model_idx]

        # Enable/disable pressure input group
        self.amp_liq_temp_pressure_box.setEnabled(requires_press)

        # Enable/disable pressure value box
        self.amp_liq_press_temp_value_box.setEnabled(
            requires_press and self.amp_liq_press_temp_type == 1)

        # Enable/disable barometer choice and model boxes
        model_as_p_active = requires_press and self.amp_liq_press_temp_type == 2
        self.amp_liq_temp_barometer_choice_buttons.setEnabled(model_as_p_active)

        if model_as_p_active:
            self.amp_liq_temp_barometer_model_box_ao.setEnabled(
                self.amp_liq_temp_barometer_choice == 0)
            self.amp_liq_temp_barometer_model_box_al.setEnabled(
                self.amp_liq_temp_barometer_choice == 1)
        else:
            self.amp_liq_temp_barometer_model_box_ao.setEnabled(False)
            self.amp_liq_temp_barometer_model_box_al.setEnabled(False)

        # Enable/disable H2O controls
        self.amp_liq_temp_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.amp_liq_temp_fixed_h2o_input.setEnabled(
            requires_h2o and self.amp_liq_temp_fixed_h2o)

    def _update_amp_liq_press_controls(self):
        """Update controls for Amp-Liq/Amp-only Barometry"""
        # Get the appropriate model list based on current mode
        if hasattr(self, 'amp_barometry_mode') and self.amp_barometry_mode == 1:  # Amp-only mode
            model_list = MODELS_AMP_ONLY_PRESSURE
        else:  # Default to Amp-Liq mode
            model_list = MODELS_AMP_LIQ_PRESSURE

        _, _, requires_temp, requires_h2o = model_list[self.amp_liq_press_model_idx]

        # Enable/disable temperature input group
        self.amp_liq_press_temp_box.setEnabled(requires_temp)

        # Enable/disable temperature value box
        self.amp_liq_press_temp_value_box.setEnabled(
            requires_temp and self.amp_liq_temp_pressure_type == 1)

        # Enable/disable thermometer choice and model boxes
        model_as_t_active = requires_temp and self.amp_liq_temp_pressure_type == 2
        self.amp_liq_press_thermometer_choice_buttons.setEnabled(model_as_t_active)

        if model_as_t_active:
            self.amp_liq_press_thermometer_model_box_ao.setEnabled(
                self.amp_liq_press_thermometer_choice == 0)
            self.amp_liq_press_thermometer_model_box_al.setEnabled(
                self.amp_liq_press_thermometer_choice == 1)
        else:
            self.amp_liq_press_thermometer_model_box_ao.setEnabled(False)
            self.amp_liq_press_thermometer_model_box_al.setEnabled(False)

        # Enable/disable H2O controls
        self.amp_liq_press_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.amp_liq_press_fixed_h2o_input.setEnabled(
            requires_h2o and self.amp_liq_press_fixed_h2o)











    def _calculate_amp_liq_press(self, df):
        """Calculate Amp-Liq or Amp-only pressures based on current mode"""
        # Determine which model set to use
        if hasattr(self, 'amp_barometry_mode') and self.amp_barometry_mode == 1:  # Amp-only mode
            model_list = MODELS_AMP_ONLY_PRESSURE
            mode_name = "Amp-only Barometry"
            print(f"DEBUG: Using Amp-only mode with model index {self.amp_liq_press_model_idx}")
        else:  # Default to Amp-Liq mode
            model_list = MODELS_AMP_LIQ_PRESSURE
            mode_name = "Amp-Liq Barometry"
            print(f"DEBUG: Using Amp-Liq mode with model index {self.amp_liq_press_model_idx}")

        _, current_model_func_name, requires_temp, requires_h2o = model_list[self.amp_liq_press_model_idx]
        print(f"DEBUG: Selected model function: {current_model_func_name}")

        # Determine thermometer function if using model temperature
        if requires_temp and self.amp_liq_press_temp_type == 2:
            if self.amp_liq_press_thermometer_choice == 0:  # Amp-only
                current_thermometer_func_name = MODELS_AMP_ONLY_TEMPERATURE[self.amp_liq_press_thermometer_model_idx_ao][1]
                print(f"DEBUG: Using Amp-only thermometer model: {current_thermometer_func_name}")
            else:  # Amp-Liq
                current_thermometer_func_name = MODELS_AMP_LIQ_TEMPERATURE[self.amp_liq_press_thermometer_model_idx_al][1]
                print(f"DEBUG: Using Amp-Liq thermometer model: {current_thermometer_func_name}")

        df = dm.preprocessing(df, my_output='amp_liq')

        water = self._get_h2o_value(df, requires_h2o,
                                self.amp_liq_press_fixed_h2o,
                                self.amp_liq_press_fixed_h2o_value_str,
                                mode_name)
        if water is None:
            return pd.DataFrame(), "", "", ""

        T_input = self._get_temperature_value(df, requires_temp,
                                            self.amp_liq_press_temp_type,
                                            self.amp_liq_press_temp_value,
                                            mode_name)

        pressure = None
        temperature_output = None

        if requires_temp and self.amp_liq_press_temp_type == 2:  # Model as Temperature
            if self.amp_barometry_mode == 1:  # Amp-only mode
                calc = calculate_amp_liq_press_temp(
                    amp_comps=df[amp_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name)
            else:  # Amp-Liq mode
                calc = calculate_amp_liq_press_temp(
                    amp_comps=df[amp_cols], liq_comps=df[liq_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name,
                    H2O_Liq=water)
            pressure = calc['P_kbar_calc']
            temperature_output = calc['T_K_calc']
        else:  # Fixed or dataset temperature
            if self.amp_barometry_mode == 1:  # Amp-only mode
                pressure_result = calculate_amp_only_press(
                    amp_comps=df[amp_cols],
                    equationP=current_model_func_name,
                    T=T_input)
                # Handle cases where the function returns a DataFrame (like Ridolfi2021)
                if isinstance(pressure_result, pd.DataFrame):
                    pressure = pressure_result['P_kbar_calc']
                else:
                    pressure = pressure_result
            else:  # Amp-Liq mode
                pressure = calculate_amp_liq_press(
                    amp_comps=df[amp_cols], liq_comps=df[liq_cols],
                    equationP=current_model_func_name,
                    T=T_input,
                    H2O_Liq=water)

        results_df = pd.DataFrame()
        results_df['P_kbar_calc'] = pressure

        if temperature_output is not None:
            results_df['T_K_calc'] = temperature_output
        elif T_input is not None:
            results_df['T_K_input'] = T_input
        else:
            results_df['T_K_input'] = np.full(len(df), np.nan)

        return results_df, "AmpLiq", "T_K", "P_kbar"

    def _calculate_amp_liq_temp(self, df):
            """Calculate Amp-Liq or Amp-only temperatures based on current mode"""
            # Determine which model set to use
            if hasattr(self, 'amp_thermometry_mode') and self.amp_thermometry_mode == 1:  # Amp-only mode
                model_list = MODELS_AMP_ONLY_TEMPERATURE
                mode_name = "Amp-only Thermometry"
            else:  # Default to Amp-Liq mode
                model_list = MODELS_AMP_LIQ_TEMPERATURE
                mode_name = "Amp-Liq Thermometry"

            _, current_model_func_name, requires_pressure, requires_h2o = model_list[self.amp_liq_temp_model_idx]

            # Determine barometer function if using model pressure
            if requires_pressure and self.amp_liq_temp_pressure_type == 2:
                if self.amp_liq_temp_barometer_choice == 0:  # Amp-only
                    current_barometer_func_name = MODELS_AMP_ONLY_PRESSURE[self.amp_liq_temp_barometer_model_idx_ao][1]
                else:  # Amp-Liq
                    current_barometer_func_name = MODELS_AMP_LIQ_PRESSURE[self.amp_liq_temp_barometer_model_idx_al][1]

            df = dm.preprocessing(df, my_output='amp_liq')

            water = self._get_h2o_value(df, requires_h2o,
                                    self.amp_liq_temp_fixed_h2o,
                                    self.amp_liq_temp_fixed_h2o_value_str,
                                    mode_name)
            if water is None: return pd.DataFrame(), "", "", ""

            P_input = self._get_pressure_value(df, requires_pressure,
                                            self.amp_liq_temp_pressure_type,
                                            self.amp_liq_temp_pressure_value,
                                            mode_name)

            temperature = None
            pressure_output = None

            if requires_pressure and self.amp_liq_temp_pressure_type == 2:  # Model as Pressure
                if self.amp_thermometry_mode == 1:  # Amp-only mode
                    calc = calculate_amp_only_press_temp(
                        amp_comps=df[amp_cols],
                        equationT=current_model_func_name,
                        equationP=current_barometer_func_name)
                else:  # Amp-Liq mode
                    calc = calculate_amp_liq_press_temp(
                        amp_comps=df[amp_cols], liq_comps=df[liq_cols],
                        equationT=current_model_func_name,
                        equationP=current_barometer_func_name,
                        H2O_Liq=water)
                temperature = calc['T_K_calc']
                pressure_output = calc['P_kbar_calc']
            else:  # Fixed or dataset pressure
                if self.amp_thermometry_mode == 1:  # Amp-only mode
                    temperature = calculate_amp_only_temp(
                        amp_comps=df[amp_cols],
                        equationT=current_model_func_name,
                        P=P_input)
                else:  # Amp-Liq mode
                    temperature = calculate_amp_liq_temp(
                        amp_comps=df[amp_cols], liq_comps=df[liq_cols],
                        equationT=current_model_func_name,
                        P=P_input,
                        H2O_Liq=water)

            results_df = pd.DataFrame()
            results_df['T_K_calc'] = temperature

            if pressure_output is not None:
                results_df['P_kbar_calc'] = pressure_output
            elif P_input is not None:
                results_df['P_kbar_input'] = P_input
            else:
                results_df['P_kbar_input'] = np.full(len(df), np.nan)

            return results_df, "AmpLiq", "T_K", "P_kbar"


## Updating controls
    def _update_controls(self):
        """Update all controls based on current settings"""
        # Hide all calculation boxes first
        self.cpx_opx_temp_box.setVisible(False)
        self.cpx_opx_press_box.setVisible(False)
        self.opx_liq_temp_box.setVisible(False)
        self.opx_liq_press_box.setVisible(False)
        self.amp_liq_temp_box.setVisible(False)
        self.amp_liq_press_box.setVisible(False)
        self.cpx_liq_temp_box.setVisible(False)
        self.cpx_liq_press_box.setVisible(False)
        # Show the selected calculation box
        if self.calculation_type == 1:  # Cpx-Opx Thermometry
            self.cpx_opx_temp_box.setVisible(True)
            self._update_cpx_opx_temp_controls()

        elif self.calculation_type == 2:  # Cpx-Opx Barometry
            self.cpx_opx_press_box.setVisible(True)
            self._update_cpx_opx_press_controls()

        elif self.calculation_type == 3:  # Opx-Liq Thermometry
            self.opx_liq_temp_box.setVisible(True)
            self._update_opx_liq_temp_controls()

        elif self.calculation_type == 4:  # Opx-Liq/Opx-only Barometry
            self.opx_liq_press_box.setVisible(True)

            # Keep your existing Opx barometry model update code
            if hasattr(self, 'opx_barometry_mode'):
                if self.opx_barometry_mode == 0:  # Opx-Liq mode
                    models = MODELS_OPX_LIQ_PRESSURE
                else:  # Opx-only mode
                    models = MODELS_OPX_ONLY_PRESSURE

                current_idx = self.opx_liq_press_model_idx
                self.opx_liq_press_models_combo.blockSignals(True)
                self.opx_liq_press_models_combo.clear()
                self.opx_liq_press_models_combo.addItems([m[0] for m in models])

                if current_idx < len(models):
                    self.opx_liq_press_model_idx = current_idx
                else:
                    self.opx_liq_press_model_idx = 0

                self.opx_liq_press_models_combo.blockSignals(False)

            self._update_opx_liq_press_controls()

        elif self.calculation_type == 5:  # Amp-Liq/Amp-only Thermometry
            self.amp_liq_temp_box.setVisible(True)

            # Add Amp thermometry model update (similar to Opx)
            if hasattr(self, 'amp_thermometry_mode'):
                if self.amp_thermometry_mode == 0:  # Amp-Liq mode
                    models = MODELS_AMP_LIQ_TEMPERATURE
                else:  # Amp-only mode
                    models = MODELS_AMP_ONLY_TEMPERATURE

                current_idx = self.amp_liq_temp_model_idx
                self.amp_liq_temp_models_combo.blockSignals(True)
                self.amp_liq_temp_models_combo.clear()
                self.amp_liq_temp_models_combo.addItems([m[0] for m in models])

                if current_idx < len(models):
                    self.amp_liq_temp_model_idx = current_idx
                else:
                    self.amp_liq_temp_model_idx = 0

                self.amp_liq_temp_models_combo.blockSignals(False)

            self._update_amp_liq_temp_controls()

        elif self.calculation_type == 6:  # Amp-Liq/Amp-only Barometry
            self.amp_liq_press_box.setVisible(True)

            # Add Amp barometry model update (similar to Opx)
            if hasattr(self, 'amp_barometry_mode'):
                if self.amp_barometry_mode == 0:  # Amp-Liq mode
                    models = MODELS_AMP_LIQ_PRESSURE
                else:  # Amp-only mode
                    models = MODELS_AMP_ONLY_PRESSURE

                current_idx = self.amp_liq_press_model_idx
                self.amp_liq_press_models_combo.blockSignals(True)
                self.amp_liq_press_models_combo.clear()
                self.amp_liq_press_models_combo.addItems([m[0] for m in models])

                if current_idx < len(models):
                    self.amp_liq_press_model_idx = current_idx
                else:
                    self.amp_liq_press_model_idx = 0

                self.amp_liq_press_models_combo.blockSignals(False)

            self._update_amp_liq_press_controls()

        elif self.calculation_type == 7:  # Cpx-Liq/Cpx-only Thermometry
            self.cpx_liq_temp_box.setVisible(True)

            # Add Cpx thermometry model update (similar to Opx)
            if hasattr(self, 'cpx_thermometry_mode'):
                if self.cpx_thermometry_mode == 0:  # Cpx-Liq mode
                    models = MODELS_CPX_LIQ_TEMPERATURE
                else:  # Cpx-only mode
                    models = MODELS_CPX_ONLY_TEMPERATURE

                current_idx = self.cpx_liq_temp_model_idx
                self.cpx_liq_temp_models_combo.blockSignals(True)
                self.cpx_liq_temp_models_combo.clear()
                self.cpx_liq_temp_models_combo.addItems([m[0] for m in models])

                if current_idx < len(models):
                    self.cpx_liq_temp_model_idx = current_idx
                else:
                    self.cpx_liq_temp_model_idx = 0

                self.cpx_liq_temp_models_combo.blockSignals(False)

            self._update_cpx_liq_temp_controls()

        elif self.calculation_type == 8:  # Cpx-Liq/Cpx-only Barometry
            self.cpx_liq_press_box.setVisible(True)

            # Add Cpx barometry model update (similar to Opx)
            if hasattr(self, 'cpx_barometry_mode'):
                if self.cpx_barometry_mode == 0:  # Cpx-Liq mode
                    models = MODELS_CPX_LIQ_PRESSURE
                else:  # Cpx-only mode
                    models = MODELS_CPX_ONLY_PRESSURE

                current_idx = self.cpx_liq_press_model_idx
                self.cpx_liq_press_models_combo.blockSignals(True)
                self.cpx_liq_press_models_combo.clear()
                self.cpx_liq_press_models_combo.addItems([m[0] for m in models])

                if current_idx < len(models):
                    self.cpx_liq_press_model_idx = current_idx
                else:
                    self.cpx_liq_press_model_idx = 0

                self.cpx_liq_press_models_combo.blockSignals(False)

            self._update_cpx_liq_press_controls()

        self.commit.now()








    ##

    @Inputs.data
    def set_data(self, data):
        self.data = data
        self.commit.now()

    @gui.deferred
    def commit(self):
        self.clear_messages()
        self.Error.value_error.clear()
        self.Warning.value_error.clear()

        if self.data is None:
            self.Outputs.data.send(None)
            return

        if len(self.data.domain.attributes) <= 1:
            self.Warning.value_error("Not enough attributes in the dataset for calculations.")
            self.Outputs.data.send(None)
            return

        df = pd.DataFrame(data=np.array(self.data.X), columns=[a.name for a in self.data.domain.attributes])

        result_df = pd.DataFrame()
        prefix = ""
        temp_col_name_suffix = ""
        press_col_name_suffix = ""

        # Perform calculation based on selected type
        if self.calculation_type == 1:  # Cpx-Opx Thermometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_cpx_opx_temp(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Cpx-Opx Thermometry: {e}")
                self.Outputs.data.send(None)
                return

        elif self.calculation_type == 2:  # Cpx-Opx Barometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_cpx_opx_press(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Cpx-Opx Barometry: {e}")
                self.Outputs.data.send(None)
                return

        elif self.calculation_type == 3:  # Opx-Liq Thermometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_opx_liq_temp(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Opx-Liq Thermometry: {e}")
                self.Outputs.data.send(None)
                return

        elif self.calculation_type == 4:  # Opx-Liq Barometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_opx_liq_press(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Opx-Liq Barometry: {e}")
                self.Outputs.data.send(None)
                return

        # NEW AMPHIBOLE CALCULATIONS ADDED HERE
        elif self.calculation_type == 5:  # Amp-only Thermometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_amp_liq_temp(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Amp-only Thermometry: {e}")
                self.Outputs.data.send(None)
                return

        elif self.calculation_type == 6:  # Amp-only Barometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_amp_liq_press(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Amp-only Barometry: {e}")
                self.Outputs.data.send(None)
                return

        elif self.calculation_type == 7:  # Cpx-Liq Thermometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_cpx_liq_temp(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Cpx-Liq Thermometry: {e}")
                self.Outputs.data.send(None)
                return

        elif self.calculation_type == 8:  # Cpx-Liq Barometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_cpx_liq_press(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Cpx-Liq Barometry: {e}")
                self.Outputs.data.send(None)
                return


        # Prepare output if calculation was successful
        if not result_df.empty:
            output_table = self._create_output_table(
                self.data, result_df, prefix, temp_col_name_suffix, press_col_name_suffix)
            self.Outputs.data.send(output_table)
        else:
            self.Outputs.data.send(None)





## Helper functions to update buttons
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
                return 0  # Default to 0 if required but not found and not fixed
        return 0  # Return 0 if H2O is not required

    def _get_pressure_value(self, df, requires_pressure, pressure_type, pressure_value, calculation_name):
        """Helper to get Pressure value, handling dataset, fixed, or None."""
        if requires_pressure:
            if pressure_type == 0:  # Dataset
                if 'P_kbar' in df.columns:
                    return df['P_kbar']
                else:
                    self.Warning.value_error(f"'P_kbar' column not in Dataset for {calculation_name}. Using default 1 kbar.")
                    return 1.0  # Default to 1 kbar if required and not found in dataset
            elif pressure_type == 1:  # Fixed
                return pressure_value
        return None  # Return None if pressure is not required

    def _get_temperature_value(self, df, requires_temp, temp_type, temp_value, calculation_name):
        """Helper to get Temperature value, handling dataset, fixed, or None."""
        if requires_temp:
            if temp_type == 0:  # Dataset
                if 'T_K' in df.columns:
                    return df['T_K']
                else:
                    self.Warning.value_error(f"'T_K' column not in Dataset for {calculation_name}. Using default 900 K.")
                    return 900.0  # Default to 900 K if required and not found in dataset
            elif temp_type == 1:  # Fixed
                return temp_value
        return None  # Return None if temperature is not required

    def _create_output_table(self, original_table, results_df, prefix, temp_col_suffix, press_col_suffix):
        """Creates a new Orange Table with calculated results as meta attributes."""
        current_meta_names = set([m.name for m in original_table.domain.metas])

        new_meta_variables = []
        new_meta_values = []

        base_output_temp_name = f"{prefix}_{temp_col_suffix}"
        base_output_press_name = f"{prefix}_{press_col_suffix}"

        existing_names = set([a.name for a in original_table.domain.attributes] + list(current_meta_names))

        # Handle Temperature Output
        output_temp_calc_name = ""
        output_temp_input_name = ""

        if 'T_K_calc' in results_df.columns and not results_df['T_K_calc'].isnull().all():
            output_temp_calc_name = base_output_temp_name
            suffix = 0
            while output_temp_calc_name in existing_names:
                suffix += 1
                output_temp_calc_name = f"{base_output_temp_name}_{suffix}"

            new_meta_variables.append(ContinuousVariable(output_temp_calc_name))
            new_meta_values.append(results_df['T_K_calc'].values)
            existing_names.add(output_temp_calc_name)

        if 'T_K_input' in results_df.columns and not results_df['T_K_input'].isnull().all():
            output_temp_input_name = base_output_temp_name + "_Input"
            suffix = 0
            while output_temp_input_name in existing_names:
                suffix += 1
                output_temp_input_name = f"{base_output_temp_name}_Input_{suffix}"

            new_meta_variables.append(ContinuousVariable(output_temp_input_name))
            new_meta_values.append(results_df['T_K_input'].values)
            existing_names.add(output_temp_input_name)

        # Handle Pressure Output
        output_press_calc_name = ""
        output_press_input_name = ""

        if 'P_kbar_calc' in results_df.columns and not results_df['P_kbar_calc'].isnull().all():
            output_press_calc_name = base_output_press_name
            suffix = 0
            while output_press_calc_name in existing_names:
                suffix += 1
                output_press_calc_name = f"{base_output_press_name}_{suffix}"

            new_meta_variables.append(ContinuousVariable(output_press_calc_name))
            new_meta_values.append(results_df['P_kbar_calc'].values)
            existing_names.add(output_press_calc_name)

        if 'P_kbar_input' in results_df.columns and not results_df['P_kbar_input'].isnull().all():
            output_press_input_name = base_output_press_name + "_Input"
            suffix = 0
            while output_press_input_name in existing_names:
                suffix += 1
                output_press_input_name = f"{base_output_press_name}_Input_{suffix}"

            new_meta_variables.append(ContinuousVariable(output_press_input_name))
            new_meta_values.append(results_df['P_kbar_input'].values)
            existing_names.add(output_press_input_name)

        # Convert the list of 1D new_meta_values into a 2D array (columns)
        if new_meta_values:
            new_metas_array = np.column_stack(new_meta_values)
        else:
            new_metas_array = np.empty((len(original_table.X), 0))

        # Combine existing metas with new ones
        if original_table.metas is not None and original_table.metas.size > 0:
            combined_metas_array = np.hstack([original_table.metas, new_metas_array])
        else:
            combined_metas_array = new_metas_array

        # Ensure combined_metas_array has the correct shape for from_numpy
        if combined_metas_array.ndim == 1:
            combined_metas_array = combined_metas_array[:, np.newaxis]
        elif combined_metas_array.size == 0 and len(original_table.X) > 0:
            combined_metas_array = np.empty((len(original_table.X), 0))

        # Construct the new domain
        new_domain = Domain(original_table.domain.attributes, original_table.domain.class_vars,
                           original_table.domain.metas + tuple(new_meta_variables))

        return Table.from_numpy(new_domain, original_table.X, original_table.Y, combined_metas_array)
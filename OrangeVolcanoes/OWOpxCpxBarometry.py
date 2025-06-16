import numpy as np
import pandas as pd
from Orange.data import Table, ContinuousVariable, Domain
from Orange.widgets.settings import Setting, ContextSetting
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from orangewidget.widget import Msg
from Thermobar import calculate_cpx_opx_temp, calculate_cpx_opx_press_temp

from OrangeVolcanoes.utils import dataManipulation as dm
from AnyQt.QtCore import Qt

cpx_cols = ['SiO2_Cpx', 'TiO2_Cpx', 'Al2O3_Cpx',
'FeOt_Cpx', 'MnO_Cpx', 'MgO_Cpx', 'CaO_Cpx', 'Na2O_Cpx', 'K2O_Cpx',
'Cr2O3_Cpx']


opx_cols = ['SiO2_Opx', 'TiO2_Opx', 'Al2O3_Opx',
'FeOt_Opx', 'MnO_Opx', 'MgO_Opx', 'CaO_Opx', 'Na2O_Opx', 'K2O_Opx',
'Cr2O3_Opx']


# First element is the display name, second is the func name in Thermobar
# First tuple indicates whether model requires a PRESSURE, second whether it requires water.



# Opx-Cpx temp
MODELS_OL = [
    ('T_Put2008_eq36', 'T_Put2008_eq36', True, False),
        ('T_Put2008_eq37', 'T_Put2008_eq37', True, False),
        ('T_Brey1990', 'T_Brey1990', True, False),
        ('T_Wood1973', 'T_Wood1973', False, False),
        ('T_Wells1977', 'T_Wells1977', False, False),

]


# Opx only pressure
MODELS_OO = [
 ('None_available','None_available',  True, True),
]



# Opx only pressure -
MODELS_PRESSURE_OO = [
 ('None_available','None_available',  True, True),
]

MODELS_PRESSURE_OL = [
    ('P_Put2008_eq38', 'P_Put2008_eq38'),
    ('P_Put2008_eq39', 'P_Put2008_eq39'),
]


## Directly adapted from the opx one.
class OWOpxCpxThermometer(OWWidget):
    name = "Cpx_Opx_Thermometer"
    description = "The widget allows the user to determine the temperature of Opx-Cpx formation/re-equilibration from paired data."
    icon = "icons/Cpx_Opx_Thermometer.png"
    priority = 6
    keywords = ['Opx', 'Cpx', 'Thermometer']

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        data = Output("Data", Table, dynamic=False)

    GENERIC = 0
    FROM_VAR = 0

    #  0 is using PRESSURE from a column in the dataset. 1 is using a fixed value entered by the user.
    # 2 is iterating with an equation.

    VALID_PRESSURE_TYPES = [0, 1, 2]

    # Changed default model_type to 1 for Opx-Cpx
    model_type = ContextSetting(1)
    PRESSURE_type = ContextSetting(GENERIC)

    resizing_enabled = False
    want_main_area = False


    model_idx_oo = 0 #Setting(0)
    model_idx_ol = 0 #Setting(0)

    model_idx_PRESSURE_oo = Setting(0)
    model_idx_PRESSURE_ol = Setting(0)

    # CHANGE: New setting to control which barometer type is active. 0=Opx-only, 1=Opx-Liq
    active_barometer_choice = Setting(1)

    PRESSURE = Setting(True)

    # Water test
    fixed_h2o = Setting(False)
    fixed_h2o_value_str = Setting("1.0")


    PRESSURE_model_oo = Setting(False)
    PRESSURE_model_ol = Setting(False)

    PRESSURE_value = Setting(1)

    auto_apply = Setting(True)

    fixed_h2o = Setting(False)
    fixed_h2o_value = Setting(1.0)  # Default in wt%




    class Error(OWWidget.Error):
        value_error = Msg("{}")

    class Warning(OWWidget.Warning):
        value_error = Msg("{}")



    def __init__(self):
        OWWidget.__init__(self)
        self.data = None

        lbl = gui.label(self.controlArea, self, "<i>Calculations performed using Thermobar...</i>")
        lbl.setStyleSheet("font-size:10px; color: gray;")

        box = gui.radioButtons(
            self.controlArea, self, "model_type", box="Models",
            callback=self._update_controls)

        # Removed Opx-only thermometer section as it was commented out and causing NameError
        # button = gui.appendRadioButton(box, "Opx-only thermometers")
        # self.models_combo_oo = gui.comboBox(
        #     gui.indentedBox(box, gui.checkButtonOffsetHint(button)), self, "model_idx_oo",
        #     items=[m[0] for m in MODELS_OO],
        #     callback=self._update_controls)

        # Assign the radio button for "Opx-Cpx thermometers" to a variable
        cpx_opx_button = gui.appendRadioButton(box, "Opx-Cpx thermometers")
        self.models_combo_ol = gui.comboBox(
            gui.indentedBox(box, gui.checkButtonOffsetHint(cpx_opx_button)), self, "model_idx_ol",
            items=[m[0] for m in MODELS_OL],
            callback=self._update_controls)

        self.box_1 = gui.radioButtons(
            self.controlArea, self, "PRESSURE_type", box="PRESSURE",
            callback=self._update_controls)

        gui.appendRadioButton(self.box_1, "Dataset_as_PRESSURE_(kbar)")

        rb_fixed_p = gui.appendRadioButton(self.box_1, "Fixed_PRESSURE")
        self.PRESSURE_value_box = gui.doubleSpin(
            gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(rb_fixed_p)), self,
            "PRESSURE_value", 1.0, 10000.0, step=0.1, label="PRESSURE_value_(kbar)",
            alignment=Qt.AlignRight, callback=self._value_change, controlWidth=80, decimals=1)

        rb_model_p = gui.appendRadioButton(self.box_1, "Model_as_PRESSURE")
        model_as_p_box = gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(rb_model_p))

        # CHANGE: Add radio buttons to choose between barometer types
        self.barometer_choice_buttons = gui.radioButtons(
            model_as_p_box, self, "active_barometer_choice",
            callback=self._barometer_choice_change)

        # Removed Opx-only barometer as it was commented out and causing issues with index
        # rb_oo = gui.appendRadioButton(self.barometer_choice_buttons, "Use Opx-only barometer")
        # self.PRESSURE_model_box_oo = gui.comboBox(
        #     gui.indentedBox(self.barometer_choice_buttons, gui.checkButtonOffsetHint(rb_oo)),
        #     self, "model_idx_PRESSURE_oo", items=[m[0] for m in MODELS_PRESSURE_OO],
        #     callback=self._model_PRESSURE_oo_change)

        # Removed setting of active_barometer_choice to 0 here to avoid issues with it being set to 1 by default
        rb_ol = gui.appendRadioButton(self.barometer_choice_buttons, "Use Opx-Cpx barometer")
        self.PRESSURE_model_box_ol = gui.comboBox(
            gui.indentedBox(self.barometer_choice_buttons, gui.checkButtonOffsetHint(rb_ol)),
            self, "model_idx_PRESSURE_ol", items=[m[0] for m in MODELS_PRESSURE_OL],
            callback=self._model_PRESSURE_ol_change)


        self.fixed_h2o_box = gui.vBox(self.controlArea, "H₂O Settings")
        gui.checkBox(self.fixed_h2o_box, self, "fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.fixed_h2o_input = gui.lineEdit(
            self.fixed_h2o_box, self, "fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)

        gui.auto_apply(self.buttonsArea, self)
        self._update_controls()


    def _update_controls(self):
        """A single function to update the state of all GUI controls."""
        # Simplified model_type handling since Opx-only thermometer is removed
        # The model_type radio buttons are still there, but now only control the internal state based on initial setting.
        # It's better to remove the model_type radio buttons if Opx-only isn't an option.
        # For now, let's just make sure the correct model is selected based on self.model_type
        if self.model_type == 0: # This case should ideally not be reached if model_type is set to 1
            # You might want to remove this branch if Opx-only is truly removed from the UI
            _, self.model, self.PRESSURE, self.h2o = MODELS_OO[self.model_idx_oo]
            # self.models_combo_oo.setEnabled(True) # If you decide to re-add, uncomment this
            self.models_combo_ol.setEnabled(False)
        else: # self.model_type == 1
            _, self.model, self.PRESSURE, self.h2o = MODELS_OL[self.model_idx_ol]
            # self.models_combo_oo.setEnabled(False) # If you decide to re-add, uncomment this
            self.models_combo_ol.setEnabled(True)


        self.box_1.setEnabled(self.PRESSURE)
        self.PRESSURE_value_box.setEnabled(self.PRESSURE and self.PRESSURE_type == 1)

        # Logic for the "Model as PRESSURE" section
        model_as_p_active = self.PRESSURE and self.PRESSURE_type == 2
        self.barometer_choice_buttons.setEnabled(model_as_p_active)

        if model_as_p_active:
            # Since only Opx-Cpx barometer is available, force choice to 1
            self.active_barometer_choice = 1
            # Disable the Opx-only button if it were there, and enable the Opx-Cpx one
            # self.barometer_choice_buttons.buttons[0].setEnabled(False) # if it existed
            # The order of buttons might shift if you remove one. Assuming [0] is Opx-Cpx now.
            if len(self.barometer_choice_buttons.buttons) > 0:
                self.barometer_choice_buttons.buttons[0].setEnabled(True) # This is the Opx-Cpx one now

            # Sync the enabled state of the dropdowns
            self._barometer_choice_change()
        else:
            # Disable dropdown if Model as P is not selected
            # self.PRESSURE_model_box_oo.setEnabled(False) # if it existed
            self.PRESSURE_model_box_ol.setEnabled(False)

        self.fixed_h2o_box.setEnabled(self.h2o)
        self.fixed_h2o_input.setEnabled(self.h2o and self.fixed_h2o)

        self.commit.deferred()

    def _barometer_choice_change(self):
        """Handles switching between Opx-only and Opx-Liq barometer types."""
        # Enable/disable the comboboxes based on the radio button selection
        # self.PRESSURE_model_box_oo.setEnabled(self.active_barometer_choice == 0) # if it existed
        self.PRESSURE_model_box_ol.setEnabled(self.active_barometer_choice == 1)

        # Update the pressure model to reflect the active choice and commit
        # if self.active_barometer_choice == 0: # if it existed
        #     self._model_PRESSURE_oo_change()
        # else:
        self._model_PRESSURE_ol_change()

    def _value_change(self):
        self.commit.deferred()

    def _model_PRESSURE_oo_change(self):
        # This function might become redundant if Opx-only barometer is completely removed
        _, self.model_PRESSURE = MODELS_PRESSURE_OO[self.model_idx_PRESSURE_oo]
        self.commit.deferred()

    def _model_PRESSURE_ol_change(self):
        _, self.model_PRESSURE = MODELS_PRESSURE_OL[self.model_idx_PRESSURE_ol]
        self.commit.deferred()

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
            return

        if len(self.data.domain.attributes) <= 1:
            return

        df = pd.DataFrame(data=np.array(self.data.X), columns=[a.name for a in self.data.domain.attributes])

        if self.fixed_h2o:
            try:
                water = float(self.fixed_h2o_value_str)
            except ValueError:
                self.Error.value_error("Invalid H₂O value entered.")
                return
        else:
            if self.h2o and 'H2O_Liq' in df.columns:
                water = df['H2O_Liq']
            else:
                water = 0
                if self.h2o:
                    self.Warning.value_error("'H2O_Liq' column not in Dataset, H₂O is set to zero.")

        temperature = None
        PRESSURE_output = None

        # This block now effectively becomes the only active path for calculations
        # since model_type is set to 1.
        if self.model_type == 0:
            # This 'raise' will no longer be hit if model_type is initialized to 1.
            raise NotImplementedError("Opx-only thermometers are not yet implemented to iterate with Cpx-opx.")

        elif self.model_type == 1:
            df = dm.preprocessing(df, my_output='cpx_opx')
            P = None
            if self.PRESSURE:
                if self.PRESSURE_type == 0: # Dataset
                    if 'P_kbar' in df.columns:
                        P = df['P_kbar']
                    else:
                        self.Warning.value_error("'P_kbar' column not in Dataset.")
                elif self.PRESSURE_type == 1: # Fixed
                    P = self.PRESSURE_value

            if self.PRESSURE and self.PRESSURE_type == 2: # Model
                calc = calculate_cpx_opx_press_temp(
                    opx_comps=df[opx_cols], cpx_comps=df[cpx_cols],
                    equationT=self.model, equationP=self.model_PRESSURE)
                temperature = calc['T_K_calc']
                PRESSURE_output = calc['P_kbar_calc']
            else: # No pressure or fixed/dataset pressure
                temperature = calculate_cpx_opx_temp(
                    opx_comps=df[opx_cols], cpx_comps=df[cpx_cols],
                    equationT=self.model, P=P)

        # Prepare and send output
        if PRESSURE_output is not None:
            my_domain = Domain(
                [ContinuousVariable(name=a.name) for a in self.data.domain.attributes],
                [ContinuousVariable("T_K_output"), ContinuousVariable("P_kbar_output")],
                metas=self.data.domain.metas)
            Y = np.column_stack([temperature, PRESSURE_output])
        else:
            if self.PRESSURE and self.PRESSURE_type == 0:
                P_out = df["P_kbar"] if 'P_kbar' in df.columns else np.full(len(df), np.nan)
            elif self.PRESSURE and self.PRESSURE_type == 1:
                P_out = np.full(len(df), self.PRESSURE_value)
            else: # No pressure input
                P_out = np.full(len(df), np.nan)

            my_domain = Domain(
                [ContinuousVariable(name=a.name) for a in self.data.domain.attributes],
                [ContinuousVariable("T_K_output"), ContinuousVariable("P_kbar_input")],
                metas=self.data.domain.metas)
            Y = np.column_stack([temperature, P_out])

        out = Table.from_numpy(my_domain, self.data.X, Y, self.data.metas)
        self.Outputs.data.send(out)
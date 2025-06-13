import numpy as np
import pandas as pd
from Orange.data import Table, ContinuousVariable, Domain
from Orange.widgets.settings import Setting, ContextSetting
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from orangewidget.widget import Msg
from Thermobar import calculate_opx_only_press, calculate_opx_liq_press, calculate_opx_liq_press_temp

from OrangeVolcanoes.utils import dataManipulation as dm
from AnyQt.QtCore import Qt


liq_cols = ['SiO2_Liq', 'TiO2_Liq', 'Al2O3_Liq',
'FeOt_Liq', 'MnO_Liq', 'MgO_Liq', 'CaO_Liq', 'Na2O_Liq', 'K2O_Liq',
'Cr2O3_Liq', 'P2O5_Liq', 'H2O_Liq', 'Fe3Fet_Liq', 'NiO_Liq', 'CoO_Liq',
 'CO2_Liq']


opx_cols = ['SiO2_Opx', 'TiO2_Opx', 'Al2O3_Opx',
'FeOt_Opx', 'MnO_Opx', 'MgO_Opx', 'CaO_Opx', 'Na2O_Opx', 'K2O_Opx',
'Cr2O3_Opx']


# First element is the display name, second is the func name in Thermobar
# First tuple indicates whether model requires a temperature, second whether it requires water.


# Opx only pressure
MODELS_OO = [
    ('P_Put2008_eq29c', 'P_Put2008_eq29c', True, False),
]

# Opx-Liq pressure
MODELS_OL = [
    ('P_Put2008_eq29a', 'P_Put2008_eq29a', True, True),
    ('P_Put2008_eq29b', 'P_Put2008_eq29b', True, True),
    ('P_Put_Global_Opx', 'P_Put_Global_Opx', False, False),
     ('P_Put_Felsic_Opx', 'P_Put_Felsic_Opx', False, False),
]

# Opx only temp -
MODELS_TEMPERATURE_OO = [
 ('None_available', ''),
]

MODELS_TEMPERATURE_OL = [
    ('T_Put2008_eq28a', 'T_Put2008_eq28a'),
    ('T_Put2008_eq28b_opx_sat', 'T_Put2008_eq28b_opx_sat'),
    ('T_Beatt1993_opx', 'T_Beatt1993_opx')
]


## Directly adapted from the opx one.
class OWopxBarometer(OWWidget):
    name = "opxBarometer"
    description = "The widget allows the user to determine the pressure of Opx formation/re-equilibration using its chemical composition or the composition of orthopyroxene liquid pairs as input data."
    icon = "icons/Opx_Barometer_icon.png"
    priority = 4
    keywords = ['Opx', 'Barometer']

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        data = Output("Data", Table, dynamic=False)

    GENERIC = 0
    FROM_VAR = 0

    #  0 is using temperature from a column in the dataset. 1 is using a fixed value entered by the user.
    # 2 is iterating with an equation.

    VALID_TEMPERATURE_TYPES = [0, 1, 2]

    model_type = ContextSetting(GENERIC)
    temperature_type = ContextSetting(GENERIC)

    resizing_enabled = False
    want_main_area = False


    model_idx_oo = 0 #Setting(0)
    model_idx_ol = 0 #Setting(0)

    model_idx_temperature_oo = Setting(0)
    model_idx_temperature_ol = Setting(0)
    temperature = Setting(True)

    # Water test
    fixed_h2o = Setting(False)
    fixed_h2o_value_str = Setting("1.0")


    temperature_model_oo = Setting(False)
    temperature_model_ol = Setting(False)

    temperature_value = Setting(1000)

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

        # Have an option for water

        # Create the label first
        lbl = gui.label(self.controlArea, self, "<i>Calculations performed using Thermobar, please remember to cite Wieser et al. (2022) and Muso et al. (2025) </i>")

        # Then style it using Qt's stylesheet syntax
        lbl.setStyleSheet("font-size:10px; color: gray;")

        # This sets up the GUI

        box = gui.radioButtons(
            self.controlArea, self, "model_type", box="Models",
            callback=self._radio_change)



        #Opx-only GUI
        button = gui.appendRadioButton(box, "Opx-only barometers")

        self.models_combo_oo = gui.comboBox(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button)), self, "model_idx_oo",
            items=[m[0] for m in MODELS_OO],
            callback=self._model_combo_change
        )

        _, self.model, self.temperature, self.h2o = MODELS_OO[self.model_idx_oo]


        #opx-liq GUI
        gui.appendRadioButton(box, "Opx-liq barometers")

        self.models_combo_ol = gui.comboBox(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button)), self, "model_idx_ol",
            items=[m[0] for m in MODELS_OL],
            callback=self._model_combo_change

        )

        # This creates the box for how temperature is handled.
        self.box_1 = gui.radioButtons(
            self.controlArea, self, "temperature_type", box="Temperature",
            callback=self._radio_change_1)


        #Dataset as Temperature GUI
        self.button_1 = gui.appendRadioButton(self.box_1, "Dataset_as_Temperature_(K)")

        #Fixed Temperature GUI
        gui.appendRadioButton(self.box_1, "Fixed_Temperature")

        self.temperature_value_box = gui.spin(
            gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1)), self, "temperature_value", 1, 10000, label="Temperature_value_(K)",
            alignment=Qt.AlignRight, callback=self._value_change,
            controlWidth=80)

        # Model as Temperature
        gui.appendRadioButton(self.box_1, "Model_as_Temperature")

        # Add label: Opx-only thermometers
        opx_only_box = gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1))
        gui.label(opx_only_box, self, "Opx-only thermometers")
        self.temperature_model_box_oo = gui.comboBox(
            opx_only_box, self, "model_idx_temperature_oo",
            items=[m[0] for m in MODELS_TEMPERATURE_OO],
            callback=self._model_temperature_change)

        # Add label: Opx-Liq thermometers
        opx_liq_box = gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1))
        gui.label(opx_liq_box, self, "Opx-Liq thermometers")

        self.temperature_model_box_ol = gui.comboBox(
            opx_liq_box, self, "model_idx_temperature_ol",
            items=[m[0] for m in MODELS_TEMPERATURE_OL],
            callback=self._model_temperature_change)

        _, self.model_temperature = MODELS_TEMPERATURE_OO[self.model_idx_temperature_oo]


        # H₂O override section
        self.fixed_h2o_box = gui.vBox(self.controlArea, "H₂O Settings")

        # Checkbox: enables H₂O override
        gui.checkBox(
            self.fixed_h2o_box, self, "fixed_h2o", "Fixed H₂O",
            callback=self._radio_change  # reuses safe logic
        )

        # Text box: manual H₂O entry
        self.fixed_h2o_input = gui.lineEdit(
            self.fixed_h2o_box, self, "fixed_h2o_value_str",
            label="H₂O (wt%)", orientation=Qt.Horizontal,
            callback=lambda: self.commit.deferred()
        )

        self.box_1.setEnabled(False)

        self.models_combo_oo.setEnabled(True)
        self.models_combo_ol.setEnabled(False)

        gui.auto_apply(self.buttonsArea, self)

    def _h2o_toggle(self):
        self.fixed_h2o_input.setEnabled(self.fixed_h2o)

        # Only call deferred if commit is ready and callable
        if hasattr(self, "commit") and callable(getattr(self.commit, "deferred", None)):
            self.commit.deferred()

    # This function updates the GUI and model calculations when user clicks different buttons.
    def _radio_change(self):

        # For Opx-only barometer,
        if self.model_type == 0:
            # Retrieves the relevant model
            _, self.model, self.temperature, self.h2o = MODELS_OO[self.model_idx_oo]
            # Selects a temperature model if used - If Opx only temps exist, uncomment.
            # _, self.model_temperature = MODELS_TEMPERATURE_OO[self.model_idx_temperature_oo]
            # self.models_combo_oo.setEnabled(True)
            # self.models_combo_ol.setEnabled(False)

            # There are no temperature models for Opx-only so set to None
            self.model_temperature = None

            # Enable/disable GUI elements
            self.models_combo_oo.setEnabled(True)
            self.models_combo_ol.setEnabled(False)

        # Same for Opx-Liq barometry
        elif self.model_type == 1:
            _, self.model, self.temperature, self.h2o = MODELS_OL[self.model_idx_ol]
            _, self.model_temperature = MODELS_TEMPERATURE_OL[self.model_idx_temperature_ol]
            self.models_combo_oo.setEnabled(False)
            self.models_combo_ol.setEnabled(True)

        # If the user has selected fixed temperature and the selected barometer model requires temperature
        if self.temperature_type == 1 and self.temperature == True:
            # Show the input box because it does need temp
            self.temperature_value_box.setEnabled(True)
        else:
            # Dont show the input box because it doesnt need temperature.
            self.temperature_value_box.setEnabled(False)


        # For Opx-only, enables box if model needs temp and user wants to enter temp
        if self.temperature_type == 1 and self.temperature_model_oo == True:
            self.temperature_model_box_oo.setEnabled(True)
        else:
            self.temperature_model_box_oo.setEnabled(False)

        # For Opx-Liq, does the same

        if self.temperature_type == 1 and self.temperature_model_ol == True:
            self.temperature_model_box_ol.setEnabled(True)
        else:
            self.temperature_model_box_ol.setEnabled(False)


        # This disables the entire temp section if the model doesnt need temperature
        if self.temperature == False:
            self.box_1.setEnabled(False)
            self.temperature_value_box.setEnabled(False)
            self.temperature_model_box_oo.setEnabled(False)
            self.temperature_model_box_ol.setEnabled(False)
        else:
            self.box_1.setEnabled(True)

        # Enables numerical input
        if self.temperature_type == 1:
            self.temperature_value_box.setEnabled(True)
        else:
            self.temperature_value_box.setEnabled(False)

        # If want to entire a model, enables that
        if self.temperature_type == 2:
            if self.model_type == 0:
                self.temperature_model_box_oo.setEnabled(True)
                self.temperature_model_box_ol.setEnabled(False)
            elif self.model_type == 1:
                self.temperature_model_box_oo.setEnabled(False)
                self.temperature_model_box_ol.setEnabled(True)

        else:
            self.temperature_model_box_oo.setEnabled(False)
            self.temperature_model_box_ol.setEnabled(False)

        # Enable/disable H₂O box
        self.fixed_h2o_input.setEnabled(self.h2o and self.fixed_h2o)
        self.fixed_h2o_box.setEnabled(self.h2o)


        self.commit.deferred()

    # Triggered when user changes the model.
    def _model_combo_change(self):

        # If model is Opx-only, get model and flags
        if self.model_type == 0:
            _, self.model, self.temperature, self.h2o = MODELS_OO[self.model_idx_oo]

        # If model is Opx-Liq, get model and flags
        elif self.model_type == 1:
            _, self.model, self.temperature, self.h2o = MODELS_OL[self.model_idx_ol]


        if self.temperature_type == 1 and self.temperature == True:
            self.temperature_value_box.setEnabled(True)
        else:
            self.temperature_value_box.setEnabled(False)


        if self.temperature_type == 1 and self.temperature_model_oo == True:
            self.temperature_model_box_oo.setEnabled(True)
        else:
            self.temperature_model_box_oo.setEnabled(False)

        if self.temperature_type == 1 and self.temperature_model_ol == True:
            self.temperature_model_box_ol.setEnabled(True)
        else:
            self.temperature_model_box_ol.setEnabled(False)


        if self.temperature == False:
            self.box_1.setEnabled(False)
            self.temperature_value_box.setEnabled(False)
            self.temperature_model_box_oo.setEnabled(False)
            self.temperature_model_box_ol.setEnabled(False)
        else:
            self.box_1.setEnabled(True)


        if self.temperature_type == 1:
            self.temperature_value_box.setEnabled(True)
        else:
            self.temperature_value_box.setEnabled(False)


        if self.temperature_type == 2:
            if self.model_type == 0:
                self.temperature_model_box_oo.setEnabled(True)
                self.temperature_model_box_ol.setEnabled(False)
            elif self.model_type == 1:
                self.temperature_model_box_oo.setEnabled(False)
                self.temperature_model_box_ol.setEnabled(True)

        else:
            self.temperature_model_box_oo.setEnabled(False)
            self.temperature_model_box_ol.setEnabled(False)

        # Enable/disable H₂O box
        self.fixed_h2o_input.setEnabled(self.h2o and self.fixed_h2o)
        self.fixed_h2o_box.setEnabled(self.h2o)



        self.commit.deferred()

    # This function is called when the user changes the temperature input mode.
    def _radio_change_1(self):

        if self.temperature_type == 1:
            self.temperature_value_box.setEnabled(True)
        else:
            self.temperature_value_box.setEnabled(False)


        if self.temperature_type == 2:
            if self.model_type == 0:
                self.temperature_model_box_oo.setEnabled(True)
                self.temperature_model_box_ol.setEnabled(False)
            elif self.model_type == 1:
                self.temperature_model_box_oo.setEnabled(False)
                self.temperature_model_box_ol.setEnabled(True)

        else:
            self.temperature_model_box_oo.setEnabled(False)
            self.temperature_model_box_ol.setEnabled(False)

        self.commit.deferred()

    # Waits until user has finished playing with buttons
    def _value_change(self):

        self.commit.deferred()


    # Schedules a temp recalc if needed
    def _model_temperature_change(self):

        if self.model_type == 0:
            _, self.model_temperature = MODELS_TEMPERATURE_OO[self.model_idx_temperature_oo]

        elif self.model_type == 1:
            _, self.model_temperature = MODELS_TEMPERATURE_OL[self.model_idx_temperature_ol]

        self.commit.deferred()


    @Inputs.data

    def set_data(self, data):
        self.data = data
        self.commit.now()


    @gui.deferred

    # This function
    def commit(self):

        # clears messages in GUI
        self.clear_messages()
        self.Error.value_error.clear()
        self.Warning.value_error.clear()

        # Checks data is connected, if not, does nothing.
        if self.data is None:
            pass
        elif len(self.data.domain.attributes) > 1:

            # gets data into a dataframe
            df = pd.DataFrame(data=np.array(self.data.X), columns=[a.name for i, a in enumerate(self.data.domain.attributes)])

            if self.fixed_h2o:
                try:
                    water = float(self.fixed_h2o_value_str)
                except ValueError:
                    self.Error.value_error("Invalid H₂O value entered.")
                    return
            else:
                if self.h2o:
                    try:
                        water = df['H2O_Liq']
                    except:
                        water = 0
                        self.Warning.value_error("'H2O' column is not in Dataset, H₂O is set to zero.")
                else:
                    water = 0



            if self.temperature_type == 0:
                try:
                    T = df['T_K']
                except:
                    T = self.temperature_value
                    self.Warning.value_error("'T_K' column is not in Dataset")

            elif self.temperature_type == 1:
                T = self.temperature_value


            if self.model_type == 0:

                df = dm.preprocessing(df, my_output='opx_only')

                if self.temperature == False:
                    pressure = calculate_opx_only_press(opx_comps=df[opx_cols],  equationP=self.model, H2O_Liq=water)
                    #if pressure
                else:
                    if self.temperature_type == 2:
                        calc = calculate_opx_only_press_temp(opx_comps=df[opx_cols],
                                                                       equationP=self.model,
                                                                       equationT=self.model_temperature
                                                                      )
                        pressure = calc.iloc[:, 0]   # Pressure column
                        temperature_output = calc.iloc[:, 1]  # Temperature column (T_K)

                    else:
                        pressure = calculate_opx_only_press(opx_comps=df[opx_cols], equationP=self.model, T=T)

            elif self.model_type == 1:

                df = dm.preprocessing(df, my_output='opx_liq')

                if self.temperature == False:
                    pressure = calculate_opx_liq_press(opx_comps=df[opx_cols], liq_comps=df[liq_cols], equationP=self.model, H2O_Liq=water)
                else:
                    if  self.temperature_type == 2:
                        calc = calculate_opx_liq_press_temp(opx_comps=df[opx_cols],
                                                                      liq_comps=df[liq_cols],
                                                                      equationP=self.model,
                                                                      equationT=self.model_temperature, H2O_Liq=water)

                        pressure = calc.iloc[:, 0]   # Pressure column
                        temperature_output = calc.iloc[:, 1]  # Temperature column (T_K)
                    else:
                        pressure = calculate_opx_liq_press(opx_comps=df[opx_cols], liq_comps=df[liq_cols], equationP=self.model, T=T, H2O_Liq=water)

            # New logic to output temp as well
            if self.temperature_type == 2:
                # Temperature from model — output as T_K_output
                my_domain = Domain(
                    [ContinuousVariable(name=a.name) for a in self.data.domain.attributes],
                    [ContinuousVariable("P_kbar_output"), ContinuousVariable("T_K_output")],
                    metas=self.data.domain.metas
                )
                Y = np.column_stack([pressure, temperature_output])

            else:
                # Temperature was input — from dataset or fixed value
                if self.temperature_type == 0:
                    try:
                        T_out = df["T_K"]
                    except KeyError:
                        T_out = np.full(len(df), np.nan)
                        self.Warning.value_error("'T_K' column missing, cannot output T_K_input.")
                elif self.temperature_type == 1:
                    T_out = np.full(len(df), self.temperature_value)

                my_domain = Domain(
                    [ContinuousVariable(name=a.name) for a in self.data.domain.attributes],
                    [ContinuousVariable("P_kbar_output"), ContinuousVariable("T_K_input")],
                    metas=self.data.domain.metas
                )
                Y = np.column_stack([pressure, T_out])

            # Finalize and send output
            out = Table.from_numpy(my_domain, self.data.X, Y, self.data.metas)
            self.Outputs.data.send(out)







    # def __init__(self):
    #     OWWidget.__init__(self)
    #     self.data = None
    #
    #     # This can help when users open old projects with different indices
    #     # --- Reset invalid temperature_type early to prevent IndexError
    #     if self.temperature_type not in [0, 1, 2]:
    #         print(f"WARNING: Invalid temperature_type ({self.temperature_type}), resetting to 0")
    #         self.temperature_type = 0
    #
    #     # --- Set defaults
    #     self.model = MODELS_OO[self.model_idx_oo][1]
    #     self.model_temperature = None
    #
    #     # --- This gives you your first button, model_type=0 is Opx only, =1 is Opx-Liq
    #     box = gui.radioButtons(self.controlArea, self, "model_type", box="Models", callback=self._radio_change)
    #
    #     # This creates the button to produce the Opx-only drop down.
    #     button_oo = gui.appendRadioButton(box, "Opx-only")
    #
    #     self.models_combo_oo = gui.comboBox(
    #         gui.indentedBox(box, gui.checkButtonOffsetHint(button_oo)), self, "model_idx_oo",
    #         items=[m[0] for m in MODELS_OO], callback=self._model_combo_change)
    #
    #
    #     # This creates the drop down for Opx-Liq models
    #     button_ol = gui.appendRadioButton(box, "opx-liq")
    #     self.models_combo_ol = gui.comboBox(
    #         gui.indentedBox(box, gui.checkButtonOffsetHint(button_ol)), self, "model_idx_ol",
    #         items=[m[0] for m in MODELS_OL], callback=self._model_combo_change)
    #
    #

    #
    #     # --- Temperature radio group
    #     self.box_1 = gui.radioButtons(self.controlArea, self, "temperature_type", box="Temperature", callback=self._radio_change_1)
    #
    #     # 1️⃣ Dataset-based T
    #     self.button_dataset = gui.appendRadioButton(self.box_1, "Dataset_as_Temperature_(K)")
    #
    #     # 2️⃣ Fixed T
    #     self.button_fixed = gui.appendRadioButton(self.box_1, "Fixed_Temperature")
    #     self.temperature_value_box = gui.spin(
    #         gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_fixed)),
    #         self, "temperature_value", 1, 10000,
    #         label="Temperature_value_(K)", alignment=Qt.AlignRight,
    #         callback=self._value_change, controlWidth=80
    #     )
    #
    #     # 3️⃣ Model-derived T
    #     self.button_model = gui.appendRadioButton(self.box_1, "Model_as_Temperature")
    #     self.temperature_model_box_oo = gui.comboBox(
    #         gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_model)),
    #         self, "model_idx_temperature_oo",
    #         items=[m[0] for m in MODELS_TEMPERATURE_OO],
    #         callback=self._model_temperature_change
    #     )
    #     self.temperature_model_box_ol = gui.comboBox(
    #         gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_model)),
    #         self, "model_idx_temperature_ol",
    #         items=[m[0] for m in MODELS_TEMPERATURE_OL],
    #         callback=self._model_temperature_change
    #     )
    #
    #     # --- Initial enabling/disabling state
    #     self.box_1.setEnabled(False)
    #     self.models_combo_oo.setEnabled(True)
    #     self.models_combo_ol.setEnabled(False)
    #
    #     # --- Auto-apply toggle
    #     gui.auto_apply(self.buttonsArea, self)
    #
    #     # --- Apply initial radio state
    #     self._radio_change()
    #
    #
    #
    # def _radio_change(self):
    #     if self.model_type == 0:
    #         _, self.model, self.temperature, self.h2o = MODELS_OO[self.model_idx_oo]
    #         self.models_combo_oo.setEnabled(True)
    #         self.models_combo_ol.setEnabled(False)
    #     elif self.model_type == 1:
    #         _, self.model, self.temperature, self.h2o = MODELS_OL[self.model_idx_ol]
    #         _, self.model_temperature = MODELS_TEMPERATURE_OL[self.model_idx_temperature_ol]
    #         self.models_combo_oo.setEnabled(False)
    #         self.models_combo_ol.setEnabled(True)
    #
    #     # Enable temperature box if model requires it
    #     self.box_1.setEnabled(self.temperature)
    #
    #     # Disable all by default
    #     self.temperature_value_box.setEnabled(False)
    #     self.temperature_model_box_oo.setEnabled(False)
    #     self.temperature_model_box_ol.setEnabled(False)
    #
    #     self.button_fixed.setEnabled(False)
    #     self.button_dataset.setEnabled(False)
    #     self.button_model.setEnabled(False)
    #
    #     if self.temperature:
    #         self.button_fixed.setEnabled(True)
    #         self.button_dataset.setEnabled(True)
    #         self.button_model.setEnabled(self.model_type == 1)
    #
    #         if self.temperature_type == 1:
    #             self.temperature_value_box.setEnabled(True)
    #         elif self.temperature_type == 2:
    #             if self.model_type == 0:
    #                 self.temperature_model_box_oo.setEnabled(True)
    #             elif self.model_type == 1:
    #                 self.temperature_model_box_ol.setEnabled(True)
    #
    #     self._update_temperature_model_visibility()
    #     self.commit.deferred()
    #     print(f"Using model: {self.model}")
    #
    #
    #
    # def _update_temperature_model_visibility(self):
    #     self.temperature_model_box_oo.setVisible(self.model_type == 0 and self.temperature_type == 2)
    #     self.temperature_model_box_ol.setVisible(self.model_type == 1 and self.temperature_type == 2)
    #
    #
    # def _model_combo_change(self):
    #
    #     if self.model_type == 0:
    #         _, self.model, self.temperature, self.h2o = MODELS_OO[self.model_idx_oo]
    #
    #     elif self.model_type == 1:
    #         _, self.model, self.temperature, self.h2o = MODELS_OL[self.model_idx_ol]
    #
    #     if self.temperature_type == 1 and self.temperature == True:
    #         self.temperature_value_box.setEnabled(True)
    #     else:
    #         self.temperature_value_box.setEnabled(False)
    #
    #
    #     if self.temperature_type == 1 and self.temperature_model_oo == True:
    #         self.temperature_model_box_oo.setEnabled(True)
    #     else:
    #         self.temperature_model_box_oo.setEnabled(False)
    #
    #     if self.temperature_type == 1 and self.temperature_model_ol == True:
    #         self.temperature_model_box_ol.setEnabled(True)
    #     else:
    #         self.temperature_model_box_ol.setEnabled(False)
    #
    #
    #     if self.temperature == False:
    #         self.box_1.setEnabled(False)
    #         self.temperature_value_box.setEnabled(False)
    #         self.temperature_model_box_oo.setEnabled(False)
    #         self.temperature_model_box_ol.setEnabled(False)
    #     else:
    #         self.box_1.setEnabled(True)
    #
    #
    #     if self.temperature_type == 1:
    #         self.temperature_value_box.setEnabled(True)
    #     else:
    #         self.temperature_value_box.setEnabled(False)
    #
    #
    #     if self.temperature_type == 2:
    #         if self.model_type == 0:
    #             self.temperature_model_box_oo.setEnabled(True)
    #             self.temperature_model_box_ol.setEnabled(False)
    #         elif self.model_type == 1:
    #             self.temperature_model_box_oo.setEnabled(False)
    #             self.temperature_model_box_ol.setEnabled(True)
    #
    #     else:
    #         self.temperature_model_box_oo.setEnabled(False)
    #         self.temperature_model_box_ol.setEnabled(False)
    #
    #
    #     self.commit.deferred()
    #
    #
    # def _radio_change_1(self):
    #     self.temperature_value_box.setEnabled(False)
    #     self.temperature_model_box_oo.setEnabled(False)
    #     self.temperature_model_box_ol.setEnabled(False)
    #
    #     if self.temperature_type == 1:
    #         self.temperature_value_box.setEnabled(True)
    #     elif self.temperature_type == 2:
    #         if self.model_type == 0:
    #             self.temperature_model_box_oo.setEnabled(True)
    #         elif self.model_type == 1:
    #             self.temperature_model_box_ol.setEnabled(True)
    #
    #     self._update_temperature_model_visibility()
    #     self.commit.deferred()
    #
    #
    #
    # def _value_change(self):
    #
    #     self.commit.deferred()
    #
    #
    # def _model_temperature_change(self):
    #
    #     if self.model_type == 0:
    #         self.model_temperature = None  # or skip this line entirely
    #     elif self.model_type == 1:
    #         _, self.model_temperature = MODELS_TEMPERATURE_OL[self.model_idx_temperature_ol]
    #
    #     self.commit.deferred()
    #
    #
    # @Inputs.data
    #
    # def set_data(self, data):
    #     self.data = data
    #     self.commit.now()
    #
    #
    # @gui.deferred
    # def commit(self):
    #     print("Running commit()")
    #
    #
    #     self.clear_messages()
    #     self.Error.value_error.clear()
    #     self.Warning.value_error.clear()
    #
    #     if self.data is None:
    #         pass
    #     elif len(self.data.domain.attributes) > 1:
    #
    #         df = pd.DataFrame(data=np.array(self.data.X), columns=[a.name for i, a in enumerate(self.data.domain.attributes)])
    #
    #         # H2O in Dataset
    #         if self.h2o == True:
    #             try:
    #                 water = df['H2O_Liq']
    #             except:
    #                 water = 0
    #                 self.Warning.value_error("'H2O_Liq' column is not in Dataset, H2O is set to zero.")
    #         else:
    #             water = 0
    #
    #
    #         if self.temperature_type == 0:
    #             if 'T_K' not in df.columns:
    #                 self.Error.value_error("'T_K' column is missing from the dataset but required for temperature input.")
    #                 return
    #             T = df['T_K']
    #
    #         elif self.temperature_type == 1:
    #             T = self.temperature_value
    #
    #
    #         if self.model_type == 0:
    #             df = dm.preprocessing(df, my_output='opx_only')
    #
    #             if not self.temperature:
    #                 pressure = calculate_opx_only_press(opx_comps=df[opx_cols], equationP=self.model, H2O_Liq=water)
    #             else:
    #                 # Only use T, do NOT support model-based temperature (temperature_type == 2)
    #                 pressure = calculate_opx_only_press(opx_comps=df[opx_cols], equationP=self.model, T=T)
    #
    #
    #         elif self.model_type == 1:
    #
    #             df = dm.preprocessing(df, my_output='opx_liq')
    #
    #             if self.temperature == False:
    #                 pressure = calculate_opx_liq_press(opx_comps=df[opx_cols], liq_comps=df[liq_cols], equationP=self.model, H2O_Liq=water)
    #             else:
    #                 if  self.temperature_type == 2:
    #                     pressure = calculate_opx_liq_press_temp(opx_comps=df[opx_cols],
    #                                                                   liq_comps=df[liq_cols],
    #                                                                   equationP=self.model_temperature,
    #                                                                   equationT=self.model, H2O_Liq=water).iloc[:,0]
    #                 else:
    #                     pressure = calculate_opx_liq_press(opx_comps=df[opx_cols], liq_comps=df[liq_cols], equationP=self.model, T=T, H2O_Liq=water)
    #
    #         my_domain = Domain([ContinuousVariable(name=a.name) for i, a in enumerate(self.data.domain.attributes)],
    #                         ContinuousVariable.make("P_kbar_output"), metas=self.data.domain.metas)
    #
    #         out = Table.from_numpy(my_domain, self.data.X,pressure, self.data.metas)
    #
    #
    #         self.Outputs.data.send(out)

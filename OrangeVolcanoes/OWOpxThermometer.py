import numpy as np
import pandas as pd
from Orange.data import Table, ContinuousVariable, Domain
from Orange.widgets.settings import Setting, ContextSetting
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from orangewidget.widget import Msg
from Thermobar import  calculate_opx_liq_temp,  calculate_opx_liq_press_temp

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
# First tuple indicates whether model requires a PRESSURE, second whether it requires water.



# Opx-Liq temp
MODELS_OL = [
    ('T_Put2008_eq28a', 'T_Put2008_eq28a', True, True),
        ('T_Put2008_eq28b_opx_sat', 'T_Put2008_eq28b_opx_sat', True, True),
        ('T_Beatt1993_opx', 'T_Beatt1993_opx', True, False),
]


# Opx only pressure
MODELS_OO = [
 ('None_available', ''),
]



# Opx only pressure -
MODELS_PRESSURE_OO = [
 ('P_Put2008_eq29c', 'P_Put2008_eq29c')
]

MODELS_PRESSURE_OL = [
    ('P_Put2008_eq29a', 'P_Put2008_eq29a'),
    ('P_Put2008_eq29b', 'P_Put2008_eq29b'),
    ('P_Put_Global_Opx', 'P_Put_Global_Opx'),
     ('P_Put_Felsic_Opx', 'P_Put_Felsic_Opx'),
]


## Directly adapted from the opx one.
class OWOpxThermometer(OWWidget):
    name = "OpxThermometer"
    description = "The widget allows the user to determine the temperature of Opx formation/re-equilibration using its chemical composition or the composition of orthopyroxene liquid pairs as input data."
    icon = "icons/Opx_Thermometer_icon.png"
    priority = 5
    keywords = ['Opx', 'Thermometer']

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        data = Output("Data", Table, dynamic=False)

    GENERIC = 0
    FROM_VAR = 0

    #  0 is using PRESSURE from a column in the dataset. 1 is using a fixed value entered by the user.
    # 2 is iterating with an equation.

    VALID_PRESSURE_TYPES = [0, 1, 2]

    model_type = ContextSetting(GENERIC)
    PRESSURE_type = ContextSetting(GENERIC)

    resizing_enabled = False
    want_main_area = False


    model_idx_oo = 0 #Setting(0)
    model_idx_ol = 0 #Setting(0)

    model_idx_PRESSURE_oo = Setting(0)
    model_idx_PRESSURE_ol = Setting(0)
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
        button = gui.appendRadioButton(box, "Opx-only thermometers")

        self.models_combo_oo = gui.comboBox(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button)), self, "model_idx_oo",
            items=[m[0] for m in MODELS_OO],
            callback=self._model_combo_change
        )

        _ = MODELS_OO[self.model_idx_oo]
        self.model = None
        self.PRESSURE = False
        self.h2o = False



        #opx-liq GUI
        gui.appendRadioButton(box, "Opx-liq thermometers")

        self.models_combo_ol = gui.comboBox(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button)), self, "model_idx_ol",
            items=[m[0] for m in MODELS_OL],
            callback=self._model_combo_change

        )

        # This creates the box for how PRESSURE is handled.
        self.box_1 = gui.radioButtons(
            self.controlArea, self, "PRESSURE_type", box="PRESSURE",
            callback=self._radio_change_1)


        #Dataset as PRESSURE GUI
        self.button_1 = gui.appendRadioButton(self.box_1, "Dataset_as_PRESSURE_(kbar)")

        #Fixed PRESSURE GUI
        gui.appendRadioButton(self.box_1, "Fixed_PRESSURE")

        self.PRESSURE_value_box = gui.doubleSpin(
            gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1)), self,
            "PRESSURE_value", 1.0, 10000.0, step=0.1,
            label="PRESSURE_value_(kbar)",
            alignment=Qt.AlignRight, callback=self._value_change,
            controlWidth=80, decimals=1)


        # Model as PRESSURE
        gui.appendRadioButton(self.box_1, "Model_as_PRESSURE")

        # Add label: Opx-only barometers
        opx_only_box = gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1))
        gui.label(opx_only_box, self, "Opx-only barometers")
        self.PRESSURE_model_box_oo = gui.comboBox(
            opx_only_box, self, "model_idx_PRESSURE_oo",
            items=[m[0] for m in MODELS_PRESSURE_OO],
            callback=self._model_PRESSURE_change)

        # Add label: Opx-Liq barometers
        opx_liq_box = gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1))
        gui.label(opx_liq_box, self, "Opx-Liq barometers")

        self.PRESSURE_model_box_ol = gui.comboBox(
            opx_liq_box, self, "model_idx_PRESSURE_ol",
            items=[m[0] for m in MODELS_PRESSURE_OL],
            callback=self._model_PRESSURE_change)

        _, self.model_PRESSURE = MODELS_PRESSURE_OO[self.model_idx_PRESSURE_oo]


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
        # Set model and pressure flags
        if self.model_type == 0:
            _, self.model, self.PRESSURE, self.h2o = MODELS_OO[self.model_idx_oo]
            self.model_PRESSURE = None
            self.PRESSURE_model_oo = True
            self.PRESSURE_model_ol = False
            self.models_combo_oo.setEnabled(True)
            self.models_combo_ol.setEnabled(False)
        elif self.model_type == 1:
            _, self.model, self.PRESSURE, self.h2o = MODELS_OL[self.model_idx_ol]
            _, self.model_PRESSURE = MODELS_PRESSURE_OL[self.model_idx_PRESSURE_ol]
            self.PRESSURE_model_oo = False
            self.PRESSURE_model_ol = True
            self.models_combo_oo.setEnabled(False)
            self.models_combo_ol.setEnabled(True)

        # Handle visibility of PRESSURE entry and combo boxes
        self.PRESSURE_value_box.setEnabled(self.PRESSURE and self.PRESSURE_type == 1)

        if self.PRESSURE_type == 2:
            self.PRESSURE_model_box_oo.setEnabled(self.model_type == 0)
            self.PRESSURE_model_box_ol.setEnabled(self.model_type == 1)
        else:
            self.PRESSURE_model_box_oo.setEnabled(False)
            self.PRESSURE_model_box_ol.setEnabled(False)

        self.box_1.setEnabled(self.PRESSURE)

        # Enable H₂O override widgets
        self.fixed_h2o_input.setEnabled(self.h2o and self.fixed_h2o)
        self.fixed_h2o_box.setEnabled(self.h2o)

        self.commit.deferred()




    # Triggered when user changes the model.
    def _model_combo_change(self):

        # If model is Opx-only, get model and flags
        if self.model_type == 0:
            _, self.model, self.PRESSURE, self.h2o = MODELS_OO[self.model_idx_oo]

        # If model is Opx-Liq, get model and flags
        elif self.model_type == 1:
            _, self.model, self.PRESSURE, self.h2o = MODELS_OL[self.model_idx_ol]


        if self.PRESSURE_type == 1 and self.PRESSURE == True:
            self.PRESSURE_value_box.setEnabled(True)
        else:
            self.PRESSURE_value_box.setEnabled(False)


        if self.PRESSURE_type == 1 and self.PRESSURE_model_oo == True:
            self.PRESSURE_model_box_oo.setEnabled(True)
        else:
            self.PRESSURE_model_box_oo.setEnabled(False)

        if self.PRESSURE_type == 1 and self.PRESSURE_model_ol == True:
            self.PRESSURE_model_box_ol.setEnabled(True)
        else:
            self.PRESSURE_model_box_ol.setEnabled(False)


        if self.PRESSURE == False:
            self.box_1.setEnabled(False)
            self.PRESSURE_value_box.setEnabled(False)
            self.PRESSURE_model_box_oo.setEnabled(False)
            self.PRESSURE_model_box_ol.setEnabled(False)
        else:
            self.box_1.setEnabled(True)


        if self.PRESSURE_type == 1:
            self.PRESSURE_value_box.setEnabled(True)
        else:
            self.PRESSURE_value_box.setEnabled(False)


        if self.PRESSURE_type == 2:
            self.PRESSURE_model_box_oo.setEnabled(self.model_type == 0)
            self.PRESSURE_model_box_ol.setEnabled(self.model_type == 1)
        else:
            self.PRESSURE_model_box_oo.setEnabled(False)
            self.PRESSURE_model_box_ol.setEnabled(False)


        # Enable/disable H₂O box
        self.fixed_h2o_input.setEnabled(self.h2o and self.fixed_h2o)
        self.fixed_h2o_box.setEnabled(self.h2o)




        self.commit.deferred()

    # This function is called when the user changes the PRESSURE input mode.
    def _radio_change_1(self):

        if self.PRESSURE_type == 1:
            self.PRESSURE_value_box.setEnabled(True)
        else:
            self.PRESSURE_value_box.setEnabled(False)


        if self.PRESSURE_type == 2:
            if self.model_type == 0:
                self.PRESSURE_model_box_oo.setEnabled(True)
                self.PRESSURE_model_box_ol.setEnabled(False)
            elif self.model_type == 1:
                self.PRESSURE_model_box_oo.setEnabled(False)
                self.PRESSURE_model_box_ol.setEnabled(True)

        else:
            self.PRESSURE_model_box_oo.setEnabled(False)
            self.PRESSURE_model_box_ol.setEnabled(False)

        self.commit.deferred()

    # Waits until user has finished playing with buttons
    def _value_change(self):

        self.commit.deferred()


    # Schedules a temp recalc if needed
    def _model_PRESSURE_change(self):

        if self.model_type == 0:
            _, self.model_PRESSURE = MODELS_PRESSURE_OO[self.model_idx_PRESSURE_oo]

        elif self.model_type == 1:
            _, self.model_PRESSURE = MODELS_PRESSURE_OL[self.model_idx_PRESSURE_ol]

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



            if self.PRESSURE_type == 0:
                try:
                    P = df['P_kbar']
                except:
                    P = self.PRESSURE_value
                    self.Warning.value_error("'P_kbar' column is not in Dataset")

            elif self.PRESSURE_type == 1:
                P = self.PRESSURE_value


            if self.model_type == 0:
                if self.model_type == 0:
                    raise NotImplementedError("Opx-only thermometers are not yet implemented.")


                # If one comes along
                # df = dm.preprocessing(df, my_output='opx_only')
                #
                # if self.PRESSURE == False:
                #     temperature = calculate_opx_only_temp(opx_comps=df[opx_cols],  equationT=self.model, H2O_Liq=water)
                #     #if pressure
                # else:
                #     if self.PRESSURE_type == 2:
                #         calc = calculate_opx_only_press_temp(opx_comps=df[opx_cols],
                #                                                        equationT=self.model,
                #                                                        equationP=self.model_PRESSURE
                #                                                       )
                #         temperature =calc['T_K_calc']    # temp column
                #         PRESSURE_output = calc['P_kbar_calc'] # PRESSURE column
                #
                #     else:
                #         temperature = calculate_opx_only_temp(opx_comps=df[opx_cols], equationT=self.model, P=P)

            elif self.model_type == 1:

                df = dm.preprocessing(df, my_output='opx_liq')

                if self.PRESSURE == False:
                    temperature = calculate_opx_liq_temp(opx_comps=df[opx_cols], liq_comps=df[liq_cols], equationT=self.model, H2O_Liq=water)
                else:
                    if  self.PRESSURE_type == 2:
                        calc = calculate_opx_liq_press_temp(opx_comps=df[opx_cols],
                                                                      liq_comps=df[liq_cols],
                                                                      equationT=self.model,
                                                                      equationP=self.model_PRESSURE, H2O_Liq=water)

                        temperature = calc['T_K_calc']    # temp column
                        PRESSURE_output = calc['P_kbar_calc'] # PRESSURE column
                    else:
                        temperature = calculate_opx_liq_temp(opx_comps=df[opx_cols], liq_comps=df[liq_cols], equationT=self.model, P=P, H2O_Liq=water)

            # New logic to output temp as well
            if self.PRESSURE_type == 2:
                # PRESSURE from model — output as T_K_output
                my_domain = Domain(
                    [ContinuousVariable(name=a.name) for a in self.data.domain.attributes],
                    [ContinuousVariable("T_K_output"), ContinuousVariable("P_kbar_output")],
                    metas=self.data.domain.metas
                )
                Y = np.column_stack([temperature, PRESSURE_output])

            else:
                # PRESSURE was input — from dataset or fixed value
                if self.PRESSURE_type == 0:
                    try:
                        P_out = df["P_kbar"]
                    except KeyError:
                        P_out = np.full(len(df), np.nan)
                        self.Warning.value_error("'P_kbar' column missing, cannot output P_kbar_input.")
                elif self.PRESSURE_type == 1:
                    P_out = np.full(len(df), self.PRESSURE_value)

                my_domain = Domain(
                    [ContinuousVariable(name=a.name) for a in self.data.domain.attributes],
                    [ContinuousVariable("T_K_output"), ContinuousVariable("P_kbar_input")],
                    metas=self.data.domain.metas
                )
                Y = np.column_stack([temperature, P_out])

            # Finalize and send output
            out = Table.from_numpy(my_domain, self.data.X, Y, self.data.metas)
            self.Outputs.data.send(out)




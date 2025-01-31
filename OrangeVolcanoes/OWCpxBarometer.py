import numpy as np
import pandas as pd
from Orange.data import Table, ContinuousVariable, Domain
from Orange.widgets.settings import Setting, ContextSetting
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from orangewidget.widget import Msg
from Thermobar import calculate_cpx_only_press, calculate_cpx_only_press_temp, calculate_cpx_liq_press, calculate_cpx_liq_press_temp
from OrangeVolcanoes.utils import dataManipulation as dm
from AnyQt.QtCore import Qt
    

liq_cols = ['SiO2_Liq', 'TiO2_Liq', 'Al2O3_Liq',
'FeOt_Liq', 'MnO_Liq', 'MgO_Liq', 'CaO_Liq', 'Na2O_Liq', 'K2O_Liq',
'Cr2O3_Liq', 'P2O5_Liq', 'H2O_Liq', 'Fe3Fet_Liq', 'NiO_Liq', 'CoO_Liq',
 'CO2_Liq']

cpx_cols = ['SiO2_Cpx', 'TiO2_Cpx', 'Al2O3_Cpx',
'FeOt_Cpx','MnO_Cpx', 'MgO_Cpx', 'CaO_Cpx', 'Na2O_Cpx', 'K2O_Cpx',
'Cr2O3_Cpx']


MODELS_CO = [
    ('P_Wang2021_eq1', 'P_Wang2021_eq1',False),
    ('P_Put2008_eq32a', 'P_Put2008_eq32a',True),
    ('P_Put2008_eq32b', 'P_Put2008_eq32b',True),
    #('P_Petrelli2020_Cpx_only_(ML)', 'P_Petrelli2020_Cpx_only',False),
    ('P_Petrelli2020_Cpx_only(ML)', 'P_Petrelli2020_Cpx_only_onnx',False),
    #('P_Jorgenson2022_Cpx_only_Norm_(ML)', 'P_Jorgenson2022_Cpx_only_Norm',False),
    #('P_Jorgenson2022_Cpx_only_(ML)', 'P_Jorgenson2022_Cpx_only',False),
    ('P_Jorgenson2022_Cpx_only(ML)', 'P_Jorgenson2022_Cpx_only_onnx',False),
    ('P_Petrelli2020_Cpx_only_withH2O_(ML)', 'P_Petrelli2020_Cpx_only_withH2O',False),
    ('P_Nimis1999_BA', 'P_Nimis1999_BA',False)
]


MODELS_CL = [
    ('P_Put1996_eqP1', 'P_Put1996_eqP1',True),
    ('P_Mas2013_eqPalk1', 'P_Mas2013_eqPalk1',True),
    ('P_Put1996_eqP2', 'P_Put1996_eqP2',True),
    #('P_Mas2013_eqPalk2', 'P_Mas2013_eqPalk2',True),
    ('P_Put2003', 'P_Put2003',True),
    ('P_Put2008_eq30', 'P_Put2008_eq30',True),
    ('P_Put2008_eq31', 'P_Put2008_eq31',True),
    ('P_Put2008_eq32c', 'P_Put2008_eq32c',True),
    ('P_Mas2013_eqalk32c', 'P_Mas2013_eqalk32c',True),
    ('P_Mas2013_Palk2012', 'P_Mas2013_Palk2012',False),
    ('P_Neave2017', 'P_Neave2017',True),
    #('P_Petrelli2020_Cpx_Liq_(ML)', 'P_Petrelli2020_Cpx_Liq',False),
    ('P_Petrelli2020_Cpx_Liq(ML)', 'P_Petrelli2020_Cpx_Liq_onnx',False),
    ('P_Jorgenson2022_Cpx_Liq_Norm_(ML)', 'P_Jorgenson2022_Cpx_Liq_Norm',False),
    #('P_Jorgenson2022_Cpx_Liq(ML)', 'P_Jorgenson2022_Cpx_Liq',False),
    ('P_Jorgenson2022_Cpx_Liq(ML)', 'P_Jorgenson2022_Cpx_Liq_onnx',False)
]


MODELS_TEMPERATURE_CO = [
    ('T_Put2008_eq32d', 'T_Put2008_eq32d'),
    ('T_Put2008_eq32d_subsol', 'T_Put2008_eq32d_subsol')
]


MODELS_TEMPERATURE_CL = [
    ('T_Put1996_eqT2', 'T_Put1996_eqT2'),
    ('T_Put1999', 'T_Put1999'),
    ('T_Put2003', 'T_Put2003'),
    ('T_Put2008_eq33', 'T_Put2008_eq33'),
    ('T_Put2008_eq34_cpx_sat', 'T_Put2008_eq34_cpx_sat'),
    ('T_Mas2013_eqTalk2', 'T_Mas2013_eqTalk2'),
    ('T_Mas2013_eqalk33', 'T_Mas2013_eqalk33')
]


class OWCpxBarometer(OWWidget):
    name = "CpxBarometer"
    description = "CpxBarometer"
    icon = "icons/CpxBaromether.png"
    priority = 4
    keywords = ['Cpx', 'Baromether']

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        data = Output("Data", Table, dynamic=False)

    GENERIC = 0
    FROM_VAR = 0 

    model_type = ContextSetting(GENERIC)
    temperature_type = ContextSetting(GENERIC)

    resizing_enabled = False 
    want_main_area = False  


    model_idx_co = Setting(0)
    model_idx_cl = Setting(0)

    model_idx_temperature_co = Setting(0)
    model_idx_temperature_cl = Setting(0)

    temperature = Setting(True)
    temperature_model_co = Setting(False)
    temperature_model_cl = Setting(False)

    temperature_value = Setting(1000)

    auto_apply = Setting(True)



    class Error(OWWidget.Error):
        value_error = Msg("{}")



    def __init__(self):
        OWWidget.__init__(self)
        self.data = None

        box = gui.radioButtons(
            self.controlArea, self, "model_type", box="Models",
            callback=self._radio_change)


        #Cpx-only GUI
        button = gui.appendRadioButton(box, "Cpx-only")

        self.models_combo_co = gui.comboBox(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button)), self, "model_idx_co",
            items=[m[0] for m in MODELS_CO],
            callback=self._model_combo_change
        )


        _, self.model, temperature = MODELS_CO[self.model_idx_co]
        

        #Cpx-liq GUI
        gui.appendRadioButton(box, "Cpx-liq")

        self.models_combo_cl = gui.comboBox(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button)), self, "model_idx_cl",
            items=[m[0] for m in MODELS_CL],
            callback=self._model_combo_change

        )


        self.box_1 = gui.radioButtons(
            self.controlArea, self, "temperature_type", box="Temperature",
            callback=self._radio_change_1)


        #Dataset as Pressure GUI
        self.button_1 = gui.appendRadioButton(self.box_1, "Dataset_as_Temperature_(°C)")   

        #Fixed Pressure GUI
        gui.appendRadioButton(self.box_1, "Fixed_Temperature")

        self.temperature_value_box = gui.spin(
            gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1)), self, "temperature_value", 1, 10000, label="Temperature_value_(°C)",
            alignment=Qt.AlignRight, callback=self._value_change,
            controlWidth=80)

        #Model as Pressure
        gui.appendRadioButton(self.box_1, "Model_as_Temperature")

        self.temperature_model_box_co = gui.comboBox(
            gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1)),  self, "model_idx_temperature_co",
            items=[m[0] for m in MODELS_TEMPERATURE_CO],
            callback=self._model_temperature_change)

        _, self.model_temperature = MODELS_TEMPERATURE_CO[self.model_idx_temperature_co]

        self.temperature_model_box_cl = gui.comboBox(
            gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1)),  self, "model_idx_temperature_cl",
            items=[m[0] for m in MODELS_TEMPERATURE_CL],
            callback=self._model_temperature_change)

        self.box_1.setEnabled(False)

        self.models_combo_co.setEnabled(True)
        self.models_combo_cl.setEnabled(False)

        gui.auto_apply(self.buttonsArea, self)


    def _radio_change(self):

        if self.model_type == 0:
            _, self.model, self.temperature = MODELS_CO[self.model_idx_co]
            _, self.model_temperature = MODELS_TEMPERATURE_CO[self.model_idx_temperature_co]
            self.models_combo_co.setEnabled(True)
            self.models_combo_cl.setEnabled(False)

        elif self.model_type == 1:
            _, self.model, self.temperature = MODELS_CL[self.model_idx_cl]
            _, self.model_temperature = MODELS_TEMPERATURE_CL[self.model_idx_temperature_cl]
            self.models_combo_co.setEnabled(False)
            self.models_combo_cl.setEnabled(True)


        if self.temperature_type == 1 and self.temperature == True:
            self.temperature_value_box.setEnabled(True)
        else:
            self.temperature_value_box.setEnabled(False)


        if self.temperature_type == 1 and self.temperature_model_co == True:
            self.temperature_model_box_co.setEnabled(True)
        else:
            self.temperature_model_box_co.setEnabled(False)

        if self.temperature_type == 1 and self.temperature_model_cl == True:
            self.temperature_model_box_cl.setEnabled(True)
        else:
            self.temperature_model_box_cl.setEnabled(False)


        if self.temperature == False:
            self.box_1.setEnabled(False)
            self.temperature_value_box.setEnabled(False)
            self.temperature_model_box_co.setEnabled(False)
            self.temperature_model_box_cl.setEnabled(False)
        else: 
            self.box_1.setEnabled(True)


        if self.temperature_type == 1:
            self.temperature_value_box.setEnabled(True)
        else:
            self.temperature_value_box.setEnabled(False)


        if self.temperature_type == 2:
            if self.model_type == 0:
                self.temperature_model_box_co.setEnabled(True)
                self.temperature_model_box_cl.setEnabled(False)
            elif self.model_type == 1:
                self.temperature_model_box_co.setEnabled(False)
                self.temperature_model_box_cl.setEnabled(True)

        else:
            self.temperature_model_box_co.setEnabled(False)
            self.temperature_model_box_cl.setEnabled(False)
                
                
        self.commit.deferred()    


    def _model_combo_change(self):

        if self.model_type == 0:
            _, self.model, self.temperature = MODELS_CO[self.model_idx_co]

        elif self.model_type == 1:
            _, self.model, self.temperature = MODELS_CL[self.model_idx_cl]


        if self.temperature_type == 1 and self.temperature == True:
            self.temperature_value_box.setEnabled(True)
        else:
            self.temperature_value_box.setEnabled(False)


        if self.temperature_type == 1 and self.temperature_model_co == True:
            self.temperature_model_box_co.setEnabled(True)
        else:
            self.temperature_model_box_co.setEnabled(False)

        if self.temperature_type == 1 and self.temperature_model_cl == True:
            self.temperature_model_box_cl.setEnabled(True)
        else:
            self.temperature_model_box_cl.setEnabled(False)


        if self.temperature == False:
            self.box_1.setEnabled(False)
            self.temperature_value_box.setEnabled(False)
            self.temperature_model_box_co.setEnabled(False)
            self.temperature_model_box_cl.setEnabled(False)
        else: 
            self.box_1.setEnabled(True)


        if self.temperature_type == 1:
            self.temperature_value_box.setEnabled(True)
        else:
            self.temperature_value_box.setEnabled(False)


        if self.temperature_type == 2:
            if self.model_type == 0:
                self.temperature_model_box_co.setEnabled(True)
                self.temperature_model_box_cl.setEnabled(False)
            elif self.model_type == 1:
                self.temperature_model_box_co.setEnabled(False)
                self.temperature_model_box_cl.setEnabled(True)

        else:
            self.temperature_model_box_co.setEnabled(False)
            self.temperature_model_box_cl.setEnabled(False)
                
                
        self.commit.deferred()  


    def _radio_change_1(self):

        if self.temperature_type == 1:
            self.temperature_value_box.setEnabled(True)
        else:
            self.temperature_value_box.setEnabled(False)


        if self.temperature_type == 2:
            if self.model_type == 0:
                self.temperature_model_box_co.setEnabled(True)
                self.temperature_model_box_cl.setEnabled(False)
            elif self.model_type == 1:
                self.temperature_model_box_co.setEnabled(False)
                self.temperature_model_box_cl.setEnabled(True)

        else:
            self.temperature_model_box_co.setEnabled(False)
            self.temperature_model_box_cl.setEnabled(False)
                
        self.commit.deferred()    


    def _value_change(self):

        self.commit.deferred()


    def _model_temperature_change(self):

        if self.model_type == 0:
            _, self.model_temperature = MODELS_TEMPERATURE_CO[self.model_idx_temperature_co]

        elif self.model_type == 1:
            _, self.model_temperature = MODELS_TEMPERATURE_CL[self.model_idx_temperature_cl]

        self.commit.deferred()


    @Inputs.data
    
    def set_data(self, data):
        self.data = data
        self.commit.now()

    
    @gui.deferred
    def commit(self):


        self.clear_messages()

        if self.data is None:
            pass
        elif len(self.data.domain.attributes) > 1:

            df = pd.DataFrame(data=np.array(self.data.X), columns=[a.name for i, a in enumerate(self.data.domain.attributes)])

            if self.temperature_type == 0:
                try:
                    T = df['T_C'] + 273.15
                except:
                    T = self.temperature_value
                
            elif self.temperature_type == 1:
                T = self.temperature_value


            if self.model_type == 0: 

                df = dm.preprocessing(df, my_output='cpx_only')

                if self.temperature == False:
                    pressure = calculate_cpx_only_press(cpx_comps=df[cpx_cols],  equationP=self.model)
                else:
                    if self.temperature_type == 2:
                        pressure = calculate_cpx_only_press_temp(cpx_comps=df[cpx_cols],
                                                                       equationP=self.model_temperature,
                                                                       equationT=self.model).iloc[:,0] 
                    else:
                        pressure = calculate_cpx_only_press(cpx_comps=df[cpx_cols], equationP=self.model, T=T) 

            elif self.model_type == 1: 

                df = dm.preprocessing(df, my_output='cpx_liq')

                if self.temperature == False:
                    presssure = calculate_cpx_liq_press(cpx_comps=df[cpx_cols], liq_comps=df[liq_cols], equationP=self.model)
                else:
                    if  self.temperature_type == 2:
                        pressure = calculate_cpx_liq_press_temp(cpx_comps=df[cpx_cols],
                                                                      liq_comps=df[liq_cols],
                                                                      equationP=self.model_temperature,
                                                                      equationT=self.model).iloc[:,0]
                    else:
                        pressure = calculate_cpx_liq_press(cpx_comps=df[cpx_cols], liq_comps=df[liq_cols], equationP=self.model, T=T)



            my_domain = Domain([ContinuousVariable(name=a.name) for i, a in enumerate(self.data.domain.attributes)],
                            ContinuousVariable.make("Pressure_bar_output"), metas=self.data.domain.metas)

            out = Table.from_numpy(my_domain, self.data.X,pressure, self.data.metas)


            self.Outputs.data.send(out)

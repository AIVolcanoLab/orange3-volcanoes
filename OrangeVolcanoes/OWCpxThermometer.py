import numpy as np
import pandas as pd
from Orange.data import Table, ContinuousVariable, Domain
from Orange.widgets.settings import Setting, ContextSetting
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from orangewidget.widget import Msg
from Thermobar import calculate_cpx_only_temp, calculate_cpx_only_press_temp, calculate_cpx_liq_temp, calculate_cpx_liq_press_temp
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
    ('T_Put2008_eq32d', 'T_Put2008_eq32d',True),
    ('T_Put2008_eq32d_subsol', 'T_Put2008_eq32d_subsol',True),
    ('T_Wang2021_eq2', 'T_Wang2021_eq2',False),
    #('T_Jorgenson2022_Cpx_only_(ML)', 'T_Jorgenson2022_Cpx_only',False),
    ('T_Jorgenson2022_Cpx_only_(ML)', 'T_Jorgenson2022_Cpx_only_onnx',False)
]

MODELS_CL = [
    ('T_Put1996_eqT1', 'T_Put1996_eqT1',False),
    ('T_Put1996_eqT2', 'T_Put1996_eqT2',True),
    ('T_Put1999', 'T_Put1999',True),
    ('T_Put2003', 'T_Put2003',True),
    ('T_Put2008_eq33', 'T_Put2008_eq33',True),
    ('T_Put2008_eq34_cpx_sat', 'T_Put2008_eq34_cpx_sat',True),
    ('T_Mas2013_eqTalk1', 'T_Mas2013_eqTalk1',False),
    ('T_Mas2013_eqTalk2', 'T_Mas2013_eqTalk2',True),
    ('T_Mas2013_eqalk33', 'T_Mas2013_eqalk33',True),
    ('T_Mas2013_Talk2012', 'T_Mas2013_Talk2012',False),
    ('T_Brug2019', 'T_Brug2019',False),
    #('T_Petrelli2020_Cpx_Liq_(ML)', 'T_Petrelli2020_Cpx_Liq',False),
    ('T_Petrelli2020_Cpx_Liq_(ML)', 'T_Petrelli2020_Cpx_Liq_onnx',False),
    ('T_Jorgenson2022_Cpx_Liq_Norm_(ML)', 'T_Jorgenson2022_Cpx_Liq_Norm',False),
    #('T_Jorgenson2022_Cpx_Liq_(ML)', 'T_Jorgenson2022_Cpx_Liq',False),
    ('T_Jorgenson2022_Cpx_Liq_(ML)', 'T_Jorgenson2022_Cpx_Liq_onnx',False)
]

MODELS_PRESSURE_CO = [
    ('P_Put2008_eq32a', 'P_Put2008_eq32a'),
    ('P_Put2008_eq32b', 'P_Put2008_eq32b')
]


MODELS_PRESSURE_CL = [
    ('P_Put1996_eqP1', 'P_Put1996_eqP1'),
    ('P_Mas2013_eqPalk1', 'P_Mas2013_eqPalk1'),
    ('P_Put1996_eqP2', 'P_Put1996_eqP2'),
    ('P_Mas2013_eqPalk2', 'P_Mas2013_eqPalk2'),
    ('P_Put2003', 'P_Put2003'),
    ('P_Put2008_eq30', 'P_Put2008_eq30'),
    ('P_Put2008_eq31', 'P_Put2008_eq31'),
    ('P_Put2008_eq32c', 'P_Put2008_eq32c'),
    ('P_Mas2013_eqalk32c', 'P_Mas2013_eqalk32c'),
    ('P_Neave2017', 'P_Neave2017')
]


class OWCpxThermometer(OWWidget):
    name = "CpxThermometer"
    description = "CpxThermometer"
    icon = "icons/CpxThermometer.png"
    priority = 5
    keywords = ['Cpx', 'Thermometer']

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        data = Output("Data", Table, dynamic=False)

    GENERIC = 0
    FROM_VAR = 0 

    model_type = ContextSetting(GENERIC)
    pressure_type = ContextSetting(GENERIC)

    resizing_enabled = False 
    want_main_area = False  


    model_idx_co = Setting(0)
    model_idx_cl = Setting(0)

    model_idx_pressure_co = Setting(0)
    model_idx_pressure_cl = Setting(0)

    pressure = Setting(True)
    pressure_model_co = Setting(False)
    pressure_model_cl = Setting(False)

    pressure_value = Setting(1)

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


        _, self.model, pressure = MODELS_CO[self.model_idx_co]
        

        #Cpx-liq GUI
        gui.appendRadioButton(box, "Cpx-liq")

        self.models_combo_cl = gui.comboBox(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button)), self, "model_idx_cl",
            items=[m[0] for m in MODELS_CL],
            callback=self._model_combo_change

        )


        self.box_1 = gui.radioButtons(
            self.controlArea, self, "pressure_type", box="Pressure",
            callback=self._radio_change_1)


        #Dataset as Pressure GUI
        self.button_1 = gui.appendRadioButton(self.box_1, "Dataset_as_Pressure_(Kbar)")   

        #Fixed Pressure GUI
        gui.appendRadioButton(self.box_1, "Fixed_Pressure")

        self.pressure_value_box = gui.spin(
            gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1)), self, "pressure_value", 
            spinType=float, minv=0,maxv=10000,step=0.1, label="Pressure_value_(bar)",
            alignment=Qt.AlignRight, callback=self._value_change,
            controlWidth=80)

        #Model as Pressure
        gui.appendRadioButton(self.box_1, "Model_as_Pressure")

        self.pressure_model_box_co = gui.comboBox(
            gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1)),  self, "model_idx_pressure_co",
            items=[m[0] for m in MODELS_PRESSURE_CO],
            callback=self._model_pressure_change)

        _, self.model_pressure = MODELS_PRESSURE_CO[self.model_idx_pressure_co]

        self.pressure_model_box_cl = gui.comboBox(
            gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1)),  self, "model_idx_pressure_cl",
            items=[m[0] for m in MODELS_PRESSURE_CL],
            callback=self._model_pressure_change)

        self.box_1.setEnabled(False)

        self.models_combo_co.setEnabled(True)
        self.models_combo_cl.setEnabled(False)

        gui.auto_apply(self.buttonsArea, self)


    def _radio_change(self):

        if self.model_type == 0:
            _, self.model, self.pressure = MODELS_CO[self.model_idx_co]
            _, self.model_pressure = MODELS_PRESSURE_CO[self.model_idx_pressure_co]
            self.models_combo_co.setEnabled(True)
            self.models_combo_cl.setEnabled(False)

        elif self.model_type == 1:
            _, self.model, self.pressure = MODELS_CL[self.model_idx_cl]
            _, self.model_pressure = MODELS_PRESSURE_CL[self.model_idx_pressure_cl]
            self.models_combo_co.setEnabled(False)
            self.models_combo_cl.setEnabled(True)


        if self.pressure_type == 1 and self.pressure == True:
            self.pressure_value_box.setEnabled(True)
        else:
            self.pressure_value_box.setEnabled(False)


        if self.pressure_type == 1 and self.pressure_model_co == True:
            self.pressure_model_box_co.setEnabled(True)
        else:
            self.pressure_model_box_co.setEnabled(False)

        if self.pressure_type == 1 and self.pressure_model_cl == True:
            self.pressure_model_box_cl.setEnabled(True)
        else:
            self.pressure_model_box_cl.setEnabled(False)


        if self.pressure == False:
            self.box_1.setEnabled(False)
            self.pressure_value_box.setEnabled(False)
            self.pressure_model_box_co.setEnabled(False)
            self.pressure_model_box_cl.setEnabled(False)
        else: 
            self.box_1.setEnabled(True)


        if self.pressure_type == 1:
            self.pressure_value_box.setEnabled(True)
        else:
            self.pressure_value_box.setEnabled(False)


        if self.pressure_type == 2:
            if self.model_type == 0:
                self.pressure_model_box_co.setEnabled(True)
                self.pressure_model_box_cl.setEnabled(False)
            elif self.model_type == 1:
                self.pressure_model_box_co.setEnabled(False)
                self.pressure_model_box_cl.setEnabled(True)

        else:
            self.pressure_model_box_co.setEnabled(False)
            self.pressure_model_box_cl.setEnabled(False)
                
                
        self.commit.deferred()    


    def _model_combo_change(self):

        if self.model_type == 0:
            _, self.model, self.pressure = MODELS_CO[self.model_idx_co]

        elif self.model_type == 1:
            _, self.model, self.pressure = MODELS_CL[self.model_idx_cl]


        if self.pressure_type == 1 and self.pressure == True:
            self.pressure_value_box.setEnabled(True)
        else:
            self.pressure_value_box.setEnabled(False)


        if self.pressure_type == 1 and self.pressure_model_co == True:
            self.pressure_model_box_co.setEnabled(True)
        else:
            self.pressure_model_box_co.setEnabled(False)

        if self.pressure_type == 1 and self.pressure_model_cl == True:
            self.pressure_model_box_cl.setEnabled(True)
        else:
            self.pressure_model_box_cl.setEnabled(False)


        if self.pressure == False:
            self.box_1.setEnabled(False)
            self.pressure_value_box.setEnabled(False)
            self.pressure_model_box_co.setEnabled(False)
            self.pressure_model_box_cl.setEnabled(False)
        else: 
            self.box_1.setEnabled(True)


        if self.pressure_type == 1:
            self.pressure_value_box.setEnabled(True)
        else:
            self.pressure_value_box.setEnabled(False)


        if self.pressure_type == 2:
            if self.model_type == 0:
                self.pressure_model_box_co.setEnabled(True)
                self.pressure_model_box_cl.setEnabled(False)
            elif self.model_type == 1:
                self.pressure_model_box_co.setEnabled(False)
                self.pressure_model_box_cl.setEnabled(True)

        else:
            self.pressure_model_box_co.setEnabled(False)
            self.pressure_model_box_cl.setEnabled(False)
                
                
        self.commit.deferred()  


    def _radio_change_1(self):

        if self.pressure_type == 1:
            self.pressure_value_box.setEnabled(True)
        else:
            self.pressure_value_box.setEnabled(False)


        if self.pressure_type == 2:
            if self.model_type == 0:
                self.pressure_model_box_co.setEnabled(True)
                self.pressure_model_box_cl.setEnabled(False)
            elif self.model_type == 1:
                self.pressure_model_box_co.setEnabled(False)
                self.pressure_model_box_cl.setEnabled(True)

        else:
            self.pressure_model_box_co.setEnabled(False)
            self.pressure_model_box_cl.setEnabled(False)
                
        self.commit.deferred()    


    def _value_change(self):

        self.commit.deferred()


    def _model_pressure_change(self):

        if self.model_type == 0:
            _, self.model_pressure = MODELS_PRESSURE_CO[self.model_idx_pressure_co]

        elif self.model_type == 1:
            _, self.model_pressure = MODELS_PRESSURE_CL[self.model_idx_pressure_cl]

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

            if self.pressure_type == 0:
                try:
                    P = df['Pressure_Kbar']
                except:
                    P = self.pressure_value
                
            elif self.pressure_type == 1:
                P = self.pressure_value

            if self.model_type == 0: 

                df = dm.preprocessing(df, my_output='cpx_only')

                if self.pressure == False:
                    temperature = calculate_cpx_only_temp(cpx_comps=df[cpx_cols],  equationT=self.model)-273.15
                else:
                    if self.pressure_type == 2:
                        temperature = calculate_cpx_only_press_temp(cpx_comps=df[cpx_cols],
                                                                       equationP=self.model_pressure,
                                                                       equationT=self.model).iloc[:,1]-273.15 
                    else:
                        temperature = calculate_cpx_only_temp(cpx_comps=df[cpx_cols], equationT=self.model, P=P)-273.15 

            elif self.model_type == 1: 

                df = dm.preprocessing(df, my_output='cpx_liq')

                if self.pressure == False:
                    temperature = calculate_cpx_liq_temp(cpx_comps=df[cpx_cols], liq_comps=df[liq_cols], equationT=self.model)-273.15
                else:
                    if  self.pressure_type == 2:
                        temperature = calculate_cpx_liq_press_temp(cpx_comps=df[cpx_cols],
                                                                      liq_comps=df[liq_cols],
                                                                      equationP=self.model_pressure,
                                                                      equationT=self.model).iloc[:,1]-273.15
                    else:
                        temperature = calculate_cpx_liq_temp(cpx_comps=df[cpx_cols], liq_comps=df[liq_cols], equationT=self.model, P=P)-273.15 



            my_domain = Domain([ContinuousVariable(name=a.name) for i, a in enumerate(self.data.domain.attributes)],
                            ContinuousVariable.make("Temperature_C_output"), metas=self.data.domain.metas)

            out = Table.from_numpy(my_domain, self.data.X,temperature, self.data.metas)


            self.Outputs.data.send(out)

import numpy as np
import pandas as pd
from Orange.data import Table, ContinuousVariable, Domain
from Orange.widgets.settings import Setting, ContextSetting
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from orangewidget.widget import Msg
from Thermobar import calculate_liq_only_temp
from OrangeVolcanoes.utils import dataManipulation as dm
from AnyQt.QtCore import Qt



liq_cols = ['SiO2_Liq', 'TiO2_Liq', 'Al2O3_Liq',
'FeOt_Liq', 'MnO_Liq', 'MgO_Liq', 'CaO_Liq', 'Na2O_Liq', 'K2O_Liq',
'Cr2O3_Liq', 'P2O5_Liq', 'H2O_Liq', 'Fe3Fet_Liq', 'NiO_Liq', 'CoO_Liq',
 'CO2_Liq']

cpx_cols = ['SiO2_Cpx', 'TiO2_Cpx', 'Al2O3_Cpx',
'FeOt_Cpx','MnO_Cpx', 'MgO_Cpx', 'CaO_Cpx', 'Na2O_Cpx', 'K2O_Cpx',
'Cr2O3_Cpx']


MODELS = [
    ('T_Put2008_eq13', 'T_Put2008_eq13',False),
    ('T_Put2008_eq14', 'T_Put2008_eq14',False),
    ('T_Put2008_eq15', 'T_Put2008_eq15',False),
    ('T_Put2008_eq16', 'T_Put2008_eq16',False),
    ('T_Helz1987_MgO', 'T_Helz1987_MgO',False),
    ('T_Shea2022_MgO', 'T_Shea2022_MgO',False),
    ('T_Montierth1995_MgO', 'T_Montierth1995_MgO',False),
    ('T_Helz1987_CaO', 'T_Helz1987_CaO',False),
    ('T_Beatt93_BeattDMg', 'T_Beatt93_BeattDMg',False),
    ('T_Beatt93_BeattDMg_HerzCorr', 'T_Beatt93_BeattDMg_HerzCorr',False),
    ('T_Sug2000_eq1', 'T_Sug2000_eq1',False),
    ('T_Sug2000_eq3_ol', 'T_Sug2000_eq3_ol',False),
    ('T_Sug2000_eq3_opx', 'T_Sug2000_eq3_opx',False),
    ('T_Sug2000_eq3_cpx', 'T_Sug2000_eq3_cpx',False),
    ('T_Sug2000_eq3_pig', 'T_Sug2000_eq3_pig',False),
    ('T_Sug2000_eq6a_H7a', 'T_Sug2000_eq6a_H7a',False),
    ('T_Sug2000_eq6b', 'T_Sug2000_eq6b',False),
    ('T_Sug2000_eq6b_H7b', 'T_Sug2000_eq6b_H7b',False),
    ('T_Put2008_eq19_BeattDMg', 'T_Put2008_eq19_BeattDMg',False),
    ('T_Put2008_eq21_BeattDMg', 'T_Put2008_eq21_BeattDMg',False),
    ('T_Put2008_eq22_BeattDMg', 'T_Put2008_eq22_BeattDMg',False),
    ('T_Molina2015_amp_sat', 'T_Molina2015_amp_sat',False),
    ('T_Put2016_eq3_amp_sat', 'T_Put2016_eq3_amp_sat',False),
    ('T_Put1999_cpx_sat', 'T_Put1999_cpx_sat',False),
    ('T_Put2008_eq34_cpx_sat', 'T_Put2008_eq34_cpx_sat',False),
    ('T_Beatt1993_opx', 'T_Beatt1993_opx',False),
    ('T_Put2005_eqD_plag_sat', 'T_Put2005_eqD_plag_sat',False),
    ('T_Put2008_eq26_plag_sat', 'T_Put2008_eq26_plag_sat',False),
    ('T_Put2008_eq24c_kspar_sat', 'T_Put2008_eq24c_kspar_sat',False),
    ('T_Put2008_eq28b_opx_sat', 'T_Put2008_eq28b_opx_sat',False)

]

class OWLiqThermometer(OWWidget):
    name = "LiqThermometer"
    description = "LiqThermometer"
    icon = "icons/LiqThermometer.png"
    priority = 6
    keywords = ['Liq', 'Thermometer']

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


    model_idx = Setting(0)

    pressure = Setting(True)

    pressure_value = Setting(1)

    auto_apply = Setting(True)



    class Error(OWWidget.Error):
        value_error = Msg("{}")



    def __init__(self):
        OWWidget.__init__(self)
        self.data = None

        box = gui.comboBox(
            self.controlArea, self, "model_idx",
            items=[m[0] for m in MODELS],
            callback=self._model_combo_change
        )


        _, self.model, pressure = MODELS[self.model_idx]
        

        self.box_1 = gui.radioButtons(
            self.controlArea, self, "pressure_type", box="Pressure",
            callback=self._radio_change_1)


        #Dataset as Pressure GUI
        self.button_1 = gui.appendRadioButton(self.box_1, "Dataset_as_Pressure_(Kbar)")   

        #Fixed Pressure GUI
        gui.appendRadioButton(self.box_1, "Fixed_Pressure")

        self.pressure_value_box = gui.spin(
            gui.indentedBox(self.box_1, gui.checkButtonOffsetHint(self.button_1)), self, "pressure_value", 
            spinType=float, minv=0,maxv=100,step=0.1, label="Pressure_value_(Kbar)",
            alignment=Qt.AlignRight, callback=self._value_change,
            controlWidth=80)

        self.pressure_value_box.setEnabled(False)

        gui.auto_apply(self.buttonsArea, self)


    

    def _model_combo_change(self):

        if self.pressure_type == 1 and self.pressure == True:
            self.pressure_value_box.setEnabled(True)
        else:
            self.pressure_value_box.setEnabled(False)

        if self.pressure == False:
            self.box_1.setEnabled(False)
            self.pressure_value_box.setEnabled(False)
        else: 
            self.box_1.setEnabled(True)


        if self.pressure_type == 1:
            self.pressure_value_box.setEnabled(True)
        else:
            self.pressure_value_box.setEnabled(False)
      
        self.commit.deferred()  


    def _radio_change_1(self):

        if self.pressure_type == 1:
            self.pressure_value_box.setEnabled(True)
        else:
            self.pressure_value_box.setEnabled(False)
                
        self.commit.deferred()    


    def _value_change(self):

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

            df_o = pd.DataFrame(data=np.array(self.data.X), columns=[a.name for i, a in enumerate(self.data.domain.attributes)])
            df = dm.preprocessing(df_o, my_output='liq_only')

            if self.pressure_type == 0:
                try:
                    P = df['P_Kbar']
                except:
                    P = self.pressure_value
                
            elif self.pressure_type == 1:
                P = self.pressure_value 

            if self.pressure == False:
                temperature = calculate_liq_only_temp(liq_comps=df[liq_cols],  equationT=self.model)-273.15
            else:
                temperature = calculate_liq_only_temp(liq_comps=df[liq_cols], equationT=self.model, P=P)-273.15 


            my_domain = Domain([ContinuousVariable(name=a.name) for i, a in enumerate(self.data.domain.attributes)],
                            ContinuousVariable.make("Temperature_C_output"), metas=self.data.domain.metas)

            out = Table.from_numpy(my_domain, self.data.X,temperature, self.data.metas)


            self.Outputs.data.send(out)

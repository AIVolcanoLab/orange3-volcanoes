import numpy as np
import pandas as pd
from Orange.data import Table, ContinuousVariable, Domain
from Orange.widgets.settings import Setting, ContextSetting, DomainContextHandler
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from orangewidget.widget import Msg
from Orange.data.pandas_compat import table_from_frame, table_to_frame
import Thermobar as pt
from AnyQt.QtCore import Qt


## This specifies the default order for each dataframe type used in calculations
liq_cols = ['SiO2_Liq', 'TiO2_Liq', 'Al2O3_Liq',
'FeOt_Liq', 'MnO_Liq', 'MgO_Liq', 'CaO_Liq', 'Na2O_Liq', 'K2O_Liq',
'Cr2O3_Liq', 'P2O5_Liq', 'H2O_Liq', 'Fe3Fet_Liq', 'NiO_Liq', 'CoO_Liq',
 'CO2_Liq']

cpx_cols = ['SiO2_Cpx', 'TiO2_Cpx', 'Al2O3_Cpx',
'FeOt_Cpx','MnO_Cpx', 'MgO_Cpx', 'CaO_Cpx', 'Na2O_Cpx', #'K2O_Cpx',
'Cr2O3_Cpx']


FILTERS_ET = [
    ('Kd_Put2008', 'Delta_Kd_Put2008'),
    ('Kd_Mas2013', 'Delta_Kd_Mas2013'),
    ('EnFs_Mollo13', 'Delta_EnFs_Mollo13'),
    ('EnFs_I_M_Mollo13', 'Delta_EnFs_I_M_Mollo13'),
    ('EnFs_Put1999', 'Delta_EnFs_Put1999'),
    ('DiHd_Mollo13', 'Delta_DiHd_Mollo13'),
    ('DiHd_Put1999', 'Delta_DiHd_Put1999')
]


class OWDataCleaning(OWWidget):
    name = "DataCleaning"
    description = "DataCleaning"
    icon = "icons/DataCleaning.png"
    priority = 2
    keywords = ['DataCleaning', 'Oxides', 'Equilibrium', 'Test', 'Cations']


    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        data = Output("Data", Table, dynamic=False)

    GENERIC, FROM_VAR = range(2)

    resizing_enabled = False
    want_main_area = False

    DEFAULT_PREFIX = "Feature"

    filter_idx_et = Setting(0)

    temperature = Setting(1000)
    pressure = Setting(1)
    threshold_tot = Setting(40)
    threshold_cat = Setting(40)
    threshold_et = Setting(40)
    

    settingsHandler = DomainContextHandler()

    filter_type = ContextSetting(GENERIC)
    data_type = ContextSetting(GENERIC)
    auto_apply = Setting(True)


    class Error(OWWidget.Error):
        value_error = Msg("{}")


    def __init__(self):
        OWWidget.__init__(self)
        self.data = None

        box = gui.radioButtons(
            self.controlArea, self, "filter_type", box="Filtering",
            callback=self._radio_change)

        #Cations Filter GUI
        button_0 = gui.appendRadioButton(box, "Oxides-Totals")

        self.threshold_value_box_tot = gui.spin(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button_0)), self, "threshold_tot", 1, 100, label="100 ± Delta",
            alignment=Qt.AlignRight, callback=self._value_change,
            controlWidth=80)

        button_1 = gui.appendRadioButton(box, "Cations-Filter")

        self.threshold_value_box_cat = gui.spin(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button_1)), self, "threshold_cat", spinType=float, minv=0,maxv=4,step=0.001, label="4 ± Delta",
            alignment=Qt.AlignRight, callback=self._value_change,
            controlWidth=80)
       
        button_2 = gui.appendRadioButton(box, "Equilibrium-Test")

        self.filter_combo_et = gui.comboBox(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button_2)), self, "filter_idx_et",
            items=[m[0] for m in FILTERS_ET],
            callback=self._filter_et_change
        )

        _, self.filter_et = FILTERS_ET[self.filter_idx_et]

        self.threshold_value_box_et = gui.spin(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button_2)), self, "threshold_et", spinType=float, minv=0,maxv=10,step=0.001, label="0 ± Delta",
            alignment=Qt.AlignRight, callback=self._value_change,
            controlWidth=80)

        self.temperature_value_box = gui.spin(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button_2)), self, "temperature", 0, 10000, label="Temperature (C)",
            alignment=Qt.AlignRight, callback=self._value_change,
            controlWidth=80)

        self.pressure_value_box = gui.spin(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button_2)), self, "pressure", spinType=float, minv=0,maxv=10000,step=0.1, label="Pressure (Kbar)",
            alignment=Qt.AlignRight, callback=self._value_change,
            controlWidth=80)

        self.threshold_value_box_tot.setEnabled(True)
        self.threshold_value_box_cat.setEnabled(False)
        self.filter_combo_et.setEnabled(False)
        self.threshold_value_box_et.setEnabled(False)
        self.temperature_value_box.setEnabled(False)
        self.pressure_value_box.setEnabled(False)

        gui.auto_apply(self.buttonsArea, self)


    def _radio_change(self):

        if self.filter_type == 0:
            self.threshold_value_box_tot.setEnabled(True)
            self.threshold_value_box_cat.setEnabled(False)
            self.filter_combo_et.setEnabled(False)
            self.threshold_value_box_et.setEnabled(False)
            self.temperature_value_box.setEnabled(False)
            self.pressure_value_box.setEnabled(False)

        elif self.filter_type == 1:
            self.threshold_value_box_tot.setEnabled(False)
            self.threshold_value_box_cat.setEnabled(True)
            self.filter_combo_et.setEnabled(False)
            self.threshold_value_box_et.setEnabled(False)
            self.temperature_value_box.setEnabled(False)
            self.pressure_value_box.setEnabled(False)

        elif self.filter_type == 2:
            self.threshold_value_box_tot.setEnabled(False)
            self.threshold_value_box_cat.setEnabled(False)
            self.filter_combo_et.setEnabled(True)
            self.threshold_value_box_et.setEnabled(True)
            self.temperature_value_box.setEnabled(True)
            self.pressure_value_box.setEnabled(True)

        self.commit.deferred()



    def _filter_et_change(self):

        _, self.filter_et = FILTERS_ET[self.filter_idx_et]
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

            df = table_to_frame(self.data)

            if self.filter_type == 0:
                df_temp = df.copy()
                df_temp['sum'] = df_temp[cpx_cols].sum(axis=1)
                out = df_temp[(df_temp['sum']-100).abs()<=self.threshold_tot].drop(['sum'],axis=1)

            elif self.filter_type == 1:
                df_temp = df.copy()
                df_temp['cations'] = pt.calculate_clinopyroxene_components(df_temp)['Cation_Sum_Cpx']
                #out = df_temp[df_temp['cations']>=self.threshold_cat].drop(['cations'],axis=1)
                out = df_temp[(df_temp['cations']-4).abs()<=self.threshold_cat].drop(['cations'],axis=1)

            elif self.filter_type == 2:

                if set(table_to_frame(self.data).columns) <= set(cpx_cols+liq_cols):
                    self.Error.value_error("Data Input uncorrect")
                else:
                    self.Error.value_error.clear()
                    return

                df_temp = df.copy()
                df_temp[self.filter_et] = pt.calculate_cpx_liq_eq_tests(meltmatch=None, liq_comps=df_temp[liq_cols],
                                                              cpx_comps=df_temp[cpx_cols],Fe3Fet_Liq=None,
                                                              P=self.pressure, T=self.temperature, sigma=1, Kd_Err=0.03)[self.filter_et] 
                out = df_temp[df_temp[self.filter_et].abs()<=self.threshold_et].drop([self.filter_et],axis=1)

            out = table_from_frame(out)

            self.Outputs.data.send(out)
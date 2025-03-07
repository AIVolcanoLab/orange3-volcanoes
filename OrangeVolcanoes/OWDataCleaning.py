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
from OrangeVolcanoes.utils import dataManipulation as dm


## This specifies the default order for each dataframe type used in calculations
liq_cols = ['SiO2_Liq', 'TiO2_Liq', 'Al2O3_Liq',
'FeOt_Liq', 'MnO_Liq', 'MgO_Liq', 'CaO_Liq', 'Na2O_Liq', 'K2O_Liq',
'Cr2O3_Liq', 'P2O5_Liq', 'H2O_Liq', 'Fe3Fet_Liq', 'NiO_Liq', 'CoO_Liq',
 'CO2_Liq']

cpx_cols = ['SiO2_Cpx', 'TiO2_Cpx', 'Al2O3_Cpx',
'FeOt_Cpx','MnO_Cpx', 'MgO_Cpx', 'CaO_Cpx', 'Na2O_Cpx', 'K2O_Cpx',
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
    name = "Data Cleaning"
    description = "This widget allows the user to filter the input data according to: (i) the total oxide weight content in percentage; (ii) the cations per unit formula and (iii) the equilibrium between clinopyroxene and liquid."
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
    pressure_flag = False
    temperature_flag = False
    

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
            self.controlArea, self, "filter_type", box="Cpx Filtering",
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
       
        button_2 = gui.appendRadioButton(box, "Cpx-Liq Equilibrium-Test")

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
            gui.indentedBox(box, gui.checkButtonOffsetHint(button_2)), self, "temperature", 0, 10000, label="Temperature (K)",
            alignment=Qt.AlignRight, callback=self._value_change,
            controlWidth=80)
        
        self.temperature_check = gui.checkBox(
            gui.indentedBox(box),self, "temperature_flag", label="Use Dataset as Temperature (K)", callback=self._flag_dataset_temperature_change)


        self.pressure_value_box = gui.spin(
            gui.indentedBox(box, gui.checkButtonOffsetHint(button_2)), self, "pressure", spinType=float, minv=0,maxv=10000,step=0.1, label="Pressure (Kbar)",
            alignment=Qt.AlignRight, callback=self._value_change,
            controlWidth=80)
        
        self.pressure_check = gui.checkBox(
            gui.indentedBox(box),self, "pressure_flag", label="Use Dataset as Pressure (Kbar)", callback=self._flag_dataset_pressure_change)

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
            self.pressure_check.setEnabled(False)
            self.temperature_check.setEnabled(False)

        elif self.filter_type == 1:
            self.threshold_value_box_tot.setEnabled(False)
            self.threshold_value_box_cat.setEnabled(True)
            self.filter_combo_et.setEnabled(False)
            self.threshold_value_box_et.setEnabled(False)
            self.temperature_value_box.setEnabled(False)
            self.pressure_value_box.setEnabled(False)
            self.pressure_check.setEnabled(False)
            self.temperature_check.setEnabled(False)

        elif self.filter_type == 2:
            self.threshold_value_box_tot.setEnabled(False)
            self.threshold_value_box_cat.setEnabled(False)
            self.filter_combo_et.setEnabled(True)
            self.threshold_value_box_et.setEnabled(True)
            self.temperature_value_box.setEnabled(True)
            self.pressure_value_box.setEnabled(True)
            self.pressure_check.setEnabled(True)
            self.temperature_check.setEnabled(True)

        self.commit.deferred()



    def _filter_et_change(self):

        _, self.filter_et = FILTERS_ET[self.filter_idx_et]
        self.commit.deferred()



    def _value_change(self):

        self.commit.deferred()


    def _flag_dataset_pressure_change(self):

        if self.pressure_flag == True:
            self.pressure_value_box.setEnabled(False)
        else:
            self.pressure_value_box.setEnabled(True)

        self.commit.deferred()

    def _flag_dataset_temperature_change(self):

        if self.temperature_flag == True:
            self.temperature_value_box.setEnabled(False)
        else:
            self.temperature_value_box.setEnabled(True)
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
            mask = np.ones(len(df), dtype=bool)  # Inizializza la maschera come True per tutte le righe

            if self.filter_type == 0:
                df_temp = dm.preprocessing(df.copy(), my_output='cpx_only')
                df_temp['sum'] = df_temp[cpx_cols].sum(axis=1)
                mask &= (df_temp['sum']-100).abs() <= self.threshold_tot

            elif self.filter_type == 1:
                df_temp = dm.preprocessing(df.copy(), my_output='cpx_only')

                if set(df_temp.columns) <= set(cpx_cols):
                    self.Error.value_error("Data Input uncorrect")
                    return
                else:
                    self.Error.value_error.clear()
                    
                df_temp['cations'] = pt.calculate_clinopyroxene_components(df_temp)['Cation_Sum_Cpx']
                mask &= (df_temp['cations']-4).abs() <= self.threshold_cat

            elif self.filter_type == 2:
                df_temp = dm.preprocessing(df.copy(), my_output='cpx_liq')

                if set(df_temp.columns) <= set(cpx_cols + liq_cols):
                    self.Error.value_error("Data Input uncorrect")
                    return
                else:
                    self.Error.value_error.clear()

                temp_T = df_temp['T_K'] if 'T_K' in df_temp else self.temperature
                temp_P = df_temp['P_kbar'] if 'P_kbar' in df_temp else self.pressure

                df_temp[self.filter_et] = pt.calculate_cpx_liq_eq_tests(
                    meltmatch=None, liq_comps=df_temp[liq_cols],
                    cpx_comps=df_temp[cpx_cols], Fe3Fet_Liq=None,
                    P=temp_P, T=temp_T, sigma=1, Kd_Err=0.03)[self.filter_et]
                mask &= df_temp[self.filter_et].abs() <= self.threshold_et

        
            df_final = df[mask]

            attribute_names = self.data.domain.attributes
            metas = [a for a in self.data.domain.metas]
            class_vars = [a for a in self.data.domain.class_vars]

            column_names = [var.name for var in attribute_names]

            new_domain = Domain(attributes=attribute_names, class_vars=class_vars, metas=metas)
            
            new_table = Table.from_numpy(domain=new_domain, X=df_final[column_names].values, Y=self.data.Y[mask], metas=self.data.metas[mask])

            self.Outputs.data.send(new_table)

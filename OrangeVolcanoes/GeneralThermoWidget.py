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
    calculate_amp_liq_press, calculate_amp_liq_press_temp,
    calculate_liq_only_temp, calculate_ol_liq_temp,
    calculate_ol_sp_temp, calculate_plag_kspar_temp,
    calculate_fspar_liq_temp, calculate_fspar_liq_press,
    calculate_fspar_liq_press_temp,
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

ol_cols = ['SiO2_Ol', 'TiO2_Ol', 'Al2O3_Ol',
'FeOt_Ol', 'MnO_Ol', 'MgO_Ol', 'CaO_Ol', 'Na2O_Ol', 'K2O_Ol', 'Cr2O3_Ol',
'NiO_Ol']

sp_cols=['SiO2_Sp', 'TiO2_Sp', 'Al2O3_Sp',
'FeOt_Sp', 'MnO_Sp', 'MgO_Sp', 'CaO_Sp', 'Na2O_Sp', 'K2O_Sp', 'Cr2O3_Sp',
'NiO_Sp']

amp_cols = ['SiO2_Amp', 'TiO2_Amp', 'Al2O3_Amp',
 'FeOt_Amp', 'MnO_Amp', 'MgO_Amp', 'CaO_Amp', 'Na2O_Amp', 'K2O_Amp',
 'Cr2O3_Amp', 'F_Amp', 'Cl_Amp']

plag_cols=['SiO2_Plag', 'TiO2_Plag', 'Al2O3_Plag',
'FeOt_Plag', 'MnO_Plag', 'MgO_Plag', 'CaO_Plag', 'Na2O_Plag', 'K2O_Plag',
'Cr2O3_Plag']

kspar_cols=['SiO2_Kspar', 'TiO2_Kspar',
 'Al2O3_Kspar', 'FeOt_Kspar','MnO_Kspar', 'MgO_Kspar', 'CaO_Kspar',
 'Na2O_Kspar', 'K2O_Kspar', 'Cr2O3_Kspar']

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
## Extend Cpx models
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

## Liquid and olivine models
MODELS_LIQ_ONLY_TEMPERATURE = [
    ('T_Put2008_eq13', 'T_Put2008_eq13',False,False),
    ('T_Put2008_eq14', 'T_Put2008_eq14',False,True),
    ('T_Put2008_eq15', 'T_Put2008_eq15',True,True),
    ('T_Put2008_eq16', 'T_Put2008_eq16',True,False),
    ('T_Helz1987_MgO', 'T_Helz1987_MgO',False,False),
    ('T_Shea2022_MgO', 'T_Shea2022_MgO',False,False),
    ('T_Montierth1995_MgO', 'T_Montierth1995_MgO',False,False),
    ('T_Helz1987_CaO', 'T_Helz1987_CaO',False,False),
    #('T_Beatt93_BeattDMg', 'T_Beatt93_BeattDMg',False,False),
    ('T_Beatt93_BeattDMg_HerzCorr', 'T_Beatt93_BeattDMg_HerzCorr',True,False),
    ('T_Sug2000_eq1', 'T_Sug2000_eq1',False,False),
    ('T_Sug2000_eq3_ol', 'T_Sug2000_eq3_ol',True,False),
    ('T_Sug2000_eq3_opx', 'T_Sug2000_eq3_opx',True,False),
    ('T_Sug2000_eq3_cpx', 'T_Sug2000_eq3_cpx',True,False),
    ('T_Sug2000_eq3_pig', 'T_Sug2000_eq3_pig',True,False),
    ('T_Sug2000_eq6a_H7a', 'T_Sug2000_eq6a_H7a',True,True),
    ('T_Sug2000_eq6b', 'T_Sug2000_eq6b',True,False),
    ('T_Sug2000_eq6b_H7b', 'T_Sug2000_eq6b_H7b',True,True),
    ('T_Put2008_eq19_BeattDMg', 'T_Put2008_eq19_BeattDMg',True,False),
    ('T_Put2008_eq21_BeattDMg', 'T_Put2008_eq21_BeattDMg',True,True),
    ('T_Put2008_eq22_BeattDMg', 'T_Put2008_eq22_BeattDMg',True,True),
    ('T_Molina2015_amp_sat', 'T_Molina2015_amp_sat',False,False),
    ('T_Put2016_eq3_amp_sat', 'T_Put2016_eq3_amp_sat',False,False),
    ('T_Put1999_cpx_sat', 'T_Put1999_cpx_sat',True,False),
    ('T_Put2008_eq34_cpx_sat', 'T_Put2008_eq34_cpx_sat',True,True),
    ('T_Beatt1993_opx', 'T_Beatt1993_opx',True,False),
    ('T_Put2005_eqD_plag_sat', 'T_Put2005_eqD_plag_sat',True,True),
    ('T_Put2008_eq26_plag_sat', 'T_Put2008_eq26_plag_sat',True,True),
    ('T_Put2008_eq24c_kspar_sat', 'T_Put2008_eq24c_kspar_sat',True,True)#,
    #('T_Put2008_eq28b_opx_sat', 'T_Put2008_eq28b_opx_sat',True,True)

]

MODELS_LIQ_OL_TEMPERATURE = [
('T_Beatt93_ol', 'T_Beatt93_ol', True, False),
('T_Beatt93_ol_HerzCorr', 'T_Beatt93_ol_HerzCorr', True, False),
('T_Put2008_eq19', 'T_Put2008_eq19', True, False),
('T_Put2008_eq21', 'T_Put2008_eq21', True, True),
('T_Put2008_eq22', 'T_Put2008_eq22', True, True),
('T_Sisson1992', 'T_Sisson1992', True, False),
('T_Pu2017', 'T_Pu2017', False, False),
('T_Pu2017_Mg', 'T_Pu2017_Mg', False, False),
('T_Pu2021', 'T_Pu2021', True, False)
]

MODELS_LIQ_ONLY_PRESSURE = [
    ('None_available', 'None_available', True, True),
]

MODELS_LIQ_OL_PRESSURE = [
    ('None_available', 'None_available', True, True),
]
## Two feldspar-Plag models
MODELS_PLAG_KSPAR_TEMP = [
    ('T_Put2008_eq27a', 'T_Put2008_eq27a', True, False),
    ('T_Put2008_eq27b', 'T_Put2008_eq27b', True, False),
    ('T_Put_Global_2Fspar', 'T_Put_Global_2Fspar', True, False),

]

MODELS_PLAG_KSPAR_PRESSURE = [
    ('None_available', 'None_available', True, False),
]

## Plag-Liq
MODELS_PLAG_ONLY_PRESSURE = [
    ('None_available', 'None_available', False, False),
]

MODELS_PLAG_LIQ_PRESSURE = [
    ('P_Put2008_eq25', 'P_Put2008_eq25', True, False),
]

MODELS_PLAG_ONLY_TEMPERATURE = [
    ('None_available', 'None_available', False, False),
]

MODELS_PLAG_LIQ_TEMPERATURE = [
    ('T_Put2008_eq23', 'T_Put2008_eq23', True, True),
    ('T_Put2008_eq24a', 'T_Put2008_eq24a', True, True),

]


## Kspar-Liq
MODELS_KSPAR_ONLY_PRESSURE = [
    ('None_available', 'None_available', False, False),
]

MODELS_KSPAR_LIQ_PRESSURE = [
    ('None_available', 'None_available', False, False),
]

MODELS_KSPAR_ONLY_TEMPERATURE = [
    ('None_available', 'None_available', False, False),
]

MODELS_KSPAR_LIQ_TEMPERATURE = [
    ('T_Put2008_eq24b', 'T_Put2008_eq24b', True,False),


]

## Olivine_Spinel
MODELS_OL_SP_TEMP = [
    ('T_Coogan2014', 'T_Coogan2014', False, False),
    ('T_Wan2008', 'T_Wan2008', False, False),


]

MODELS_OL_SP_PRESSURE = [
    ('None_available', 'None_available', True, False),
]

## Actual class calling Thermobar
class OWThermobar(OWWidget):
    name = "Thermobar Calculations"
    description = "Perform various thermobarometric calculations on mineral data."
    icon = "icons/thermobar.png"
    priority = 5
    keywords = ['Thermobar', 'Cpx', 'Opx', 'Amp', 'Liquid', 'Plag', 'Kspar', 'Spinel', 'Temperature', 'Pressure']

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



    # liq-Liq Thermometry settings
    liq_thermometry_mode = ContextSetting(0)  # 0=Cpx-Liq, 1=Cpx-only
    liq_ol_temp_model_idx = ContextSetting(0)
    liq_ol_temp_pressure_type = ContextSetting(0)
    liq_ol_temp_pressure_value = ContextSetting(1.0)
    liq_ol_temp_barometer_choice = ContextSetting(1)  # 0=liq-only, 1=liq-Liq
    liq_ol_temp_barometer_model_idx_lon = ContextSetting(0)
    liq_ol_temp_barometer_model_idx_lo = ContextSetting(0)
    liq_ol_temp_fixed_h2o = ContextSetting(False)
    liq_ol_temp_fixed_h2o_value_str = ContextSetting("1.0")

    # liq-Liq Barometry settings
    liq_barometry_mode = ContextSetting(0)  # 0=liq-Liq, 1=liq-only
    liq_ol_press_model_idx = ContextSetting(0)
    liq_ol_press_temp_type = ContextSetting(0)
    liq_ol_press_temp_value = ContextSetting(900.0)
    liq_ol_press_thermometer_choice = ContextSetting(1)  # 0=liq-only, 1=liq-Liq
    liq_ol_press_thermometer_model_idx_lon = ContextSetting(0)
    liq_ol_press_thermometer_model_idx_lo = ContextSetting(0)
    liq_ol_press_fixed_h2o = ContextSetting(False)
    liq_ol_press_fixed_h2o_value_str = ContextSetting("1.0")

    # Plag-Kspar Thermometry settings
    plag_kspar_temp_model_idx = ContextSetting(0)
    plag_kspar_temp_pressure_type = ContextSetting(0)
    plag_kspar_temp_pressure_value = ContextSetting(1.0)
    plag_kspar_temp_barometer_model_idx = ContextSetting(0)
    plag_kspar_temp_fixed_h2o = ContextSetting(False)
    plag_kspar_temp_fixed_h2o_value_str = ContextSetting("1.0")

    # Plag-Kspar Barometry settings
    plag_kspar_press_model_idx = ContextSetting(0)
    plag_kspar_press_temp_type = ContextSetting(0)
    plag_kspar_press_temp_value = ContextSetting(900.0)
    plag_kspar_press_thermometer_model_idx = ContextSetting(0)
    plag_kspar_press_fixed_h2o = ContextSetting(False)
    plag_kspar_press_fixed_h2o_value_str = ContextSetting("1.0")

    # plag-Liq Thermometry settings
    plag_thermometry_mode = ContextSetting(0)  # 0=Plag-Liq, 1=Plag-only
    plag_liq_temp_model_idx = ContextSetting(0)
    plag_liq_temp_pressure_type = ContextSetting(0)
    plag_liq_temp_pressure_value = ContextSetting(1.0)
    plag_liq_temp_barometer_choice = ContextSetting(1)  # 0=plag-only, 1=plag-Liq
    plag_liq_temp_barometer_model_idx_co = ContextSetting(0)
    plag_liq_temp_barometer_model_idx_cl = ContextSetting(0)
    plag_liq_temp_fixed_h2o = ContextSetting(False)
    plag_liq_temp_fixed_h2o_value_str = ContextSetting("1.0")

    # plag-Liq Barometry settings
    plag_barometry_mode = ContextSetting(0)  # 0=plag-Liq, 1=plag-only
    plag_liq_press_model_idx = ContextSetting(0)
    plag_liq_press_temp_type = ContextSetting(0)
    plag_liq_press_temp_value = ContextSetting(900.0)
    plag_liq_press_thermometer_choice = ContextSetting(1)  # 0=plag-only, 1=plag-Liq
    plag_liq_press_thermometer_model_idx_co = ContextSetting(0)
    plag_liq_press_thermometer_model_idx_cl = ContextSetting(0)
    plag_liq_press_fixed_h2o = ContextSetting(False)
    plag_liq_press_fixed_h2o_value_str = ContextSetting("1.0")

    # kspar-Liq Thermometry settings
    kspar_thermometry_mode = ContextSetting(0)  # 0=Kspar-Liq, 1=Kspar-only
    kspar_liq_temp_model_idx = ContextSetting(0)
    kspar_liq_temp_pressure_type = ContextSetting(0)
    kspar_liq_temp_pressure_value = ContextSetting(1.0)
    kspar_liq_temp_barometer_choice = ContextSetting(1)  # 0=kspar-only, 1=kspar-Liq
    kspar_liq_temp_barometer_model_idx_co = ContextSetting(0)
    kspar_liq_temp_barometer_model_idx_cl = ContextSetting(0)
    kspar_liq_temp_fixed_h2o = ContextSetting(False)
    kspar_liq_temp_fixed_h2o_value_str = ContextSetting("1.0")

    # kspar-Liq Barometry settings
    kspar_barometry_mode = ContextSetting(0)  # 0=kspar-Liq, 1=kspar-only
    kspar_liq_press_model_idx = ContextSetting(0)
    kspar_liq_press_temp_type = ContextSetting(0)
    kspar_liq_press_temp_value = ContextSetting(900.0)
    kspar_liq_press_thermometer_choice = ContextSetting(1)  # 0=kspar-only, 1=kspar-Liq
    kspar_liq_press_thermometer_model_idx_co = ContextSetting(0)
    kspar_liq_press_thermometer_model_idx_cl = ContextSetting(0)
    kspar_liq_press_fixed_h2o = ContextSetting(False)
    kspar_liq_press_fixed_h2o_value_str = ContextSetting("1.0")

    # Ol-Sp Thermometry settings
    ol_sp_temp_model_idx = ContextSetting(0)
    ol_sp_temp_pressure_type = ContextSetting(0)
    ol_sp_temp_pressure_value = ContextSetting(1.0)
    ol_sp_temp_barometer_model_idx = ContextSetting(0)
    ol_sp_temp_fixed_h2o = ContextSetting(False)
    ol_sp_temp_fixed_h2o_value_str = ContextSetting("1.0")

    # Ol-Sp Barometry settings
    ol_sp_press_model_idx = ContextSetting(0)
    ol_sp_press_temp_type = ContextSetting(0)
    ol_sp_press_temp_value = ContextSetting(900.0)
    ol_sp_press_thermometer_model_idx = ContextSetting(0)
    ol_sp_press_fixed_h2o = ContextSetting(False)
    ol_sp_press_fixed_h2o_value_str = ContextSetting("1.0")




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
                "Cpx-Opx Thermometry", #1
                "Cpx-Opx Barometry", #2
                "Opx±Liq Thermometry", #3
                "Opx±Liq Barometry", #4
                "Amp±Liq Thermometry", #5
                "Amp±Liq Barometry", #6
                "Cpx±Liq Thermometry", #7
                "Cpx±Liq Barometry", #8
                "Liq±Ol Thermometry", #9
                "Plag-Kspar Thermometry",#10
                "Plag-Liq Thermometry", # 11
                "Plag-Liq Barometry", # 12,
                'Kspar-Liq Thermometry', #13
                'Ol-Spinel Thermometry' ,#14
                #"Liq±Ol Barometry", #10
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

        self.opx_liq_temp_box = gui.vBox(self.controlArea, "Opx±Liq Thermometry Settings")
        self._build_opx_liq_temp_gui(self.opx_liq_temp_box)
        self.opx_liq_temp_box.setVisible(False)

        self.opx_liq_press_box = gui.vBox(self.controlArea, "Opx±Liq Barometry Settings")
        self._build_opx_liq_press_gui(self.opx_liq_press_box)
        self.opx_liq_press_box.setVisible(False)

        self.amp_liq_temp_box = gui.vBox(self.controlArea, "Opx±Liq Thermometry Settings")
        self._build_amp_liq_temp_gui(self.amp_liq_temp_box)
        self.amp_liq_temp_box.setVisible(False)

        self.amp_liq_press_box = gui.vBox(self.controlArea, "Amp±Liq Barometry Settings")
        self._build_amp_liq_press_gui(self.amp_liq_press_box)
        self.amp_liq_press_box.setVisible(False)


        self.cpx_liq_temp_box = gui.vBox(self.controlArea, "Cpx±Liq Thermometry Settings")
        self._build_cpx_liq_temp_gui(self.cpx_liq_temp_box)
        self.cpx_liq_temp_box.setVisible(False)

        self.cpx_liq_press_box = gui.vBox(self.controlArea, "Cpx±Liq Barometry Settings")
        self._build_cpx_liq_press_gui(self.cpx_liq_press_box)
        self.cpx_liq_press_box.setVisible(False)

        self.liq_ol_temp_box = gui.vBox(self.controlArea, "Liq±Ol Thermometry Settings")
        self._build_liq_ol_temp_gui(self.liq_ol_temp_box)
        self.liq_ol_temp_box.setVisible(False)

        self.liq_ol_press_box = gui.vBox(self.controlArea, "Liq±Ol Barometry Settings")
        self._build_liq_ol_press_gui(self.liq_ol_press_box)
        self.liq_ol_press_box.setVisible(False)


        self.plag_kspar_temp_box = gui.vBox(self.controlArea, "Plag-Kspar Thermometry Settings")
        self._build_plag_kspar_temp_gui(self.plag_kspar_temp_box)
        self.plag_kspar_temp_box.setVisible(False)

        self.plag_kspar_press_box = gui.vBox(self.controlArea, "Plag-Kspar Barometry Settings")
        self._build_plag_kspar_press_gui(self.plag_kspar_press_box)
        self.plag_kspar_press_box.setVisible(False)

        self.plag_liq_temp_box = gui.vBox(self.controlArea, "Plag±Liq Thermometry Settings")
        self._build_plag_liq_temp_gui(self.plag_liq_temp_box)
        self.plag_liq_temp_box.setVisible(False)

        self.plag_liq_press_box = gui.vBox(self.controlArea, "Plag±Liq Barometry Settings")
        self._build_plag_liq_press_gui(self.plag_liq_press_box)
        self.plag_liq_press_box.setVisible(False)

        self.kspar_liq_temp_box = gui.vBox(self.controlArea, "Kspar±Liq Thermometry Settings")
        self._build_kspar_liq_temp_gui(self.kspar_liq_temp_box)
        self.kspar_liq_temp_box.setVisible(False)

        self.kspar_liq_press_box = gui.vBox(self.controlArea, "Kspar±Liq Barometry Settings")
        self._build_kspar_liq_press_gui(self.kspar_liq_press_box)
        self.kspar_liq_press_box.setVisible(False)

        self.ol_sp_temp_box = gui.vBox(self.controlArea, "Ol-Sp Thermometry Settings")
        self._build_ol_sp_temp_gui(self.ol_sp_temp_box)
        self.ol_sp_temp_box.setVisible(False)

        self.ol_sp_press_box = gui.vBox(self.controlArea, "Ol-Sp Barometry Settings")
        self._build_ol_sp_press_gui(self.ol_sp_press_box)
        self.ol_sp_press_box.setVisible(False)





        gui.auto_apply(self.buttonsArea, self)
        self._update_controls()
## Liq only and Ol-Liq stuff
    ## Liq-only and Liq-Ol stuff

    def _build_liq_ol_temp_gui(self, parent_box):
        """Build GUI for Liq Thermometry"""
        # Mode selection
        mode_box = gui.hBox(parent_box)
        gui.label(mode_box, self, "Thermometry Mode:")
        self.liq_thermometry_mode_buttons = gui.radioButtons(
            mode_box, self, "liq_thermometry_mode",
            callback=self._update_controls)
        gui.appendRadioButton(self.liq_thermometry_mode_buttons, "Liq-Ol")
        gui.appendRadioButton(self.liq_thermometry_mode_buttons, "Liq-only")

        # Models selection
        temp_model_box = gui.vBox(parent_box, "Models")
        self.liq_ol_temp_models_combo = gui.comboBox(
            temp_model_box, self, "liq_ol_temp_model_idx",
            items=[],  # Populated later
            callback=self._update_controls)

        # Pressure settings
        self.liq_ol_temp_pressure_box = gui.radioButtons(
            parent_box, self, "liq_ol_temp_pressure_type", box="Pressure Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.liq_ol_temp_pressure_box, "Dataset as Pressure (kbar)")

        rb_fixed_p = gui.appendRadioButton(self.liq_ol_temp_pressure_box, "Fixed Pressure")


        self.liq_ol_temp_pressure_value_box = gui.doubleSpin(
            gui.indentedBox(self.liq_ol_temp_pressure_box, gui.checkButtonOffsetHint(rb_fixed_p)), self,
            "liq_ol_temp_pressure_value", 0, 1000, step=1.0, label="Pressure Value (kbar)",
            alignment=Qt.AlignRight, callback=self.commit.deferred, controlWidth=80, decimals=0)

        rb_model_p = gui.appendRadioButton(self.liq_ol_temp_pressure_box, "Model as Pressure")
        model_as_p_box = gui.indentedBox(self.liq_ol_temp_pressure_box, gui.checkButtonOffsetHint(rb_model_p))

        self.liq_ol_temp_barometer_choice_buttons = gui.radioButtons(
            model_as_p_box, self, "liq_ol_temp_barometer_choice",
            callback=self._update_controls)

        rb_co = gui.appendRadioButton(self.liq_ol_temp_barometer_choice_buttons, "Use Liq-only barometer")
        self.liq_ol_temp_barometer_model_box_co = gui.comboBox(
            gui.indentedBox(self.liq_ol_temp_barometer_choice_buttons, gui.checkButtonOffsetHint(rb_co)),
            self, "liq_ol_temp_barometer_model_idx_lon",
            items=[m[0] for m in MODELS_LIQ_ONLY_PRESSURE],
            callback=self._update_controls)

        rb_cl = gui.appendRadioButton(self.liq_ol_temp_barometer_choice_buttons, "Use Liq-Ol barometer")
        self.liq_ol_temp_barometer_model_box_cl = gui.comboBox(
            gui.indentedBox(self.liq_ol_temp_barometer_choice_buttons, gui.checkButtonOffsetHint(rb_cl)),
            self, "liq_ol_temp_barometer_model_idx_lo",
            items=[m[0] for m in MODELS_LIQ_OL_PRESSURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.liq_ol_temp_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "liq_ol_temp_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.liq_ol_temp_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "liq_ol_temp_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _build_liq_ol_press_gui(self, parent_box):
        """Build GUI for Liq Barometry"""
        # Mode selection
        mode_box = gui.hBox(parent_box)
        gui.label(mode_box, self, "Barometry Mode:")
        self.liq_barometry_mode_buttons = gui.radioButtons(
            mode_box, self, "liq_barometry_mode",
            callback=self._update_controls)
        gui.appendRadioButton(self.liq_barometry_mode_buttons, "Liq-Ol")
        gui.appendRadioButton(self.liq_barometry_mode_buttons, "Liq-only")

        # Models selection
        press_model_box = gui.vBox(parent_box, "Models")
        self.liq_ol_press_models_combo = gui.comboBox(
            press_model_box, self, "liq_ol_press_model_idx",
            items=[],  # Populated later
            callback=self._update_controls)

        # Temperature settings
        self.liq_ol_press_temp_box = gui.radioButtons(
            parent_box, self, "liq_ol_press_temp_type", box="Temperature Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.liq_ol_press_temp_box, "Dataset as Temperature (K)")

        rb_fixed_t = gui.appendRadioButton(self.liq_ol_press_temp_box, "Fixed Temperature")
        self.liq_ol_press_temp_value_box = gui.doubleSpin(
            gui.indentedBox(self.liq_ol_press_temp_box, gui.checkButtonOffsetHint(rb_fixed_t)), self,
            "liq_ol_press_temp_value", 500.0, 2000.0, step=1.0, label="Temperature Value (K)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=0)

        rb_model_t = gui.appendRadioButton(self.liq_ol_press_temp_box, "Model as Temperature")
        model_as_t_box = gui.indentedBox(self.liq_ol_press_temp_box, gui.checkButtonOffsetHint(rb_model_t))

        self.liq_ol_press_thermometer_choice_buttons = gui.radioButtons(
            model_as_t_box, self, "liq_ol_press_thermometer_choice",
            callback=self._update_controls)

        rb_co = gui.appendRadioButton(self.liq_ol_press_thermometer_choice_buttons, "Use Liq-only thermometer")
        self.liq_ol_press_thermometer_model_box_co = gui.comboBox(
            gui.indentedBox(self.liq_ol_press_thermometer_choice_buttons, gui.checkButtonOffsetHint(rb_co)),
            self, "liq_ol_press_thermometer_model_idx_lon",
            items=[m[0] for m in MODELS_LIQ_ONLY_TEMPERATURE],
            callback=self._update_controls)

        rb_cl = gui.appendRadioButton(self.liq_ol_press_thermometer_choice_buttons, "Use Liq-Ol thermometer")
        self.liq_ol_press_thermometer_model_box_cl = gui.comboBox(
            gui.indentedBox(self.liq_ol_press_thermometer_choice_buttons, gui.checkButtonOffsetHint(rb_cl)),
            self, "liq_ol_press_thermometer_model_idx_lo",
            items=[m[0] for m in MODELS_LIQ_OL_TEMPERATURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.liq_ol_press_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "liq_ol_press_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.liq_ol_press_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "liq_ol_press_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _update_liq_ol_temp_controls(self):
        """Update controls for Liq-Ol/Liq-only Thermometry"""
        # Get the appropriate model list based on current mode
        if hasattr(self, 'liq_thermometry_mode') and self.liq_thermometry_mode == 1:  # Liq-only mode
            model_list = MODELS_LIQ_ONLY_TEMPERATURE
        else:  # Default to Liq-Ol mode
            model_list = MODELS_LIQ_OL_TEMPERATURE

        _, _, requires_press, requires_h2o = model_list[self.liq_ol_temp_model_idx]

        # Enable/disable pressure input group
        self.liq_ol_temp_pressure_box.setEnabled(requires_press)

        # Enable/disable pressure value box
        self.liq_ol_press_temp_value_box.setEnabled(
            requires_press and self.liq_ol_temp_pressure_type == 1)

        # Enable/disable barometer choice and model boxes
        model_as_p_active = requires_press and self.liq_ol_temp_pressure_type == 2
        self.liq_ol_temp_barometer_choice_buttons.setEnabled(model_as_p_active)

        if model_as_p_active:
            self.liq_ol_temp_barometer_model_box_co.setEnabled(
                self.liq_ol_temp_barometer_choice == 0)
            self.liq_ol_temp_barometer_model_box_cl.setEnabled(
                self.liq_ol_temp_barometer_choice == 1)
        else:
            self.liq_ol_temp_barometer_model_box_co.setEnabled(False)
            self.liq_ol_temp_barometer_model_box_cl.setEnabled(False)

        # Enable/disable H2O controls
        self.liq_ol_temp_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.liq_ol_temp_fixed_h2o_input.setEnabled(
            requires_h2o and self.liq_ol_temp_fixed_h2o)

    def _update_liq_ol_press_controls(self):
        """Update controls for Liq-Ol/Liq-only Barometry"""
        # Get the appropriate model list based on current mode
        if hasattr(self, 'liq_barometry_mode') and self.liq_barometry_mode == 1:  # Liq-only mode
            model_list = MODELS_LIQ_ONLY_PRESSURE
        else:  # Default to Liq-Ol mode
            model_list = MODELS_LIQ_OL_PRESSURE

        _, _, requires_temp, requires_h2o = model_list[self.liq_ol_press_model_idx]

        # Enable/disable temperature input group
        self.liq_ol_press_temp_box.setEnabled(requires_temp)

        # Enable/disable temperature value box
        self.liq_ol_press_temp_value_box.setEnabled(
            requires_temp and self.liq_ol_press_temp_type == 1)

        # Enable/disable thermometer choice and model boxes
        model_as_t_active = requires_temp and self.liq_ol_press_temp_type == 2
        self.liq_ol_press_thermometer_choice_buttons.setEnabled(model_as_t_active)

        if model_as_t_active:
            self.liq_ol_press_thermometer_model_box_co.setEnabled(
                self.liq_ol_press_thermometer_choice == 0)
            self.liq_ol_press_thermometer_model_box_cl.setEnabled(
                self.liq_ol_press_thermometer_choice == 1)
        else:
            self.liq_ol_press_thermometer_model_box_co.setEnabled(False)
            self.liq_ol_press_thermometer_model_box_cl.setEnabled(False)

        # Enable/disable H2O controls
        self.liq_ol_press_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.liq_ol_press_fixed_h2o_input.setEnabled(
            requires_h2o and self.liq_ol_press_fixed_h2o)











    def _calculate_liq_ol_press(self, df):
        """Calculate Liq-Ol or Liq-only pressures based on current mode"""
        # Determine which model set to use
        if hasattr(self, 'liq_barometry_mode') and self.liq_barometry_mode == 1:  # Liq-only mode
            model_list = MODELS_LIQ_ONLY_PRESSURE
            mode_name = "Liq-only Barometry"
            print(f"DEBUG: Using Liq-only mode with model index {self.liq_ol_press_model_idx}")
        else:  # Default to Liq-Ol mode
            model_list = MODELS_LIQ_OL_PRESSURE
            mode_name = "Liq-Ol Barometry"
            print(f"DEBUG: Using Liq-Ol mode with model index {self.liq_ol_press_model_idx}")

        _, current_model_func_name, requires_temp, requires_h2o = model_list[self.liq_ol_press_model_idx]
        print(f"DEBUG: Selected model function: {current_model_func_name}")

        # Determine thermometer function if using model temperature
        if requires_temp and self.liq_ol_press_temp_type == 2:
            if self.liq_ol_press_thermometer_choice == 0:  # Liq-only
                current_thermometer_func_name = MODELS_LIQ_ONLY_TEMPERATURE[self.liq_ol_press_thermometer_model_idx_lon][1]
                print(f"DEBUG: Using Liq-only thermometer model: {current_thermometer_func_name}")
            else:  # Liq-Ol
                current_thermometer_func_name = MODELS_LIQ_OL_TEMPERATURE[self.liq_ol_press_thermometer_model_idx_lo][1]
                print(f"DEBUG: Using Liq-Ol thermometer model: {current_thermometer_func_name}")

        df = dm.preprocessing(df, my_output='liq_ol')

        water = self._get_h2o_value(df, requires_h2o,
                                self.liq_ol_press_fixed_h2o,
                                self.liq_ol_press_fixed_h2o_value_str,
                                mode_name)
        if water is None:
            return pd.DataFrame(), "", "", ""

        T_input = self._get_temperature_value(df, requires_temp,
                                            self.liq_ol_press_temp_type,
                                            self.liq_ol_press_temp_value,
                                            mode_name)

        pressure = None
        temperature_output = None

        if requires_temp and self.liq_ol_press_temp_type == 2:  # Model as Temperature
            if self.liq_barometry_mode == 1:  # Liq-only mode
                calc = calculate_liq_ol_press_temp(
                    liq_comps=df[liq_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name)
            else:  # Liq-Ol mode
                calc = calculate_liq_ol_press_temp(
                    liq_comps=df[liq_cols], ol_comps=df[ol_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name,
                    H2O_Liq=water)
            pressure = calc['P_kbar_calc']
            temperature_output = calc['T_K_calc']
        else:  # Fixed or dataset temperature
            if self.liq_barometry_mode == 1:  # Liq-only mode
                pressure_result = calculate_liq_only_press(
                    liq_comps=df[liq_cols],
                    equationP=current_model_func_name,
                    T=T_input)
                # Handle cases where the function returns a DataFrame (like Ridolfi2021)
                if isinstance(pressure_result, pd.DataFrame):
                    pressure = pressure_result['P_kbar_calc']
                else:
                    pressure = pressure_result
            else:  # Liq-Ol mode
                pressure = calculate_liq_ol_press(
                    liq_comps=df[liq_cols], ol_comps=df[ol_cols],
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

        return results_df, "LiqOl", "T_K", "P_kbar"

    def _calculate_liq_ol_temp(self, df):
        """Calculate Liq-Ol or Liq-only temperatures based on current mode"""



        # Determine which model set to use
        if hasattr(self, 'liq_thermometry_mode') and self.liq_thermometry_mode == 1:  # Liq-only mode
            model_list = MODELS_LIQ_ONLY_TEMPERATURE
            mode_name = "Liq-only Thermometry"
        else:  # Default to Liq-Ol mode
            model_list = MODELS_LIQ_OL_TEMPERATURE
            mode_name = "Liq-Ol Thermometry"

        _, current_model_func_name, requires_pressure, requires_h2o = model_list[self.liq_ol_temp_model_idx]

        print(">>> Entered _calculate_liq_ol_temp")
        print(f"Model index: {self.liq_ol_temp_model_idx}")
        print(f"Mode: {'Liq-only' if self.liq_thermometry_mode == 1 else 'Liq-Ol'}")
        print(f"Returned df length: {len(df)}")
        print(f"Requires pressure: {requires_pressure}, requires H2O: {requires_h2o}")


        # Determine barometer function if using model pressure
        if requires_pressure and self.liq_ol_temp_pressure_type == 2:
            if self.liq_ol_temp_barometer_choice == 0:  # Liq-only
                current_barometer_func_name = MODELS_LIQ_ONLY_PRESSURE[self.liq_ol_temp_barometer_model_idx_lon][1]
            else:  # Liq-Ol
                current_barometer_func_name = MODELS_LIQ_OL_PRESSURE[self.liq_ol_temp_barometer_model_idx_lo][1]

        df = dm.preprocessing(df, my_output='liq_ol')

        water = self._get_h2o_value(df, requires_h2o,
                                self.liq_ol_temp_fixed_h2o,
                                self.liq_ol_temp_fixed_h2o_value_str,
                                mode_name)
        if water is None: return pd.DataFrame(), "", "", ""

        P_input = self._get_pressure_value(df, requires_pressure,
                                        self.liq_ol_temp_pressure_type,
                                        self.liq_ol_temp_pressure_value,
                                        mode_name)


        temperature = None
        pressure_output = None

        # Not relevant right now, as no barometers.
        if requires_pressure and self.liq_ol_temp_pressure_type == 2:  # Model as Pressure
            if self.liq_thermometry_mode == 1:  # Liq-only mode
                calc = calculate_liq_only_press_temp(
                    liq_comps=df[liq_cols],
                    equationT=current_model_func_name,
                    equationP=current_barometer_func_name
                    , H2O_Liq=water)
            else:  # Liq-Ol mode
                calc = calculate_liq_ol_press_temp(
                    liq_comps=df[liq_cols], ol_comps=df[ol_cols],
                    equationT=current_model_func_name,
                    equationP=current_barometer_func_name,
                    H2O_Liq=water)
            temperature = calc['T_K_calc']
            pressure_output = calc['P_kbar_calc']

        # This is the relevant one for us.
        else:  # Fixed or dataset pressure
            if self.liq_thermometry_mode == 1:  # Liq-only mode
                temperature = calculate_liq_only_temp(
                    liq_comps=df[liq_cols],
                    equationT=current_model_func_name,
                    P=P_input, H2O_Liq=water)
            else:  # Liq-Ol mode - outputs Kd hence need .T_K_calc
                temperature = calculate_ol_liq_temp(
                    liq_comps=df[liq_cols], ol_comps=df[ol_cols],
                    equationT=current_model_func_name,
                    P=P_input,
                    H2O_Liq=water).T_K_calc

        results_df = pd.DataFrame()
        results_df['T_K_calc'] = temperature

        if pressure_output is not None:
            results_df['P_kbar_calc'] = pressure_output
        elif P_input is not None:
            results_df['P_kbar_input'] = P_input
        else:
            results_df['P_kbar_input'] = np.full(len(df), np.nan)

        print(">>> Result columns:", results_df.columns)

        return results_df, "LiqOl", "T_K", "P_kbar"




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

    ## Kspar-Plag functions

    def _build_plag_kspar_temp_gui(self, parent_box):
        """Build GUI for Plag-Kspar Thermometry"""
        # Models selection
        temp_model_box = gui.vBox(parent_box, "Models")
        self.plag_kspar_temp_models_combo = gui.comboBox(
            temp_model_box, self, "plag_kspar_temp_model_idx",
            items=[m[0] for m in MODELS_PLAG_KSPAR_TEMP],
            callback=self._update_controls)

        # Pressure settings
        self.plag_kspar_temp_pressure_box = gui.radioButtons(
            parent_box, self, "plag_kspar_temp_pressure_type", box="Pressure Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.plag_kspar_temp_pressure_box, "Dataset as Pressure (kbar)")

        rb_fixed_p = gui.appendRadioButton(self.plag_kspar_temp_pressure_box, "Fixed Pressure")
        self.plag_kspar_temp_pressure_value_box = gui.doubleSpin(
            gui.indentedBox(self.plag_kspar_temp_pressure_box, gui.checkButtonOffsetHint(rb_fixed_p)), self,
            "plag_kspar_temp_pressure_value", 1.0, 10000.0, step=0.1, label="Pressure Value (kbar)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=1)

        rb_model_p = gui.appendRadioButton(self.plag_kspar_temp_pressure_box, "Model as Pressure")
        model_as_p_box = gui.indentedBox(self.plag_kspar_temp_pressure_box, gui.checkButtonOffsetHint(rb_model_p))

        self.plag_kspar_temp_barometer_model_box = gui.comboBox(
            model_as_p_box, self, "plag_kspar_temp_barometer_model_idx",
            items=[m[0] for m in MODELS_PLAG_KSPAR_PRESSURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.plag_kspar_temp_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "plag_kspar_temp_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.plag_kspar_temp_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "plag_kspar_temp_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)

    def _build_plag_kspar_press_gui(self, parent_box):
        """Build GUI for Plag-Kspar Barometry"""
        # Models selection
        press_model_box = gui.vBox(parent_box, "Models")
        self.plag_kspar_press_models_combo = gui.comboBox(
            press_model_box, self, "plag_kspar_press_model_idx",
            items=[m[0] for m in MODELS_PLAG_KSPAR_PRESSURE],
            callback=self._update_controls)

        # Temperature settings
        self.plag_kspar_press_temp_box = gui.radioButtons(
            parent_box, self, "plag_kspar_press_temp_type", box="Temperature Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.plag_kspar_press_temp_box, "Dataset as Temperature (K)")

        rb_fixed_t = gui.appendRadioButton(self.plag_kspar_press_temp_box, "Fixed Temperature")
        self.plag_kspar_press_temp_value_box = gui.doubleSpin(
            gui.indentedBox(self.plag_kspar_press_temp_box, gui.checkButtonOffsetHint(rb_fixed_t)), self,
            "plag_kspar_press_temp_value", 500.0, 2000.0, step=1.0, label="Temperature Value (K)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=0)

        rb_model_t = gui.appendRadioButton(self.plag_kspar_press_temp_box, "Model as Temperature")
        model_as_t_box = gui.indentedBox(self.plag_kspar_press_temp_box, gui.checkButtonOffsetHint(rb_model_t))

        self.plag_kspar_press_thermometer_model_box = gui.comboBox(
            model_as_t_box, self, "plag_kspar_press_thermometer_model_idx",
            items=[m[0] for m in MODELS_PLAG_KSPAR_TEMP],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.plag_kspar_press_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "plag_kspar_press_fixed_h2o", "Fixed H₂O", callback=self._update_controls)

        self.plag_kspar_press_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "plag_kspar_press_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _update_plag_kspar_temp_controls(self):
        """Update controls for Plag-Kspar Thermometry"""
        _, _, requires_pressure, requires_h2o = MODELS_PLAG_KSPAR_TEMP[self.plag_kspar_temp_model_idx]

        # Enable/disable pressure radio group
        self.plag_kspar_temp_pressure_box.setEnabled(requires_pressure)

        # Enable/disable pressure value box
        self.plag_kspar_temp_pressure_value_box.setEnabled(
            requires_pressure and self.plag_kspar_temp_pressure_type == 1)

        # Enable/disable barometer model box
        self.plag_kspar_temp_barometer_model_box.setEnabled(
            requires_pressure and self.plag_kspar_temp_pressure_type == 2)

        # Enable/disable H2O input
        self.plag_kspar_temp_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.plag_kspar_temp_fixed_h2o_input.setEnabled(requires_h2o and self.plag_kspar_temp_fixed_h2o)

    def _update_plag_kspar_press_controls(self):
        """Update controls for Plag-Kspar Barometry"""
        _, _, requires_temp, requires_h2o = MODELS_PLAG_KSPAR_PRESSURE[self.plag_kspar_press_model_idx]

        # Enable/disable temperature radio group
        self.plag_kspar_press_temp_box.setEnabled(requires_temp)

        # Enable/disable temperature value box
        self.plag_kspar_press_temp_value_box.setEnabled(
            requires_temp and self.plag_kspar_press_temp_type == 1)

        # Enable/disable thermometer model box
        self.plag_kspar_press_thermometer_model_box.setEnabled(
            requires_temp and self.plag_kspar_press_temp_type == 2)

        # Enable/disable H2O input
        self.plag_kspar_press_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.plag_kspar_press_fixed_h2o_input.setEnabled(requires_h2o and self.plag_kspar_press_fixed_h2o)



    def _calculate_plag_kspar_press(self, df):
        """Calculate Plag-Kspar pressures"""
        _, current_model_func_name, requires_temp, requires_h2o = MODELS_PLAG_KSPAR_PRESSURE[self.plag_kspar_press_model_idx]
        current_thermometer_func_name = MODELS_PLAG_KSPAR_TEMP[self.plag_kspar_press_thermometer_model_idx][1]

        df = dm.preprocessing(df, my_output='plag_kspar')

        water = self._get_h2o_value(df, requires_h2o,
                                self.plag_kspar_press_fixed_h2o,
                                self.plag_kspar_press_fixed_h2o_value_str,
                                "Plag-Kspar Barometry")
        if water is None:
            return pd.DataFrame(), "", "", ""

        T_input = self._get_temperature_value(df, requires_temp,
                                            self.plag_kspar_press_temp_type,
                                            self.plag_kspar_press_temp_value,
                                            "Plag-Kspar Barometry")

        # Initialize results
        results_df = pd.DataFrame()

        if requires_temp and self.plag_kspar_press_temp_type == 2:  # Model as Temperature
            try:
                calc = calculate_plag_kspar_press_temp(
                    kspar_comps=df[kspar_cols],
                    plag_comps=df[plag_cols],
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
                pressure = calculate_plag_kspar_press(
                    kspar_comps=df[kspar_cols],
                    plag_comps=df[plag_cols],
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

        return results_df, "PlagKspar", "T_K", "P_kbar"

    def _calculate_plag_kspar_temp(self, df):
        """Encapsulates the Plag-Kspar Thermometry calculation logic."""
        _, current_model_func_name, requires_pressure_by_model, requires_h2o_by_model = MODELS_PLAG_KSPAR_TEMP[self.plag_kspar_temp_model_idx]
        current_barometer_func_name = MODELS_PLAG_KSPAR_PRESSURE[self.plag_kspar_temp_barometer_model_idx][1]

        df = dm.preprocessing(df, my_output='plag_kspar')

        water = self._get_h2o_value(df, requires_h2o_by_model,
                                    self.plag_kspar_temp_fixed_h2o,
                                    self.plag_kspar_temp_fixed_h2o_value_str,
                                    "Plag-Kspar Thermometry")
        if water is None: return pd.DataFrame(), "", "", "" # Error occurred in H2O fetching

        P_input = self._get_pressure_value(df, requires_pressure_by_model,
                                           self.plag_kspar_temp_pressure_type,
                                           self.plag_kspar_temp_pressure_value,
                                           "Plag-Kspar Thermometry")

        temperature = None
        pressure_output = None # This is for when pressure is calculated iteratively with temp

        if requires_pressure_by_model and self.plag_kspar_temp_pressure_type == 2: # Model as Pressure
            calc = calculate_plag_kspar_press_temp(
                kspar_comps=df[kspar_cols], plag_comps=df[plag_cols],
                equationT=current_model_func_name, equationP=current_barometer_func_name)
            temperature = calc['T_K_calc']
            pressure_output = calc['P_kbar_calc']
        else: # No pressure, fixed, or dataset pressure
            temperature = calculate_plag_kspar_temp(
                kspar_comps=df[kspar_cols], plag_comps=df[plag_cols],
                equationT=current_model_func_name, P=P_input)


        results_df = pd.DataFrame()
        results_df['T_K_calc'] = temperature

        if pressure_output is not None:
            results_df['P_kbar_calc'] = pressure_output
        elif P_input is not None:
            results_df['P_kbar_input'] = P_input # Store the input pressure if used
        else:
            results_df['P_kbar_input'] = np.full(len(df), np.nan) # Placeholder if no P input

        return results_df, "PlagKspar", "T_K", "P_kbar"

## Plag-Liq

    ## Plag-only and Plag-Liq stuff

    def _build_plag_liq_temp_gui(self, parent_box):
        """Build GUI for Plag Thermometry"""
        # Mode selection
        mode_box = gui.hBox(parent_box)
        gui.label(mode_box, self, "Thermometry Mode:")
        self.plag_thermometry_mode_buttons = gui.radioButtons(
            mode_box, self, "plag_thermometry_mode",
            callback=self._update_controls)
        gui.appendRadioButton(self.plag_thermometry_mode_buttons, "Plag-Liq")
        gui.appendRadioButton(self.plag_thermometry_mode_buttons, "Plag-only")

        # Models selection
        temp_model_box = gui.vBox(parent_box, "Models")
        self.plag_liq_temp_models_combo = gui.comboBox(
            temp_model_box, self, "plag_liq_temp_model_idx",
            items=[],  # Populated later
            callback=self._update_controls)

        # Pressure settings
        self.plag_liq_temp_pressure_box = gui.radioButtons(
            parent_box, self, "plag_liq_temp_pressure_type", box="Pressure Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.plag_liq_temp_pressure_box, "Dataset as Pressure (kbar)")

        rb_fixed_p = gui.appendRadioButton(self.plag_liq_temp_pressure_box, "Fixed Pressure")


        self.plag_liq_temp_pressure_value_box = gui.doubleSpin(
            gui.indentedBox(self.plag_liq_temp_pressure_box, gui.checkButtonOffsetHint(rb_fixed_p)), self,
            "plag_liq_temp_pressure_value", 0, 1000, step=1.0, label="Pressure Value (kbar)",
            alignment=Qt.AlignRight, callback=self.commit.deferred, controlWidth=80, decimals=0)

        rb_model_p = gui.appendRadioButton(self.plag_liq_temp_pressure_box, "Model as Pressure")
        model_as_p_box = gui.indentedBox(self.plag_liq_temp_pressure_box, gui.checkButtonOffsetHint(rb_model_p))

        self.plag_liq_temp_barometer_choice_buttons = gui.radioButtons(
            model_as_p_box, self, "plag_liq_temp_barometer_choice",
            callback=self._update_controls)

        rb_co = gui.appendRadioButton(self.plag_liq_temp_barometer_choice_buttons, "Use Plag-only barometer")
        self.plag_liq_temp_barometer_model_box_co = gui.comboBox(
            gui.indentedBox(self.plag_liq_temp_barometer_choice_buttons, gui.checkButtonOffsetHint(rb_co)),
            self, "plag_liq_temp_barometer_model_idx_co",
            items=[m[0] for m in MODELS_PLAG_ONLY_PRESSURE],
            callback=self._update_controls)

        rb_cl = gui.appendRadioButton(self.plag_liq_temp_barometer_choice_buttons, "Use Plag-Liq barometer")
        self.plag_liq_temp_barometer_model_box_cl = gui.comboBox(
            gui.indentedBox(self.plag_liq_temp_barometer_choice_buttons, gui.checkButtonOffsetHint(rb_cl)),
            self, "plag_liq_temp_barometer_model_idx_cl",
            items=[m[0] for m in MODELS_PLAG_LIQ_PRESSURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.plag_liq_temp_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "plag_liq_temp_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.plag_liq_temp_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "plag_liq_temp_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _build_plag_liq_press_gui(self, parent_box):
        """Build GUI for Plag Barometry"""
        # Mode selection
        mode_box = gui.hBox(parent_box)
        gui.label(mode_box, self, "Barometry Mode:")
        self.plag_barometry_mode_buttons = gui.radioButtons(
            mode_box, self, "plag_barometry_mode",
            callback=self._update_controls)
        gui.appendRadioButton(self.plag_barometry_mode_buttons, "Plag-Liq")
        gui.appendRadioButton(self.plag_barometry_mode_buttons, "Plag-only")

        # Models selection
        press_model_box = gui.vBox(parent_box, "Models")
        self.plag_liq_press_models_combo = gui.comboBox(
            press_model_box, self, "plag_liq_press_model_idx",
            items=[],  # Populated later
            callback=self._update_controls)

        # Temperature settings
        self.plag_liq_press_temp_box = gui.radioButtons(
            parent_box, self, "plag_liq_press_temp_type", box="Temperature Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.plag_liq_press_temp_box, "Dataset as Temperature (K)")

        rb_fixed_t = gui.appendRadioButton(self.plag_liq_press_temp_box, "Fixed Temperature")
        self.plag_liq_press_temp_value_box = gui.doubleSpin(
            gui.indentedBox(self.plag_liq_press_temp_box, gui.checkButtonOffsetHint(rb_fixed_t)), self,
            "plag_liq_press_temp_value", 500.0, 2000.0, step=1.0, label="Temperature Value (K)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=0)

        rb_model_t = gui.appendRadioButton(self.plag_liq_press_temp_box, "Model as Temperature")
        model_as_t_box = gui.indentedBox(self.plag_liq_press_temp_box, gui.checkButtonOffsetHint(rb_model_t))

        self.plag_liq_press_thermometer_choice_buttons = gui.radioButtons(
            model_as_t_box, self, "plag_liq_press_thermometer_choice",
            callback=self._update_controls)

        rb_co = gui.appendRadioButton(self.plag_liq_press_thermometer_choice_buttons, "Use Plag-only thermometer")
        self.plag_liq_press_thermometer_model_box_co = gui.comboBox(
            gui.indentedBox(self.plag_liq_press_thermometer_choice_buttons, gui.checkButtonOffsetHint(rb_co)),
            self, "plag_liq_press_thermometer_model_idx_co",
            items=[m[0] for m in MODELS_PLAG_ONLY_TEMPERATURE],
            callback=self._update_controls)

        rb_cl = gui.appendRadioButton(self.plag_liq_press_thermometer_choice_buttons, "Use Plag-Liq thermometer")
        self.plag_liq_press_thermometer_model_box_cl = gui.comboBox(
            gui.indentedBox(self.plag_liq_press_thermometer_choice_buttons, gui.checkButtonOffsetHint(rb_cl)),
            self, "plag_liq_press_thermometer_model_idx_cl",
            items=[m[0] for m in MODELS_PLAG_LIQ_TEMPERATURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.plag_liq_press_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "plag_liq_press_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.plag_liq_press_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "plag_liq_press_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _update_plag_liq_temp_controls(self):
        """Update controls for Plag-Liq/Plag-only Thermometry"""
        # Get the appropriate model list based on current mode
        if hasattr(self, 'plag_thermometry_mode') and self.plag_thermometry_mode == 1:  # Plag-only mode
            model_list = MODELS_PLAG_ONLY_TEMPERATURE
        else:  # Default to Plag-Liq mode
            model_list = MODELS_PLAG_LIQ_TEMPERATURE

        _, _, requires_press, requires_h2o = model_list[self.plag_liq_temp_model_idx]

        # Enable/disable pressure input group
        self.plag_liq_temp_pressure_box.setEnabled(requires_press)

        # Enable/disable pressure value box
        self.plag_liq_press_temp_value_box.setEnabled(
            requires_press and self.plag_liq_temp_pressure_type == 1)

        # Enable/disable barometer choice and model boxes
        model_as_p_active = requires_press and self.plag_liq_temp_pressure_type == 2
        self.plag_liq_temp_barometer_choice_buttons.setEnabled(model_as_p_active)

        if model_as_p_active:
            self.plag_liq_temp_barometer_model_box_co.setEnabled(
                self.plag_liq_temp_barometer_choice == 0)
            self.plag_liq_temp_barometer_model_box_cl.setEnabled(
                self.plag_liq_temp_barometer_choice == 1)
        else:
            self.plag_liq_temp_barometer_model_box_co.setEnabled(False)
            self.plag_liq_temp_barometer_model_box_cl.setEnabled(False)

        # Enable/disable H2O controls
        self.plag_liq_temp_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.plag_liq_temp_fixed_h2o_input.setEnabled(
            requires_h2o and self.plag_liq_temp_fixed_h2o)

    def _update_plag_liq_press_controls(self):
        """Update controls for Plag-Liq/Plag-only Barometry"""
        # Get the appropriate model list based on current mode
        if hasattr(self, 'plag_barometry_mode') and self.plag_barometry_mode == 1:  # Plag-only mode
            model_list = MODELS_PLAG_ONLY_PRESSURE
        else:  # Default to Plag-Liq mode
            model_list = MODELS_PLAG_LIQ_PRESSURE

        _, _, requires_temp, requires_h2o = model_list[self.plag_liq_press_model_idx]

        # Enable/disable temperature input group
        self.plag_liq_press_temp_box.setEnabled(requires_temp)

        # Enable/disable temperature value box
        self.plag_liq_press_temp_value_box.setEnabled(
            requires_temp and self.plag_liq_press_temp_type == 1)

        # Enable/disable thermometer choice and model boxes
        model_as_t_active = requires_temp and self.plag_liq_press_temp_type == 2
        self.plag_liq_press_thermometer_choice_buttons.setEnabled(model_as_t_active)

        if model_as_t_active:
            self.plag_liq_press_thermometer_model_box_co.setEnabled(
                self.plag_liq_press_thermometer_choice == 0)
            self.plag_liq_press_thermometer_model_box_cl.setEnabled(
                self.plag_liq_press_thermometer_choice == 1)
        else:
            self.plag_liq_press_thermometer_model_box_co.setEnabled(False)
            self.plag_liq_press_thermometer_model_box_cl.setEnabled(False)

        # Enable/disable H2O controls
        self.plag_liq_press_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.plag_liq_press_fixed_h2o_input.setEnabled(
            requires_h2o and self.plag_liq_press_fixed_h2o)











    def _calculate_plag_liq_press(self, df):
        """Calculate Plag-Liq or Plag-only pressures based on current mode"""
        # Determine which model set to use
        if hasattr(self, 'plag_barometry_mode') and self.plag_barometry_mode == 1:  # Plag-only mode
            model_list = MODELS_PLAG_ONLY_PRESSURE
            mode_name = "Plag-only Barometry"
            print(f"DEBUG: Using Plag-only mode with model index {self.plag_liq_press_model_idx}")
        else:  # Default to Plag-Liq mode
            model_list = MODELS_PLAG_LIQ_PRESSURE
            mode_name = "Plag-Liq Barometry"
            print(f"DEBUG: Using Plag-Liq mode with model index {self.plag_liq_press_model_idx}")

        _, current_model_func_name, requires_temp, requires_h2o = model_list[self.plag_liq_press_model_idx]
        print(f"DEBUG: Selected model function: {current_model_func_name}")

        # Determine thermometer function if using model temperature
        if requires_temp and self.plag_liq_press_temp_type == 2:
            if self.plag_liq_press_thermometer_choice == 0:  # Plag-only
                current_thermometer_func_name = MODELS_PLAG_ONLY_TEMPERATURE[self.plag_liq_press_thermometer_model_idx_co][1]
                print(f"DEBUG: Using Plag-only thermometer model: {current_thermometer_func_name}")
            else:  # Plag-Liq
                current_thermometer_func_name = MODELS_PLAG_LIQ_TEMPERATURE[self.plag_liq_press_thermometer_model_idx_cl][1]
                print(f"DEBUG: Using Plag-Liq thermometer model: {current_thermometer_func_name}")

        df = dm.preprocessing(df, my_output='plag_liq')

        water = self._get_h2o_value(df, requires_h2o,
                                self.plag_liq_press_fixed_h2o,
                                self.plag_liq_press_fixed_h2o_value_str,
                                mode_name)
        if water is None:
            return pd.DataFrame(), "", "", ""

        T_input = self._get_temperature_value(df, requires_temp,
                                            self.plag_liq_press_temp_type,
                                            self.plag_liq_press_temp_value,
                                            mode_name)

        pressure = None
        temperature_output = None

        if requires_temp and self.plag_liq_press_temp_type == 2:  # Model as Temperature
            if self.plag_barometry_mode == 1:  # Plag-only mode
                calc = calculate_fspar_liq_press_temp(
                    plag_comps=df[plag_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name)
            else:  # Plag-Liq mode
                calc = calculate_fspar_liq_press_temp(
                    plag_comps=df[plag_cols], liq_comps=df[liq_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name,
                    H2O_Liq=water)
            pressure = calc['P_kbar_calc']
            temperature_output = calc['T_K_calc']
        else:  # Fixed or dataset temperature
            if self.plag_barometry_mode == 1:  # Plag-only mode
                pressure_result = calculate_fspar_only_press(
                    plag_comps=df[plag_cols],
                    equationP=current_model_func_name,
                    T=T_input)
                # Handle cases where the function returns a DataFrame (like Ridolfi2021)
                if isinstance(pressure_result, pd.DataFrame):
                    pressure = pressure_result['P_kbar_calc']
                else:
                    pressure = pressure_result
            else:  # Plag-Liq mode
                pressure = calculate_fspar_liq_press(
                    plag_comps=df[plag_cols], liq_comps=df[liq_cols],
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

        return results_df, "PlagLiq", "T_K", "P_kbar"

    def _calculate_plag_liq_temp(self, df):
        """Calculate Plag-Liq or Plag-only temperatures based on current mode"""



        # Determine which model set to use
        if hasattr(self, 'plag_thermometry_mode') and self.plag_thermometry_mode == 1:  # Plag-only mode
            model_list = MODELS_PLAG_ONLY_TEMPERATURE
            mode_name = "Plag-only Thermometry"
        else:  # Default to Plag-Liq mode
            model_list = MODELS_PLAG_LIQ_TEMPERATURE
            mode_name = "Plag-Liq Thermometry"

        _, current_model_func_name, requires_pressure, requires_h2o = model_list[self.plag_liq_temp_model_idx]

        print(">>> Entered _calculate_plag_liq_temp")
        print(f"Model index: {self.plag_liq_temp_model_idx}")
        print(f"Mode: {'Plag-only' if self.plag_thermometry_mode == 1 else 'Plag-Liq'}")
        print(f"Returned df length: {len(df)}")
        print(f"Requires pressure: {requires_pressure}, requires H2O: {requires_h2o}")


        # Determine barometer function if using model pressure
        if requires_pressure and self.plag_liq_temp_pressure_type == 2:
            if self.plag_liq_temp_barometer_choice == 0:  # Plag-only
                current_barometer_func_name = MODELS_PLAG_ONLY_PRESSURE[self.plag_liq_temp_barometer_model_idx_co][1]
            else:  # Plag-Liq
                current_barometer_func_name = MODELS_PLAG_LIQ_PRESSURE[self.plag_liq_temp_barometer_model_idx_cl][1]

        df = dm.preprocessing(df, my_output='plag_liq')

        water = self._get_h2o_value(df, requires_h2o,
                                self.plag_liq_temp_fixed_h2o,
                                self.plag_liq_temp_fixed_h2o_value_str,
                                mode_name)
        if water is None: return pd.DataFrame(), "", "", ""

        P_input = self._get_pressure_value(df, requires_pressure,
                                        self.plag_liq_temp_pressure_type,
                                        self.plag_liq_temp_pressure_value,
                                        mode_name)


        temperature = None
        pressure_output = None

        if requires_pressure and self.plag_liq_temp_pressure_type == 2:  # Model as Pressure
            if self.plag_thermometry_mode == 1:  # Plag-only mode
                calc = calculate_plag_only_press_temp(
                    plag_comps=df[plag_cols],
                    equationT=current_model_func_name,
                    equationP=current_barometer_func_name)
            else:  # Plag-Liq mode
                calc = calculate_fspar_liq_press_temp(
                    plag_comps=df[plag_cols], liq_comps=df[liq_cols],
                    equationT=current_model_func_name,
                    equationP=current_barometer_func_name,
                    H2O_Liq=water)
            temperature = calc['T_K_calc']
            pressure_output = calc['P_kbar_calc']
        else:  # Fixed or dataset pressure
            if self.plag_thermometry_mode == 1:  # Plag-only mode
                temperature = calculate_plag_only_temp(
                    plag_comps=df[plag_cols],
                    equationT=current_model_func_name,
                    P=P_input)
            else:  # Plag-Liq mode
                temperature = calculate_fspar_liq_temp(
                    plag_comps=df[plag_cols], liq_comps=df[liq_cols],
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

        return results_df, "PlagLiq", "T_K", "P_kbar"







    ## Kspar-only and Kspar-Liq stuff

    def _build_kspar_liq_temp_gui(self, parent_box):
        """Build GUI for Kspar Thermometry"""
        # Mode selection
        mode_box = gui.hBox(parent_box)
        gui.label(mode_box, self, "Thermometry Mode:")
        self.kspar_thermometry_mode_buttons = gui.radioButtons(
            mode_box, self, "kspar_thermometry_mode",
            callback=self._update_controls)
        gui.appendRadioButton(self.kspar_thermometry_mode_buttons, "Kspar-Liq")
        gui.appendRadioButton(self.kspar_thermometry_mode_buttons, "Kspar-only")

        # Models selection
        temp_model_box = gui.vBox(parent_box, "Models")
        self.kspar_liq_temp_models_combo = gui.comboBox(
            temp_model_box, self, "kspar_liq_temp_model_idx",
            items=[],  # Populated later
            callback=self._update_controls)

        # Pressure settings
        self.kspar_liq_temp_pressure_box = gui.radioButtons(
            parent_box, self, "kspar_liq_temp_pressure_type", box="Pressure Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.kspar_liq_temp_pressure_box, "Dataset as Pressure (kbar)")

        rb_fixed_p = gui.appendRadioButton(self.kspar_liq_temp_pressure_box, "Fixed Pressure")


        self.kspar_liq_temp_pressure_value_box = gui.doubleSpin(
            gui.indentedBox(self.kspar_liq_temp_pressure_box, gui.checkButtonOffsetHint(rb_fixed_p)), self,
            "kspar_liq_temp_pressure_value", 0, 1000, step=1.0, label="Pressure Value (kbar)",
            alignment=Qt.AlignRight, callback=self.commit.deferred, controlWidth=80, decimals=0)

        rb_model_p = gui.appendRadioButton(self.kspar_liq_temp_pressure_box, "Model as Pressure")
        model_as_p_box = gui.indentedBox(self.kspar_liq_temp_pressure_box, gui.checkButtonOffsetHint(rb_model_p))

        self.kspar_liq_temp_barometer_choice_buttons = gui.radioButtons(
            model_as_p_box, self, "kspar_liq_temp_barometer_choice",
            callback=self._update_controls)

        rb_co = gui.appendRadioButton(self.kspar_liq_temp_barometer_choice_buttons, "Use Kspar-only barometer")
        self.kspar_liq_temp_barometer_model_box_co = gui.comboBox(
            gui.indentedBox(self.kspar_liq_temp_barometer_choice_buttons, gui.checkButtonOffsetHint(rb_co)),
            self, "kspar_liq_temp_barometer_model_idx_co",
            items=[m[0] for m in MODELS_KSPAR_ONLY_PRESSURE],
            callback=self._update_controls)

        rb_cl = gui.appendRadioButton(self.kspar_liq_temp_barometer_choice_buttons, "Use Kspar-Liq barometer")
        self.kspar_liq_temp_barometer_model_box_cl = gui.comboBox(
            gui.indentedBox(self.kspar_liq_temp_barometer_choice_buttons, gui.checkButtonOffsetHint(rb_cl)),
            self, "kspar_liq_temp_barometer_model_idx_cl",
            items=[m[0] for m in MODELS_KSPAR_LIQ_PRESSURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.kspar_liq_temp_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "kspar_liq_temp_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.kspar_liq_temp_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "kspar_liq_temp_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _build_kspar_liq_press_gui(self, parent_box):
        """Build GUI for Kspar Barometry"""
        # Mode selection
        mode_box = gui.hBox(parent_box)
        gui.label(mode_box, self, "Barometry Mode:")
        self.kspar_barometry_mode_buttons = gui.radioButtons(
            mode_box, self, "kspar_barometry_mode",
            callback=self._update_controls)
        gui.appendRadioButton(self.kspar_barometry_mode_buttons, "Kspar-Liq")
        gui.appendRadioButton(self.kspar_barometry_mode_buttons, "Kspar-only")

        # Models selection
        press_model_box = gui.vBox(parent_box, "Models")
        self.kspar_liq_press_models_combo = gui.comboBox(
            press_model_box, self, "kspar_liq_press_model_idx",
            items=[],  # Populated later
            callback=self._update_controls)

        # Temperature settings
        self.kspar_liq_press_temp_box = gui.radioButtons(
            parent_box, self, "kspar_liq_press_temp_type", box="Temperature Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.kspar_liq_press_temp_box, "Dataset as Temperature (K)")

        rb_fixed_t = gui.appendRadioButton(self.kspar_liq_press_temp_box, "Fixed Temperature")
        self.kspar_liq_press_temp_value_box = gui.doubleSpin(
            gui.indentedBox(self.kspar_liq_press_temp_box, gui.checkButtonOffsetHint(rb_fixed_t)), self,
            "kspar_liq_press_temp_value", 500.0, 2000.0, step=1.0, label="Temperature Value (K)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=0)

        rb_model_t = gui.appendRadioButton(self.kspar_liq_press_temp_box, "Model as Temperature")
        model_as_t_box = gui.indentedBox(self.kspar_liq_press_temp_box, gui.checkButtonOffsetHint(rb_model_t))

        self.kspar_liq_press_thermometer_choice_buttons = gui.radioButtons(
            model_as_t_box, self, "kspar_liq_press_thermometer_choice",
            callback=self._update_controls)

        rb_co = gui.appendRadioButton(self.kspar_liq_press_thermometer_choice_buttons, "Use Kspar-only thermometer")
        self.kspar_liq_press_thermometer_model_box_co = gui.comboBox(
            gui.indentedBox(self.kspar_liq_press_thermometer_choice_buttons, gui.checkButtonOffsetHint(rb_co)),
            self, "kspar_liq_press_thermometer_model_idx_co",
            items=[m[0] for m in MODELS_KSPAR_ONLY_TEMPERATURE],
            callback=self._update_controls)

        rb_cl = gui.appendRadioButton(self.kspar_liq_press_thermometer_choice_buttons, "Use Kspar-Liq thermometer")
        self.kspar_liq_press_thermometer_model_box_cl = gui.comboBox(
            gui.indentedBox(self.kspar_liq_press_thermometer_choice_buttons, gui.checkButtonOffsetHint(rb_cl)),
            self, "kspar_liq_press_thermometer_model_idx_cl",
            items=[m[0] for m in MODELS_KSPAR_LIQ_TEMPERATURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.kspar_liq_press_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "kspar_liq_press_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.kspar_liq_press_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "kspar_liq_press_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _update_kspar_liq_temp_controls(self):
        """Update controls for Kspar-Liq/Kspar-only Thermometry"""
        # Get the appropriate model list based on current mode
        if hasattr(self, 'kspar_thermometry_mode') and self.kspar_thermometry_mode == 1:  # Kspar-only mode
            model_list = MODELS_KSPAR_ONLY_TEMPERATURE
        else:  # Default to Kspar-Liq mode
            model_list = MODELS_KSPAR_LIQ_TEMPERATURE

        _, _, requires_press, requires_h2o = model_list[self.kspar_liq_temp_model_idx]

        # Enable/disable pressure input group
        self.kspar_liq_temp_pressure_box.setEnabled(requires_press)

        # Enable/disable pressure value box
        self.kspar_liq_press_temp_value_box.setEnabled(
            requires_press and self.kspar_liq_temp_pressure_type == 1)

        # Enable/disable barometer choice and model boxes
        model_as_p_active = requires_press and self.kspar_liq_temp_pressure_type == 2
        self.kspar_liq_temp_barometer_choice_buttons.setEnabled(model_as_p_active)

        if model_as_p_active:
            self.kspar_liq_temp_barometer_model_box_co.setEnabled(
                self.kspar_liq_temp_barometer_choice == 0)
            self.kspar_liq_temp_barometer_model_box_cl.setEnabled(
                self.kspar_liq_temp_barometer_choice == 1)
        else:
            self.kspar_liq_temp_barometer_model_box_co.setEnabled(False)
            self.kspar_liq_temp_barometer_model_box_cl.setEnabled(False)

        # Enable/disable H2O controls
        self.kspar_liq_temp_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.kspar_liq_temp_fixed_h2o_input.setEnabled(
            requires_h2o and self.kspar_liq_temp_fixed_h2o)

    def _update_kspar_liq_press_controls(self):
        """Update controls for Kspar-Liq/Kspar-only Barometry"""
        # Get the appropriate model list based on current mode
        if hasattr(self, 'kspar_barometry_mode') and self.kspar_barometry_mode == 1:  # Kspar-only mode
            model_list = MODELS_KSPAR_ONLY_PRESSURE
        else:  # Default to Kspar-Liq mode
            model_list = MODELS_KSPAR_LIQ_PRESSURE

        _, _, requires_temp, requires_h2o = model_list[self.kspar_liq_press_model_idx]

        # Enable/disable temperature input group
        self.kspar_liq_press_temp_box.setEnabled(requires_temp)

        # Enable/disable temperature value box
        self.kspar_liq_press_temp_value_box.setEnabled(
            requires_temp and self.kspar_liq_press_temp_type == 1)

        # Enable/disable thermometer choice and model boxes
        model_as_t_active = requires_temp and self.kspar_liq_press_temp_type == 2
        self.kspar_liq_press_thermometer_choice_buttons.setEnabled(model_as_t_active)

        if model_as_t_active:
            self.kspar_liq_press_thermometer_model_box_co.setEnabled(
                self.kspar_liq_press_thermometer_choice == 0)
            self.kspar_liq_press_thermometer_model_box_cl.setEnabled(
                self.kspar_liq_press_thermometer_choice == 1)
        else:
            self.kspar_liq_press_thermometer_model_box_co.setEnabled(False)
            self.kspar_liq_press_thermometer_model_box_cl.setEnabled(False)

        # Enable/disable H2O controls
        self.kspar_liq_press_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.kspar_liq_press_fixed_h2o_input.setEnabled(
            requires_h2o and self.kspar_liq_press_fixed_h2o)











    def _calculate_kspar_liq_press(self, df):
        """Calculate Kspar-Liq or Kspar-only pressures based on current mode"""
        # Determine which model set to use
        if hasattr(self, 'kspar_barometry_mode') and self.kspar_barometry_mode == 1:  # Kspar-only mode
            model_list = MODELS_KSPAR_ONLY_PRESSURE
            mode_name = "Kspar-only Barometry"
            print(f"DEBUG: Using Kspar-only mode with model index {self.kspar_liq_press_model_idx}")
        else:  # Default to Kspar-Liq mode
            model_list = MODELS_KSPAR_LIQ_PRESSURE
            mode_name = "Kspar-Liq Barometry"
            print(f"DEBUG: Using Kspar-Liq mode with model index {self.kspar_liq_press_model_idx}")

        _, current_model_func_name, requires_temp, requires_h2o = model_list[self.kspar_liq_press_model_idx]
        print(f"DEBUG: Selected model function: {current_model_func_name}")

        # Determine thermometer function if using model temperature
        if requires_temp and self.kspar_liq_press_temp_type == 2:
            if self.kspar_liq_press_thermometer_choice == 0:  # Kspar-only
                current_thermometer_func_name = MODELS_KSPAR_ONLY_TEMPERATURE[self.kspar_liq_press_thermometer_model_idx_co][1]
                print(f"DEBUG: Using Kspar-only thermometer model: {current_thermometer_func_name}")
            else:  # Kspar-Liq
                current_thermometer_func_name = MODELS_KSPAR_LIQ_TEMPERATURE[self.kspar_liq_press_thermometer_model_idx_cl][1]
                print(f"DEBUG: Using Kspar-Liq thermometer model: {current_thermometer_func_name}")

        df = dm.preprocessing(df, my_output='kspar_liq')

        water = self._get_h2o_value(df, requires_h2o,
                                self.kspar_liq_press_fixed_h2o,
                                self.kspar_liq_press_fixed_h2o_value_str,
                                mode_name)
        if water is None:
            return pd.DataFrame(), "", "", ""

        T_input = self._get_temperature_value(df, requires_temp,
                                            self.kspar_liq_press_temp_type,
                                            self.kspar_liq_press_temp_value,
                                            mode_name)

        pressure = None
        temperature_output = None

        if requires_temp and self.kspar_liq_press_temp_type == 2:  # Model as Temperature
            if self.kspar_barometry_mode == 1:  # Kspar-only mode
                calc = calculate_fspar_liq_press_temp(
                    kspar_comps=df[kspar_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name)
            else:  # Kspar-Liq mode
                calc = calculate_fspar_liq_press_temp(
                    kspar_comps=df[kspar_cols], liq_comps=df[liq_cols],
                    equationP=current_model_func_name,
                    equationT=current_thermometer_func_name,
                    H2O_Liq=water)
            pressure = calc['P_kbar_calc']
            temperature_output = calc['T_K_calc']
        else:  # Fixed or dataset temperature
            if self.kspar_barometry_mode == 1:  # Kspar-only mode
                pressure_result = calculate_fspar_only_press(
                    kspar_comps=df[kspar_cols],
                    equationP=current_model_func_name,
                    T=T_input)
                # Handle cases where the function returns a DataFrame (like Ridolfi2021)
                if isinstance(pressure_result, pd.DataFrame):
                    pressure = pressure_result['P_kbar_calc']
                else:
                    pressure = pressure_result
            else:  # Kspar-Liq mode
                pressure = calculate_fspar_liq_press(
                    kspar_comps=df[kspar_cols], liq_comps=df[liq_cols],
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

        return results_df, "KsparLiq", "T_K", "P_kbar"

    def _calculate_kspar_liq_temp(self, df):
        """Calculate Kspar-Liq or Kspar-only temperatures based on current mode"""



        # Determine which model set to use
        if hasattr(self, 'kspar_thermometry_mode') and self.kspar_thermometry_mode == 1:  # Kspar-only mode
            model_list = MODELS_KSPAR_ONLY_TEMPERATURE
            mode_name = "Kspar-only Thermometry"
        else:  # Default to Kspar-Liq mode
            model_list = MODELS_KSPAR_LIQ_TEMPERATURE
            mode_name = "Kspar-Liq Thermometry"

        _, current_model_func_name, requires_pressure, requires_h2o = model_list[self.kspar_liq_temp_model_idx]

        print(">>> Entered _calculate_kspar_liq_temp")
        print(f"Model index: {self.kspar_liq_temp_model_idx}")
        print(f"Mode: {'Kspar-only' if self.kspar_thermometry_mode == 1 else 'Kspar-Liq'}")
        print(f"Returned df length: {len(df)}")
        print(f"Requires pressure: {requires_pressure}, requires H2O: {requires_h2o}")


        # Determine barometer function if using model pressure
        if requires_pressure and self.kspar_liq_temp_pressure_type == 2:
            if self.kspar_liq_temp_barometer_choice == 0:  # Kspar-only
                current_barometer_func_name = MODELS_KSPAR_ONLY_PRESSURE[self.kspar_liq_temp_barometer_model_idx_co][1]
            else:  # Kspar-Liq
                current_barometer_func_name = MODELS_KSPAR_LIQ_PRESSURE[self.kspar_liq_temp_barometer_model_idx_cl][1]

        df = dm.preprocessing(df, my_output='kspar_liq')

        water = self._get_h2o_value(df, requires_h2o,
                                self.kspar_liq_temp_fixed_h2o,
                                self.kspar_liq_temp_fixed_h2o_value_str,
                                mode_name)
        if water is None: return pd.DataFrame(), "", "", ""

        P_input = self._get_pressure_value(df, requires_pressure,
                                        self.kspar_liq_temp_pressure_type,
                                        self.kspar_liq_temp_pressure_value,
                                        mode_name)


        temperature = None
        pressure_output = None

        if requires_pressure and self.kspar_liq_temp_pressure_type == 2:  # Model as Pressure
            if self.kspar_thermometry_mode == 1:  # Kspar-only mode
                calc = calculate_fspar_only_press_temp(
                    kspar_comps=df[kspar_cols],
                    equationT=current_model_func_name,
                    equationP=current_barometer_func_name)
            else:  # Kspar-Liq mode
                calc = calculate_fspar_liq_press_temp(
                    kspar_comps=df[kspar_cols], liq_comps=df[liq_cols],
                    equationT=current_model_func_name,
                    equationP=current_barometer_func_name,
                    H2O_Liq=water)
            temperature = calc['T_K_calc']
            pressure_output = calc['P_kbar_calc']
        else:  # Fixed or dataset pressure
            if self.kspar_thermometry_mode == 1:  # Kspar-only mode
                temperature = calculate_fspar_only_temp(
                    kspar_comps=df[kspar_cols],
                    equationT=current_model_func_name,
                    P=P_input)
            else:  # Kspar-Liq mode
                temperature = calculate_fspar_liq_temp(
                    kspar_comps=df[kspar_cols], liq_comps=df[liq_cols],
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

        return results_df, "KsparLiq", "T_K", "P_kbar"

## Olivine-Spinel

    ## Sp-Ol functions

    def _build_ol_sp_temp_gui(self, parent_box):
        """Build GUI for Ol-Sp Thermometry"""
        # Models selection
        temp_model_box = gui.vBox(parent_box, "Models")
        self.ol_sp_temp_models_combo = gui.comboBox(
            temp_model_box, self, "ol_sp_temp_model_idx",
            items=[m[0] for m in MODELS_OL_SP_TEMP],
            callback=self._update_controls)

        # Pressure settings
        self.ol_sp_temp_pressure_box = gui.radioButtons(
            parent_box, self, "ol_sp_temp_pressure_type", box="Pressure Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.ol_sp_temp_pressure_box, "Dataset as Pressure (kbar)")

        rb_fixed_p = gui.appendRadioButton(self.ol_sp_temp_pressure_box, "Fixed Pressure")
        self.ol_sp_temp_pressure_value_box = gui.doubleSpin(
            gui.indentedBox(self.ol_sp_temp_pressure_box, gui.checkButtonOffsetHint(rb_fixed_p)), self,
            "ol_sp_temp_pressure_value", 1.0, 10000.0, step=0.1, label="Pressure Value (kbar)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=1)

        rb_model_p = gui.appendRadioButton(self.ol_sp_temp_pressure_box, "Model as Pressure")
        model_as_p_box = gui.indentedBox(self.ol_sp_temp_pressure_box, gui.checkButtonOffsetHint(rb_model_p))

        self.ol_sp_temp_barometer_model_box = gui.comboBox(
            model_as_p_box, self, "ol_sp_temp_barometer_model_idx",
            items=[m[0] for m in MODELS_OL_SP_PRESSURE],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.ol_sp_temp_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "ol_sp_temp_fixed_h2o", "Fixed H₂O", callback=self._update_controls)
        self.ol_sp_temp_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "ol_sp_temp_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)

    def _build_ol_sp_press_gui(self, parent_box):
        """Build GUI for Ol-Sp Barometry"""
        # Models selection
        press_model_box = gui.vBox(parent_box, "Models")
        self.ol_sp_press_models_combo = gui.comboBox(
            press_model_box, self, "ol_sp_press_model_idx",
            items=[m[0] for m in MODELS_OL_SP_PRESSURE],
            callback=self._update_controls)

        # Temperature settings
        self.ol_sp_press_temp_box = gui.radioButtons(
            parent_box, self, "ol_sp_press_temp_type", box="Temperature Input",
            callback=self._update_controls)
        gui.appendRadioButton(self.ol_sp_press_temp_box, "Dataset as Temperature (K)")

        rb_fixed_t = gui.appendRadioButton(self.ol_sp_press_temp_box, "Fixed Temperature")
        self.ol_sp_press_temp_value_box = gui.doubleSpin(
            gui.indentedBox(self.ol_sp_press_temp_box, gui.checkButtonOffsetHint(rb_fixed_t)), self,
            "ol_sp_press_temp_value", 500.0, 2000.0, step=1.0, label="Temperature Value (K)",
            alignment=Qt.AlignRight, callback=self._update_controls, controlWidth=80, decimals=0)

        rb_model_t = gui.appendRadioButton(self.ol_sp_press_temp_box, "Model as Temperature")
        model_as_t_box = gui.indentedBox(self.ol_sp_press_temp_box, gui.checkButtonOffsetHint(rb_model_t))

        self.ol_sp_press_thermometer_model_box = gui.comboBox(
            model_as_t_box, self, "ol_sp_press_thermometer_model_idx",
            items=[m[0] for m in MODELS_OL_SP_TEMP],
            callback=self._update_controls)

        # H2O settings
        h2o_box = gui.vBox(parent_box, "H₂O Settings")
        self.ol_sp_press_fixed_h2o_checkbox = gui.checkBox(
            h2o_box, self, "ol_sp_press_fixed_h2o", "Fixed H₂O", callback=self._update_controls)

        self.ol_sp_press_fixed_h2o_input = gui.lineEdit(
            h2o_box, self, "ol_sp_press_fixed_h2o_value_str", label="H₂O (wt%)",
            orientation=Qt.Horizontal, callback=self.commit.deferred)


    def _update_ol_sp_temp_controls(self):
        """Update controls for Ol-Sp Thermometry"""
        _, _, requires_pressure, requires_h2o = MODELS_OL_SP_TEMP[self.ol_sp_temp_model_idx]

        # Enable/disable pressure radio group
        self.ol_sp_temp_pressure_box.setEnabled(requires_pressure)

        # Enable/disable pressure value box
        self.ol_sp_temp_pressure_value_box.setEnabled(
            requires_pressure and self.ol_sp_temp_pressure_type == 1)

        # Enable/disable barometer model box
        self.ol_sp_temp_barometer_model_box.setEnabled(
            requires_pressure and self.ol_sp_temp_pressure_type == 2)

        # Enable/disable H2O input
        self.ol_sp_temp_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.ol_sp_temp_fixed_h2o_input.setEnabled(requires_h2o and self.ol_sp_temp_fixed_h2o)

    def _update_ol_sp_press_controls(self):
        """Update controls for Ol-Sp Barometry"""
        _, _, requires_temp, requires_h2o = MODELS_OL_SP_PRESSURE[self.ol_sp_press_model_idx]

        # Enable/disable temperature radio group
        self.ol_sp_press_temp_box.setEnabled(requires_temp)

        # Enable/disable temperature value box
        self.ol_sp_press_temp_value_box.setEnabled(
            requires_temp and self.ol_sp_press_temp_type == 1)

        # Enable/disable thermometer model box
        self.ol_sp_press_thermometer_model_box.setEnabled(
            requires_temp and self.ol_sp_press_temp_type == 2)

        # Enable/disable H2O input
        self.ol_sp_press_fixed_h2o_checkbox.setEnabled(requires_h2o)
        self.ol_sp_press_fixed_h2o_input.setEnabled(requires_h2o and self.ol_sp_press_fixed_h2o)



    def _calculate_ol_sp_press(self, df):
        """Calculate Ol-Sp pressures"""
        _, current_model_func_name, requires_temp, requires_h2o = MODELS_OL_SP_PRESSURE[self.ol_sp_press_model_idx]
        current_thermometer_func_name = MODELS_OL_SP_TEMP[self.ol_sp_press_thermometer_model_idx][1]

        df = dm.preprocessing(df, my_output='ol_sp')

        water = self._get_h2o_value(df, requires_h2o,
                                self.ol_sp_press_fixed_h2o,
                                self.ol_sp_press_fixed_h2o_value_str,
                                "Ol-Sp Barometry")
        if water is None:
            return pd.DataFrame(), "", "", ""

        T_input = self._get_temperature_value(df, requires_temp,
                                            self.ol_sp_press_temp_type,
                                            self.ol_sp_press_temp_value,
                                            "Ol-Sp Barometry")

        # Initialize results
        results_df = pd.DataFrame()

        if requires_temp and self.ol_sp_press_temp_type == 2:  # Model as Temperature
            try:
                calc = calculate_ol_sp_press_temp(
                    sp_comps=df[sp_cols],
                    ol_comps=df[ol_cols],
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
                pressure = calculate_ol_sp_press(
                    sp_comps=df[sp_cols],
                    ol_comps=df[ol_cols],
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

        return results_df, "OlSp", "T_K", "P_kbar"

    def _calculate_ol_sp_temp(self, df):
        """Encapsulates the Ol-Sp Thermometry calculation logic."""
        _, current_model_func_name, requires_pressure_by_model, requires_h2o_by_model = MODELS_OL_SP_TEMP[self.ol_sp_temp_model_idx]
        current_barometer_func_name = MODELS_OL_SP_PRESSURE[self.ol_sp_temp_barometer_model_idx][1]

        df = dm.preprocessing(df, my_output='ol_sp')

        water = self._get_h2o_value(df, requires_h2o_by_model,
                                    self.ol_sp_temp_fixed_h2o,
                                    self.ol_sp_temp_fixed_h2o_value_str,
                                    "Ol-Sp Thermometry")
        if water is None: return pd.DataFrame(), "", "", "" # Error occurred in H2O fetching

        P_input = self._get_pressure_value(df, requires_pressure_by_model,
                                           self.ol_sp_temp_pressure_type,
                                           self.ol_sp_temp_pressure_value,
                                           "Ol-Sp Thermometry")

        temperature = None
        pressure_output = None # This is for when pressure is calculated iteratively with temp

        if requires_pressure_by_model and self.ol_sp_temp_pressure_type == 2: # Model as Pressure
            calc = calculate_ol_sp_press_temp(
                sp_comps=df[sp_cols], ol_comps=df[ol_cols],
                equationT=current_model_func_name, equationP=current_barometer_func_name)
            temperature = calc['T_K_calc']
            pressure_output = calc['P_kbar_calc']
        else: # No pressure, fixed, or dataset pressure
            temperature = calculate_ol_sp_temp(
                sp_comps=df[sp_cols], ol_comps=df[ol_cols],
                equationT=current_model_func_name, P=P_input)


        results_df = pd.DataFrame()
        results_df['T_K_calc'] = temperature

        if pressure_output is not None:
            results_df['P_kbar_calc'] = pressure_output
        elif P_input is not None:
            results_df['P_kbar_input'] = P_input # Store the input pressure if used
        else:
            results_df['P_kbar_input'] = np.full(len(df), np.nan) # Placeholder if no P input

        return results_df, "OlSp", "T_K", "P_kbar"


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
        self.liq_ol_temp_box.setVisible(False)
        self.liq_ol_press_box.setVisible(False)
        self.plag_kspar_temp_box.setVisible(False)
        self.plag_kspar_press_box.setVisible(False)
        self.plag_liq_temp_box.setVisible(False)
        self.plag_liq_press_box.setVisible(False)
        self.kspar_liq_temp_box.setVisible(False)
        self.kspar_liq_press_box.setVisible(False)
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

# Liq

        elif self.calculation_type == 9:  # Liq-Ol/Liq-only Thermometry
            self.liq_ol_temp_box.setVisible(True)

            # Add Liq thermometry model update (similar to Opx)
            if hasattr(self, 'liq_thermometry_mode'):
                if self.liq_thermometry_mode == 0:  # Liq-Ol mode
                    models = MODELS_LIQ_OL_TEMPERATURE
                else:  # Liq-only mode
                    models = MODELS_LIQ_ONLY_TEMPERATURE

                current_idx = self.liq_ol_temp_model_idx
                self.liq_ol_temp_models_combo.blockSignals(True)
                self.liq_ol_temp_models_combo.clear()
                self.liq_ol_temp_models_combo.addItems([m[0] for m in models])

                if current_idx < len(models):
                    self.liq_ol_temp_model_idx = current_idx
                else:
                    self.liq_ol_temp_model_idx = 0

                self.liq_ol_temp_models_combo.blockSignals(False)

            self._update_liq_ol_temp_controls()


        if self.calculation_type == 10:  # Cpx-Opx Thermometry
            self.plag_kspar_temp_box.setVisible(True)
            self._update_plag_kspar_temp_controls()

        elif self.calculation_type == 11:  # Plag-Liq/Plag-only Thermometry
            self.plag_liq_temp_box.setVisible(True)

            # Add Plag thermometry model update (similar to Opx)
            if hasattr(self, 'plag_thermometry_mode'):
                if self.plag_thermometry_mode == 0:  # Plag-Liq mode
                    models = MODELS_PLAG_LIQ_TEMPERATURE
                else:  # Plag-only mode
                    models = MODELS_PLAG_ONLY_TEMPERATURE

                current_idx = self.plag_liq_temp_model_idx
                self.plag_liq_temp_models_combo.blockSignals(True)
                self.plag_liq_temp_models_combo.clear()
                self.plag_liq_temp_models_combo.addItems([m[0] for m in models])

                if current_idx < len(models):
                    self.plag_liq_temp_model_idx = current_idx
                else:
                    self.plag_liq_temp_model_idx = 0

                self.plag_liq_temp_models_combo.blockSignals(False)

            self._update_plag_liq_temp_controls()

        elif self.calculation_type == 12:  # Plag-Liq/Plag-only Barometry
            self.plag_liq_press_box.setVisible(True)

            # Add Plag barometry model update (similar to Opx)
            if hasattr(self, 'plag_barometry_mode'):
                if self.plag_barometry_mode == 0:  # Plag-Liq mode
                    models = MODELS_PLAG_LIQ_PRESSURE
                else:  # Plag-only mode
                    models = MODELS_PLAG_ONLY_PRESSURE

                current_idx = self.plag_liq_press_model_idx
                self.plag_liq_press_models_combo.blockSignals(True)
                self.plag_liq_press_models_combo.clear()
                self.plag_liq_press_models_combo.addItems([m[0] for m in models])

                if current_idx < len(models):
                    self.plag_liq_press_model_idx = current_idx
                else:
                    self.plag_liq_press_model_idx = 0

                self.plag_liq_press_models_combo.blockSignals(False)

            self._update_plag_liq_press_controls()

        elif self.calculation_type == 13:  # Kspar-Liq/Kspar-only Thermometry
            self.kspar_liq_temp_box.setVisible(True)

            # Add Kspar thermometry model update (similar to Opx)
            if hasattr(self, 'kspar_thermometry_mode'):
                if self.kspar_thermometry_mode == 0:  # Kspar-Liq mode
                    models = MODELS_KSPAR_LIQ_TEMPERATURE
                else:  # Kspar-only mode
                    models = MODELS_KSPAR_ONLY_TEMPERATURE

                current_idx = self.kspar_liq_temp_model_idx
                self.kspar_liq_temp_models_combo.blockSignals(True)
                self.kspar_liq_temp_models_combo.clear()
                self.kspar_liq_temp_models_combo.addItems([m[0] for m in models])

                if current_idx < len(models):
                    self.kspar_liq_temp_model_idx = current_idx
                else:
                    self.kspar_liq_temp_model_idx = 0

                self.kspar_liq_temp_models_combo.blockSignals(False)

            self._update_kspar_liq_temp_controls()

        elif self.calculation_type == 14:  # Ol-Spinel Thermometry
            self.ol_sp_temp_box.setVisible(True)
            self._update_ol_sp_temp_controls()



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

        elif self.calculation_type == 9:  # Liq-ol Thermometry
            print('Made it into line 2399')
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_liq_ol_temp(df.copy())
                print(result_df)
            except Exception as e:
                self.Error.value_error(f"Error in Liq-only Thermometry: {e}")
                self.Outputs.data.send(None)
                return

        # elif self.calculation_type == 10:  # Liq-ol Barometry
        #     try:
        #         result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_liq_ol_press(df.copy())
        #     except Exception as e:
        #         self.Error.value_error(f"Error in Liq-Ol Barometry: {e}")
        #         self.Outputs.data.send(None)
        #         return


        if self.calculation_type == 10:  # Plag-Kspar Thermometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_plag_kspar_temp(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Plag-Kspar Thermometry: {e}")
                self.Outputs.data.send(None)
                return

        # elif self.calculation_type == 2:  # Plag-Kspar Barometry
        #     try:
        #         result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_plag_kspar_press(df.copy())
        #     except Exception as e:
        #         self.Error.value_error(f"Error in Plag-Kspar Barometry: {e}")
        #         self.Outputs.data.send(None)
        #         return

        elif self.calculation_type == 11:  # Plag-Liq Thermometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_plag_liq_temp(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Plag-Liq Thermometry: {e}")
                self.Outputs.data.send(None)
                return

        elif self.calculation_type == 12:  # Plag-Liq Barometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_plag_liq_press(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Plag-Liq Barometry: {e}")
                self.Outputs.data.send(None)
                return

        elif self.calculation_type == 13:  # Kspar-Liq Thermometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_kspar_liq_temp(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Kspar-Liq Thermometry: {e}")
                self.Outputs.data.send(None)
                return

        elif self.calculation_type == 14:  # Ol-Sp Thermometry
            try:
                result_df, prefix, temp_col_name_suffix, press_col_name_suffix = self._calculate_ol_sp_temp(df.copy())
            except Exception as e:
                self.Error.value_error(f"Error in Ol-Sp Thermometry: {e}")
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
import numpy as np
import pandas as pd
from Thermobar.core import *

def preprocessing(my_input, my_output='cpx_liq', sample_label=None, GEOROC=False, suffix=None):
    
        ## This specifies the default order for each dataframe type used in calculations
    df_ideal_liq = pd.DataFrame(columns=['SiO2_Liq', 'TiO2_Liq', 'Al2O3_Liq',
    'FeOt_Liq', 'MnO_Liq', 'MgO_Liq', 'CaO_Liq', 'Na2O_Liq', 'K2O_Liq',
    'Cr2O3_Liq', 'P2O5_Liq', 'H2O_Liq', 'Fe3Fet_Liq', 'NiO_Liq', 'CoO_Liq',
     'CO2_Liq'])
    
    df_ideal_cpx = pd.DataFrame(columns=['SiO2_Cpx', 'TiO2_Cpx', 'Al2O3_Cpx',
    'FeOt_Cpx','MnO_Cpx', 'MgO_Cpx', 'CaO_Cpx', 'Na2O_Cpx', 'K2O_Cpx',
    'Cr2O3_Cpx'])
    
    df_ideal_exp = pd.DataFrame(columns=['P_kbar', 'T_K'])

    if any(my_input.columns.str.startswith(' ')):
        w.warn('your input file has some columns that start with spaces. This could cause you big problems if they are at the start of oxide names. Please ammend your file and reload.')
    if suffix is not None:
        if any(my_input.columns.str.contains(suffix)):
            w.warn('We notice you have specified a suffix, but some of your columns already have this suffix. '
        'e.g., If you already have _Liq in the file, you shouldnt specify suffix="_Liq" during the import')


    my_input_c = my_input.copy()
    if suffix is not None:
        my_input_c=my_input_c.add_suffix(suffix)

    if any(my_input.columns.str.contains("_cpx")):
        w.warn("You've got a column heading with a lower case _cpx, this is okay if this column is for your"
        " own use, but if its an input to Thermobar, it needs to be capitalized (_Cpx)" )

    if any(my_input.columns.str.contains("_liq")):
        w.warn("You've got a column heading with a lower case _liq, this is okay if this column is for your"
        " own use, but if its an input to Thermobar, it needs to be capitalized (_Liq)" )

    if suffix is not None:
        if any(my_input.columns.str.contains("FeO")) and (all(my_input.columns.str.contains("FeOt")==False)):
            raise ValueError("No FeOt found. You've got a column heading with FeO. To avoid errors based on common EPMA outputs"
            " thermobar only recognises columns with FeOt for all phases except liquid"
            " where you can also enter a Fe3Fet_Liq heading used for equilibrium tests")

    if any(my_input.columns.str.contains("FeO_")) and (all(my_input.columns.str.contains("FeOt_")==False)):

        if any(my_input.columns.str.contains("FeO_Liq")) and any(my_input.columns.str.contains("Fe2O3_Liq")):
            my_input_c['FeOt_Liq']=my_input_c['FeO_Liq']+my_input_c['Fe2O3_Liq']*0.89998


        else:
            raise ValueError("No FeOt found. You've got a column heading with FeO. To avoid errors based on common EPMA outputs"
        " thermobar only recognises columns with FeOt for all phases except liquid"
        " where you can also enter a Fe3Fet_Liq heading used for equilibrium tests")

    if any(my_input.columns.str.contains("FeOT_")) and (all(my_input.columns.str.contains("FeOt_")==False)):
        raise ValueError("No FeOt column found. You've got a column heading with FeOT. Change to a lower case t")



    #   myLabels=my_input.Sample_ID

    Experimental_press_temp1 = my_input.reindex(df_ideal_exp.columns, axis=1)
    # This deals with the fact almost everyone will enter as FeO, but the code uses FeOt for these minerals.
    # E.g., if users only enter FeO (not FeOt and Fe2O3), allocates a FeOt
    # column. If enter FeO and Fe2O3, put a FeOt column



    myLiquids1 = my_input_c.reindex(df_ideal_liq.columns, axis=1).fillna(0)
    myLiquids1 = myLiquids1.apply(pd.to_numeric, errors='coerce').fillna(0)
    myLiquids1[myLiquids1 < 0] = 0

    myCPXs1 = my_input_c.reindex(df_ideal_cpx.columns, axis=1).fillna(0)
    myCPXs1 = myCPXs1.apply(pd.to_numeric, errors='coerce').fillna(0)
    myCPXs1[myCPXs1 < 0] = 0


    if my_output == 'cpx_only':       
        output = myCPXs1
    elif my_output == 'liq_only':
        output = myLiquids1
    elif my_output == 'cpx_liq':
        output = pd.concat([myCPXs1, myLiquids1], axis=1)

    # Maintain all columns
    my_input_filt = my_input[[col for col in my_input.columns if col not in output.columns]]
    output_merged = pd.concat([output, my_input_filt], axis=1)


    return output_merged
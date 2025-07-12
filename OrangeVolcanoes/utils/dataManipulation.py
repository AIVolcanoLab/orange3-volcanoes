import numpy as np
import pandas as pd
from Thermobar.core import *

def preprocessing(my_input, my_output='cpx_liq', sample_label=None, GEOROC=False, suffix=None):

        ## This specifies the default order for each dataframe type used in calculations


    df_ideal_liq = pd.DataFrame(columns=['SiO2_Liq', 'TiO2_Liq', 'Al2O3_Liq',
    'FeOt_Liq', 'MnO_Liq', 'MgO_Liq', 'CaO_Liq', 'Na2O_Liq', 'K2O_Liq',
    'Cr2O3_Liq', 'P2O5_Liq', 'H2O_Liq', 'Fe3Fet_Liq', 'NiO_Liq', 'CoO_Liq',
    'CO2_Liq'])

    df_ideal_oxide = pd.DataFrame(columns=['SiO2', 'TiO2', 'Al2O3',
    'FeOt', 'MnO', 'MgO', 'CaO', 'Na2O', 'K2O',
    'Cr2O3', 'P2O5'])

    df_ideal_cpx = pd.DataFrame(columns=['SiO2_Cpx', 'TiO2_Cpx', 'Al2O3_Cpx',
    'FeOt_Cpx','MnO_Cpx', 'MgO_Cpx', 'CaO_Cpx', 'Na2O_Cpx', 'K2O_Cpx',
    'Cr2O3_Cpx'])

    df_ideal_ol = pd.DataFrame(columns=['SiO2_Ol', 'TiO2_Ol', 'Al2O3_Ol',
    'FeOt_Ol', 'MnO_Ol', 'MgO_Ol', 'CaO_Ol', 'Na2O_Ol', 'K2O_Ol', 'Cr2O3_Ol',
    'NiO_Ol'])

    df_ideal_gt = pd.DataFrame(columns=['SiO2_Gt', 'TiO2_Gt', 'Al2O3_Gt',
    'Cr2O3_Gt', 'FeOt_Gt', 'MnO_Gt', 'MgO_Gt', 'CaO_Gt', 'Na2O_Gt', 'K2O_Gt',
    'Ni_Gt', 'Ti_Gt', 'Zr_Gt', 'Zn_Gt', 'Ga_Gt', 'Sr_Gt', 'Y_Gt'])

    df_ideal_sp = pd.DataFrame(columns=['SiO2_Sp', 'TiO2_Sp', 'Al2O3_Sp',
    'FeOt_Sp', 'MnO_Sp', 'MgO_Sp', 'CaO_Sp', 'Na2O_Sp', 'K2O_Sp', 'Cr2O3_Sp',
    'NiO_Sp'])

    df_ideal_opx = pd.DataFrame(columns=['SiO2_Opx', 'TiO2_Opx', 'Al2O3_Opx',
    'FeOt_Opx', 'MnO_Opx', 'MgO_Opx', 'CaO_Opx', 'Na2O_Opx', 'K2O_Opx',
    'Cr2O3_Opx'])

    df_ideal_plag = pd.DataFrame(columns=['SiO2_Plag', 'TiO2_Plag', 'Al2O3_Plag',
    'FeOt_Plag', 'MnO_Plag', 'MgO_Plag', 'CaO_Plag', 'Na2O_Plag', 'K2O_Plag',
    'Cr2O3_Plag'])

    df_ideal_kspar = pd.DataFrame(columns=['SiO2_Kspar', 'TiO2_Kspar',
    'Al2O3_Kspar', 'FeOt_Kspar','MnO_Kspar', 'MgO_Kspar', 'CaO_Kspar',
    'Na2O_Kspar', 'K2O_Kspar', 'Cr2O3_Kspar'])

    df_ideal_amp = pd.DataFrame(columns=['SiO2_Amp', 'TiO2_Amp', 'Al2O3_Amp',
    'FeOt_Amp', 'MnO_Amp', 'MgO_Amp', 'CaO_Amp', 'Na2O_Amp', 'K2O_Amp',
    'Cr2O3_Amp', 'F_Amp', 'Cl_Amp'])


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

    if any(my_input.columns.str.contains("_opx")):
        w.warn("You've got a column heading with a lower case _opx, this is okay if this column is for your"
        " own use, but if its an input to Thermobar, it needs to be capitalized (_Opx)" )


    if any(my_input.columns.str.contains("_liq")):
        w.warn("You've got a column heading with a lower case _liq, this is okay if this column is for your"
        " own use, but if its an input to Thermobar, it needs to be capitalized (_Liq)" )

    if any(my_input.columns.str.contains("_amp")):
        w.warn("You've got a column heading with a lower case _amp, this is okay if this column is for your"
        " own use, but if its an input to Thermobar, it needs to be capitalized (_Amp)" )

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



    myOxides1 = my_input_c.reindex(df_ideal_oxide.columns, axis=1).fillna(0)
    myOxides1 = myOxides1.apply(pd.to_numeric, errors='coerce').fillna(0)
    myOxides1[myOxides1 < 0] = 0

    myLiquids1 = my_input_c.reindex(df_ideal_liq.columns, axis=1).fillna(0)
    myLiquids1 = myLiquids1.apply(pd.to_numeric, errors='coerce').fillna(0)
    myLiquids1[myLiquids1 < 0] = 0

    myCPXs1 = my_input_c.reindex(df_ideal_cpx.columns, axis=1).fillna(0)
    myCPXs1 = myCPXs1.apply(pd.to_numeric, errors='coerce').fillna(0)
    myCPXs1[myCPXs1 < 0] = 0

    myOls1 = my_input_c.reindex(df_ideal_ol.columns, axis=1).fillna(0)
    myOls1 = myOls1.apply(pd.to_numeric, errors='coerce').fillna(0)
    myOls1[myOls1 < 0] = 0

    myPlags1 = my_input_c.reindex(df_ideal_plag.columns, axis=1).fillna(0)
    myPlags1 = myPlags1.apply(pd.to_numeric, errors='coerce').fillna(0)
    myPlags1[myPlags1 < 0] = 0

    myKspars1 = my_input_c.reindex(df_ideal_kspar.columns, axis=1).fillna(0)
    myKspars1 = myKspars1.apply(pd.to_numeric, errors='coerce').fillna(0)
    myKspars1[myKspars1 < 0] = 0

    myOPXs1 = my_input_c.reindex(df_ideal_opx.columns, axis=1).fillna(0)
    myOPXs1 = myOPXs1.apply(pd.to_numeric, errors='coerce').fillna(0)
    myOPXs1[myOPXs1 < 0] = 0

    mySps1 = my_input_c.reindex(df_ideal_sp.columns, axis=1).fillna(0)
    mySps1 = mySps1.apply(pd.to_numeric, errors='coerce').fillna(0)
    mySps1[mySps1 < 0] = 0

    myAmphs1 = my_input_c.reindex(df_ideal_amp.columns, axis=1).fillna(0)
    myAmphs1 = myAmphs1.apply(pd.to_numeric, errors='coerce').fillna(0)
    myAmphs1[myAmphs1 < 0] = 0

    myGts1 = my_input_c.reindex(df_ideal_gt.columns, axis=1).fillna(0)
    myGts1 = myGts1.apply(pd.to_numeric, errors='coerce').fillna(0)
    myGts1[myGts1 < 0] = 0


    if my_output == 'cpx_only':
        output = myCPXs1

    elif my_output == 'cpx_liq':
        output = pd.concat([myCPXs1, myLiquids1], axis=1)

    if my_output == 'amp_only':
        output = myAMPs1

    elif my_output == 'amp_liq':
        output = pd.concat([myAMPs1, myLiquids1], axis=1)


    elif my_output == 'opx_only':
        output = myOPXs1

    elif my_output == 'liq_only':
        output = myLiquids1

    elif my_output == 'opx_liq':
        output = pd.concat([myOPXs1, myLiquids1], axis=1)

    elif my_output == 'liq_ol':
        output = pd.concat([myLiquids1, myOls1], axis=1)

    elif my_output=='plag_kspar':
        output = pd.concat([myPlags1, myKspars1], axis=1)

    elif my_output == 'plag_liq':
        output = pd.concat([myPlags1, myLiquids1], axis=1)
    elif my_output == 'kspar_liq':
        output = pd.concat([myKspars1, myLiquids1], axis=1)
    elif my_output == 'cpx_opx':
        output = pd.concat([myCPXs1, myOPXs1], axis=1)
    elif my_output == 'ol_sp':
        output = pd.concat([myOls1, mySps1], axis=1)

    # Maintain all columns
    my_input_filt = my_input[[col for col in my_input.columns if col not in output.columns]]
    output_merged = pd.concat([output, my_input_filt], axis=1)


    return output_merged
'''constants for vis-script for GGI-Climate Finance project'''

BAR_TECH_COLOR_DICT = {
    'BIO':'darkgreen',
    'CCG':'brown',
    'CCS': 'khaki',
    'COA':'black',
    #'COG':'peru',
    #'CSP':'wheat',
    'GEO':'red',
    'HYD':'blue',
    'OCG':'lightsalmon',
    'OIL':'lightgrey',
    #'OTH':'teal',
    #'PET':'grey',
    'SPV':'gold',
    'URN':'limegreen',
    'WAS':'darkkhaki',
    #'WAV':'red',
    'WOF':'violet',
    'WON':'blueviolet',
    'SDS': 'aqua',
}

STORAGE_LIST = ['SDS']

BAR_GEN_SHARES_COLOR_DICT = {
    'Fossil':'lightcoral',
    'Renewable':'palegreen',
    'Other' : 'lightgrey',
}

DUAL_COSTS_COLOR_DICT = {
    'bar':'cadetblue',
    'line':'lightcoral',
}

DUAL_EMISSIONS_COLOR_DICT = {
    'bar':'navy',
    'line':'lightcoral',
}

DUAL_TRANSMISSION_COLOR_DICT = {
    'new' : 'maroon',
    'max' : 'aqua',
}

COUNTRY_COLOR_DICT = {
    # ASEAN
    'BRN' : 'lightgrey', 
    'IDN' : 'lightcoral',
    'KHM' : 'black', 
    'LAO' : 'peru', 
    'MMR' : 'dodgerblue', 
    'MYS' : 'darkgreen', 
    'PHL' : 'indigo', 
    'SGP' : 'firebrick', 
    'THA' : 'violet', 
    'VNM' : 'gold',
    
    #ZiZaBoNa
    'AGO' : 'limegreen', 
    'BWA' : 'black',
    'COD' : 'firebrick', 
    'SWZ' : 'lightgrey', 
    'LSO' : 'dodgerblue', 
    'MOZ' : 'blue',
    'MWI' : 'darkgreen', 
    'NAM' : 'lightcoral', 
    'ZAF' : 'indigo', 
    'TZA' : 'violet', 
    'ZMB' : 'gold',
    'ZWE' : 'red'
    }
    
SENSITIVTIES_COLOR_DICT = {
    'Base' : 'navy',
    'CoalPhaseOut' : 'limegreen',
    'LowTransmissionCosts' : 'lightgrey',
    'LongDurationStorage' : 'aqua',
    'HighGasPrice' : 'green',
    'NoNuclear' : 'orange',
    'PointTargets' : 'red',
    'NoTargets' : 'violet'
    
    
    
    }

SENSITIVTIES_HATCH_DICT = {
    'Base' : ['', 'black'],
    'CoalPhaseOut' : ['...', 'black'],
    #'LowTransmissionCosts' : ['///', 'black'],
    #'LongDurationStorage' : ['', 'blue'],
    #'HighGasPrice' : ['...', 'blue'],
    'NoNuclear' : ['///', 'black'],
    'NoTargets' : ['ooo', 'black'],
    'PointTargets' : ['\\\\\\', 'black']
    }
import pandas as pd

def get_years(start: int, end: int) -> range:
    return range(start, end + 1)

def convert_pj_to_twh(df):
    df['VALUE'] = df['VALUE'] / 3.6
    
    return df

def convert_million_to_billion(df):
    df['VALUE'] = df['VALUE'] / 1000
    
    return df

def format_technology_col(df):
    
    df = df.loc[(df['TECHNOLOGY'].str.startswith('PWR')) & 
                ~(df['TECHNOLOGY'].str.contains('TRN'))
    ].copy()
    
    df['TECH'] = df['TECHNOLOGY'].str[3:6]
    df['COUNTRY'] = df['TECHNOLOGY'].str[6:9]
    
    df = df.groupby(['TECH', 'COUNTRY', 'YEAR'])[
        'VALUE'].sum().reset_index(drop = False)
    
    return df

def format_annual_emissions(df, country : bool):
    df['COUNTRY'] = df['EMISSION'].str[3:6]
    
    if not country:
        df = df.groupby(['YEAR'])[
            'VALUE'].sum().reset_index(drop = False)
        
    else:
        df = df[['COUNTRY', 'YEAR', 'VALUE']]
    
    return df

def calculate_results_delta(df1, df2, cols : list, scenario):
    
    df1 = df1.groupby(cols)['VALUE'].sum().reset_index(
        drop = False).set_index(cols).rename(columns = {'VALUE' : 'Base'})
        
    df2 = df2.groupby(cols)['VALUE'].sum().reset_index(
        drop = False).set_index(cols).rename(columns = {'VALUE' : scenario})

    df = pd.merge(df1, df2, left_index = True, 
                  right_index = True, how = 'outer').fillna(0)
    
    df['DELTA'] = round(df[scenario] - df['Base'], 3)
    df = df.loc[df['DELTA'] != 0]
    
    return df
import pandas as pd

def get_years(start: int, end: int) -> range:
    return range(start, end + 1)

def convert_pj_to_twh(df):
    df['VALUE'] = df['VALUE'] / 3.6
    
    return df

def convert_million_to_billion(df):
    df['VALUE'] = df['VALUE'] / 1000
    
    return df

def format_technology_col(df, node : bool):
    
    df = df.loc[(df['TECHNOLOGY'].str.startswith('PWR')) & 
                ~(df['TECHNOLOGY'].str.contains('TRN'))
    ].copy()
    
    df['TECH'] = df['TECHNOLOGY'].str[3:6]
    
    if not node:
        df['COUNTRY'] = df['TECHNOLOGY'].str[6:9]
        df = df.groupby(['TECH', 'COUNTRY', 'YEAR'])[
            'VALUE'].sum().reset_index(drop = False)
        
    else:
        df['NODE'] = df['TECHNOLOGY'].str[6:11]
        df = df.groupby(['TECH', 'NODE', 'YEAR'])[
            'VALUE'].sum().reset_index(drop = False)
    
    return df

def get_node_list(df):
    df = df.loc[(df['TECHNOLOGY'].str.startswith('PWR'))
                ].replace({'01' : ''}, regex = True)
    
    df = sorted(list(df['TECHNOLOGY'].str.strip().str[-5:].unique()))
    
    return df

def format_annual_emissions(df, country : bool):
    df['COUNTRY'] = df['EMISSION'].str[3:6]
    
    if not country:
        df = df.groupby(['YEAR'])[
            'VALUE'].sum().reset_index(drop = False)
        
    else:
        df = df[['COUNTRY', 'YEAR', 'VALUE']]
    
    return df

def calculate_power_costs(df1, df2, storage_list):
    df2 = df2.loc[~df2['TECH'].isin(storage_list)]
    df2 = df2.groupby(['YEAR'])[
        'VALUE'].sum().reset_index(drop = False)
    
    df2['VALUE'] = df1['VALUE'] / df2['VALUE']

    return df2
    

def calculate_results_delta(df1, df2, cols : list, scenario, 
                            nodal_results,  node : bool):

    if node:
        '''Only keep nodal level values for required countries.'''
        for df in [df1, df2]:
            data = df.loc[~df['NODE'].str.startswith(
                tuple(nodal_results.get(scenario)))]
            data.loc[:, 'NODE'] = data['NODE'].str[:3] + 'XX'
            df.update(data)
    
    df1 = df1.groupby(cols)['VALUE'].sum().reset_index(
        drop = False).set_index(cols).rename(columns = {'VALUE' : 'Base'})
        
    df2 = df2.groupby(cols)['VALUE'].sum().reset_index(
        drop = False).set_index(cols).rename(columns = {'VALUE' : scenario})

    df = pd.merge(df1, df2, left_index = True, 
                  right_index = True, how = 'outer').fillna(0)
    
    df['DELTA'] = round(df[scenario] - df['Base'], 2)
    df = df.loc[df['DELTA'] != 0]

    return df

def geo_filter_tech_emissions(df, scenario):
    
    geo1, geo2 = scenario[:5], scenario[5:]
    if geo1[:3] == geo2[:3]:
        df = df[df['TECHNOLOGY'].str.contains(f'{geo1}|{geo2}')]
        
    else:
        df = df[df['EMISSION'].str.contains(f'{geo1[:3]}|{geo2[:3]}')]
    
    return df[['REGION', 'EMISSION', 'YEAR', 'VALUE']]

def make_space_above(axes, topmargin=1):
    """ increase figure size to make topmargin (in inches) space for 
        titles, without changing the axes sizes"""
    fig = axes.flatten()[0].figure
    s = fig.subplotpars
    w, h = fig.get_size_inches()

    figh = h - (1-s.top)*h  + topmargin
    fig.subplots_adjust(bottom=s.bottom*h/figh, top=1-topmargin/figh)
    fig.set_figheight(figh)
    
def plot_is_empty(ax):
    contained_artists = ax.get_children()
    return len(contained_artists) <= 1
'''Functions as input to visualisations'''
import os
from matplotlib import pyplot as plt
import numpy as np

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

def format_stacked_bar_pwr(df, out_dir, chart_title, 
                           legend_title, file_name, 
                           color_dict, unit, 
                           country):
    
    if country:
        df = df.loc[df['COUNTRY'] == country]
        chart_title = f'{country} {chart_title}'
        path = os.path.join(out_dir, country)
        
    else:
        path = out_dir

    df = df.groupby(['YEAR', 'TECH'])['VALUE'].sum().unstack().fillna(0)
    
    fig, ax = plt.subplots()

    # Initialize the bottom at zero for the first set of bars.
    bottom = np.zeros(len(df))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(df.columns):
      ax.bar(df.index, df[col], bottom=bottom, 
             label=col, color = color_dict.get(col))
      bottom += np.array(df[col])
    
    ax.set_title(chart_title)
    ax.set_ylabel(unit)
    ax.legend(bbox_to_anchor=(1, 1.02), frameon = False, 
              reverse = True, title = legend_title)
    
    ax.margins(x=0)
    if country:
        plt.close(fig)

    return fig.savefig(os.path.join(path, file_name), bbox_inches = 'tight')

def format_stacked_bar_gen_shares(df, out_dir, chart_title, 
                                  legend_title, file_name, 
                                  color_dict, unit, 
                                  country):
    
    if country:
        df = df.loc[df['COUNTRY'] == country].reset_index()
        chart_title = f'{country} {chart_title}'
        path = os.path.join(out_dir, country)
        
    else:
        path = out_dir
    
    df['OTHER'] = 100 - df['RENEWABLE'] - df['FOSSIL']
    df = df[['YEAR', 'RENEWABLE', 'FOSSIL', 'OTHER']].groupby(['YEAR']).sum()
    
    fig, ax = plt.subplots()

    # Initialize the bottom at zero for the first set of bars.
    bottom = np.zeros(len(df))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(df.columns):
      ax.bar(df.index, df[col], bottom=bottom, 
             label=col, color = color_dict.get(col))
      bottom += np.array(df[col])
    
    ax.set_title(chart_title)
    ax.set_ylabel(unit)
    ax.legend(bbox_to_anchor=(1, 1.02), frameon = False, 
              reverse = True, title = legend_title)
    
    ax.margins(x=0)
    if country:
        plt.close(fig)

    return fig.savefig(os.path.join(path, file_name), bbox_inches = 'tight')

def format_bar_line_costs(df1, df2, out_dir, chart_title, 
                          legend_title, file_name, 
                          color_dict, unit1, 
                          unit2, country):
    
    if country:
        df1 = df1.loc[df1['COUNTRY'] == country][['YEAR', 'VALUE']]
        df2 = df2.loc[df2['COUNTRY'] == country][['YEAR', 'VALUE']]
        chart_title = f'{country} {chart_title}'
        path = os.path.join(out_dir, country)
        
    else:
        path = out_dir

    df1.set_index('YEAR', inplace = True)
    convert_million_to_billion(df1)
    df2.set_index('YEAR', inplace = True)
    
    fig, ax1 = plt.subplots()
    
    ax1.bar(df1.index, df1['VALUE'], label= unit1, 
           color = color_dict.get('bar'))
    
    ax2 = ax1.twinx()
    
    ax2.plot(df2.index, df2['VALUE'], label= unit2, 
             color = color_dict.get('line'))

    ax1.set_title(chart_title)
    ax1.set_ylabel(unit1)
    ax2.set_ylabel(unit2)
    ax1.legend(bbox_to_anchor=(1, 1.02), frameon = False, 
               title = legend_title)
    
    ax2.legend(bbox_to_anchor=(0.905, 0.95), frameon = False, 
               title = legend_title)
    
    ax1.margins(x=0)
    if country:
        plt.close(fig)

    return fig.savefig(os.path.join(path, file_name), bbox_inches = 'tight')

def format_line_multi_country(df, out_dir, chart_title, 
                              legend_title, file_name, 
                              color_dict, unit):

    chart_title = chart_title

    df = df.groupby(['YEAR', 'COUNTRY'])['VALUE'].sum().unstack().fillna(0)
    
    fig, ax = plt.subplots()
    
    for i, col in enumerate(df.columns):
        ax.plot(df.index, df[col], label = col, 
                 color = color_dict.get(col)
                 )

    ax.set_title(chart_title)
    ax.set_ylabel(unit)
    ax.legend(bbox_to_anchor=(1, 1.02), frameon = False, 
               title = legend_title)

    ax.margins(x=0)

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')

def format_bar_line_emissions(df1, df2, out_dir, chart_title, 
                              legend_title, file_name, 
                              color_dict, unit1, 
                              unit2, country):
    
    if country:
        df1 = df1.loc[df1['COUNTRY'] == country][['YEAR', 'VALUE']]
        df2 = df2.loc[df2['COUNTRY'] == country][['YEAR', 'VALUE']]
        chart_title = f'{country} {chart_title}'
        path = os.path.join(out_dir, country)
        
    else:
        path = out_dir

    df1.set_index('YEAR', inplace = True)
    df2.set_index('YEAR', inplace = True)
    
    fig, ax1 = plt.subplots()
    
    ax1.bar(df1.index, df1['VALUE'], label= unit1, 
           color = color_dict.get('bar'))
    
    ax2 = ax1.twinx()
    
    ax2.plot(df2.index, df2['VALUE'], label= unit2, 
             color = color_dict.get('line'))

    ax1.set_title(chart_title)
    ax1.set_ylabel(unit1)
    ax2.set_ylabel(unit2)
    ax1.legend(bbox_to_anchor=(0.95, 1.02), frameon = False, 
               title = legend_title)
    
    ax2.legend(bbox_to_anchor=(1, 0.95), frameon = False, 
               title = legend_title)
    
    ax1.margins(x=0)
    if country:
        plt.close(fig)

    return fig.savefig(os.path.join(path, file_name), bbox_inches = 'tight')

def format_stacked_bar_line_emissions(df1, df2, out_dir, chart_title, 
                                      legend_title, file_name, 
                                      color_dict, unit1, unit2):

    df1 = df1.groupby(['YEAR', 'COUNTRY'])['VALUE'].sum().unstack().fillna(0)
    df2.set_index('YEAR', inplace = True)
    
    fig, ax1 = plt.subplots()

    # Initialize the bottom at zero for the first set of bars.
    bottom = np.zeros(len(df1))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(df1.columns):
      ax1.bar(df1.index, df1[col], bottom=bottom, 
             label=col, color = color_dict.get(col))
      bottom += np.array(df1[col])
      
    ax2 = ax1.twinx()
    
    ax2.plot(df2.index, df2['VALUE'], label= unit2, 
             color = 'forestgreen')
    
    ax1.set_title(chart_title)
    ax1.set_ylabel(unit1)
    ax2.set_ylabel(unit2)
    ax1.legend(bbox_to_anchor=(1.03, -0.05), frameon = False, 
               ncols = 5, title = legend_title)
    
    ax2.legend(bbox_to_anchor=(1, 1), frameon = False, 
               title = legend_title)
    
    ax1.margins(x=0)

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')
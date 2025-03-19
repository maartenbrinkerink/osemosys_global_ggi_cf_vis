'''Functions as input to visualisations'''
import os
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
import math
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from typing import Dict
from matplotlib.gridspec import GridSpec

from utils import (
    get_years,
    make_space_above
    )

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
             label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom += np.array(df[col])
    
    ax.set_title(chart_title)
    ax.set_ylabel(unit)
    ax.legend(bbox_to_anchor=(1, 1.02), frameon = False, 
              reverse = True, title = legend_title)
    
    ax.margins(x=0)
    if country:
        plt.close(fig)

    return fig.savefig(os.path.join(path, file_name), bbox_inches = 'tight')

def format_stacked_bar_demand(df, out_dir, chart_title, 
                              legend_title, file_name, 
                              color_dict, unit):

    df['FUEL'] = df['FUEL'].str[:6].str[3:]
    
    
    df = df.groupby(['YEAR', 'FUEL'])['VALUE'].sum().unstack().fillna(0)

    fig, ax = plt.subplots()

    # Initialize the bottom at zero for the first set of bars.
    bottom = np.zeros(len(df))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(df.columns):
      ax.bar(df.index, df[col], bottom=bottom, 
             label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom += np.array(df[col])
    
    ax.set_title(chart_title)
    ax.set_ylabel(unit)
    ax.legend(bbox_to_anchor=(1, 1.02), frameon = False, 
              reverse = True, title = legend_title)
    
    ax.margins(x=0)

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')

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
             label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom += np.array(df[col])
    
    ax.set_title(chart_title)
    ax.set_ylabel(unit)
    ax.legend(bbox_to_anchor=(1, 1.02), frameon = False, 
              reverse = True, title = legend_title)
    
    ax.margins(x=0)
    if country:
        plt.close(fig)

    return fig.savefig(os.path.join(path, file_name), bbox_inches = 'tight')

def format_stacked_bar_gen_shares_delta(df_in1, df_in2, df_in3, df_in4, 
                                        out_dir, chart_title, legend_title, 
                                        file_name, color_dict, unit):
    
    # Calculate Delta's for timeseries (ts)
    df_in1['OTHER'] = 100 - df_in1['RENEWABLE'] - df_in1['FOSSIL']
    df_in1 = df_in1[['YEAR', 'RENEWABLE', 'FOSSIL', 'OTHER']].groupby(['YEAR']).sum()
    
    df_in2['OTHER'] = 100 - df_in2['RENEWABLE'] - df_in2['FOSSIL']
    df_in2 = df_in2[['YEAR', 'RENEWABLE', 'FOSSIL', 'OTHER']].groupby(['YEAR']).sum()
    
    df_ts_in = df_in2 - df_in1
    
    # Calculate Delta's for horizon (hz)
    for df in [df_in3, df_in4]:
        df['Metric'] = df['Metric'].replace({'Renewable energy share' : 'RENEWABLE',
                          'Fossil energy share' : 'FOSSIL'})

        df.set_index('Metric', inplace = True)
        df.drop(columns = ['Unit'], inplace = True)
        df.loc['OTHER'] = 100 - df.loc[df.index == 'RENEWABLE'
                                       ].iloc[0] - df.loc[df.index == 'FOSSIL'
                                                          ].iloc[0]
                                                          
    df_hz_in = df_in4 - df_in3
    df_hz_in = df_hz_in.transpose()[['RENEWABLE', 'FOSSIL', 'OTHER']]
    
    fig, axs = plt.subplots(1, 2, squeeze = False,
                            gridspec_kw = {'width_ratios' : [1, 10]})

    # SET TIMESERIES SUBPLOT
    df1 = df_ts_in.clip(upper = 0)
    df2 = df_ts_in.clip(lower = 0)

    # Initialize the bottom at zero for the first set of bars.
    bottom1 = np.zeros(len(df1))
    bottom2 = np.zeros(len(df2))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.

    for i, col in enumerate(df1.columns):
      axs[0, 1].bar(df1.index, df1[col], bottom=bottom1, 
             label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom1 += np.array(df1[col])
      
    for i, col in enumerate(df2.columns):
      axs[0, 1].bar(df2.index, df2[col], bottom=bottom2, 
                   color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom2 += np.array(df2[col])
      
    # SET HORIZON SUBPLOT
    df3 = df_hz_in.clip(upper = 0)
    df4 = df_hz_in.clip(lower = 0)
    
    # Initialize the bottom at zero for the first set of bars.
    bottom3 = np.zeros(len(df3))
    bottom4 = np.zeros(len(df4))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    
    for i, col in enumerate(df3.columns):
      axs[0, 0].bar('Total', df3[col], bottom=bottom3, 
                    color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom3 += np.array(df3[col])
      
    for i, col in enumerate(df4.columns):
      axs[0, 0].bar('Total', df4[col], bottom=bottom4, 
                    color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom4 += np.array(df4[col])
   
    fig.legend(bbox_to_anchor=(0.8, 0.05), frameon = False, 
              reverse = True, title = legend_title, ncols = 3)
    
    axs[0, 1].margins(x=0)
    axs[0, 0].margins(x=1)

    axs[0, 1].set_ylim([min(df1.sum(axis=1), default = 0) * 1.1, 
                       max(df2.sum(axis=1), default = 0) * 1.1])
    
    axs[0, 0].set_ylim([min(df3.sum(axis=1), default = 0) * 1.1, 
                       max(df4.sum(axis=1), default = 0) * 1.1])
    
    axs[0, 0].set_ylabel(unit)
    
    axs[0, 1].axhline(y=0, color='black', linestyle='-', linewidth = 0.1)
    axs[0, 0].axhline(y=0, color='black', linestyle='-', linewidth = 0.1)
    
    # Adjust subplot whitespace
    plt.subplots_adjust(wspace=0.3)
    
    # Add plot title
    if chart_title:
        make_space_above(axs, topmargin=0.3) 
        plt.suptitle(chart_title)

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')

def format_bar_line(df1, df2, out_dir, chart_title, 
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
           color = color_dict.get('bar'), edgecolor = 'black', linewidth = 0.3)
    
    ax2 = ax1.twinx()
    
    ax2.plot(df2.index, df2['VALUE'], label= unit2, 
             color = color_dict.get('line'))

    ax1.set_title(chart_title)
    ax1.set_ylabel(unit1)
    ax2.set_ylabel(unit2)
    ax1.legend(bbox_to_anchor=(0.5, -0.05), frameon = False, 
               title = legend_title)
    
    ax2.legend(bbox_to_anchor=(0.8, -0.05), frameon = False, 
               title = legend_title)
    
    ax1.margins(x=0)
    if country:
        plt.close(fig)

    return fig.savefig(os.path.join(path, file_name), bbox_inches = 'tight')

def format_bar_delta(df1, df2, out_dir, 
                     chart_title, legend_title, 
                     file_name, color_dict, 
                     unit, country):
    
    if country:
        df1 = df1.loc[df1['COUNTRY'] == country][['YEAR', 'VALUE']]
        df2 = df2.loc[df2['COUNTRY'] == country][['YEAR', 'VALUE']]

        chart_title = f'{country} {chart_title}'
        path = os.path.join(out_dir, country)
        
    else:
        path = out_dir

    df1.set_index('YEAR', inplace = True)
    df2.set_index('YEAR', inplace = True)
    
    # Calculate Delta by year
    df = df2[['VALUE']] - df1[['VALUE']]
    
    # Calculate model horizon Delta
    df3 = df.sum().fillna(0)
    
    fig, axs = plt.subplots(1, 2, squeeze = False,
                            gridspec_kw = {'width_ratios' : [1, 10]})
    
    axs[0, 1].bar(df.index, df['VALUE'], 
           color = color_dict.get('bar'), edgecolor = 'black', linewidth = 0.3)
    
    axs[0, 0].bar('Total', df3['VALUE'],
                 color = color_dict.get('bar'), edgecolor = 'black', linewidth = 0.3)
    
    axs[0, 1].margins(x=0)
    axs[0, 0].margins(x=1)
    
    axs[0, 1].axhline(y=0, color='black', linestyle='-', linewidth = 0.1)
    axs[0, 0].set_ylabel(unit)
    
    # Adjust subplot whitespace
    plt.subplots_adjust(wspace=0.3)
    
    # Add plot title
    if chart_title:
        make_space_above(axs, topmargin=0.3) 
        plt.suptitle(chart_title)
    
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

def format_line_emission_limit(df, out_dir, chart_title, 
                              legend_title, file_name, 
                              color_dict, unit):

    chart_title = chart_title
    
    df['EMISSION'] = df['EMISSION'].str.replace('CO2', '')
    df = df.groupby(['YEAR', 'EMISSION'])['VALUE'].sum().unstack().fillna(0)
    df1 = df.loc[:, df.le(100).all()]
    df2 = df.drop(columns = list(df1.columns))

    fig, axs = plt.subplots(1, 2, squeeze = False,
                            gridspec_kw = {'width_ratios' : [1, 1]},
                            figsize = (5, 3))
    
    for i, col in enumerate(df1.columns):
        axs[0, 1].plot(df1.index, df1[col], label = col, 
                 color = color_dict.get(col)
                 )    
    
    for i, col in enumerate(df2.columns):
        axs[0, 0].plot(df2.index, df2[col], label = col, 
                 color = color_dict.get(col)
                 )

    axs[0, 0].set_ylabel(unit)

    for i, ax in enumerate(fig.axes):
        ax.axhline(y=0, color='black', linestyle='-', linewidth = 0.1)
        ax.margins(x=0)
        ax.legend(bbox_to_anchor=(1.07, -0.1), frameon = False,
                  ncols = 2)

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')

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
             label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom += np.array(df1[col])
      
    ax2 = ax1.twinx()
    
    ax2.plot(df2.index, df2['VALUE'], label= unit2, 
             color = 'red')
    
    ax1.set_title(chart_title)
    ax1.set_ylabel(unit1)
    ax2.set_ylabel(unit2)
    ax1.legend(bbox_to_anchor=(1.03, -0.05), frameon = False, 
               ncols = 5, title = legend_title)
    
    ax2.legend(bbox_to_anchor=(1, 1), frameon = False, 
               title = legend_title)
    
    ax1.margins(x=0)

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')

def format_stacked_bar_pwr_delta(df_in1, df_in2, out_dir, 
                                 chart_title, legend_title, 
                                 file_name, color_dict, unit, 
                                 start_year, end_year):
    
    years = get_years(start_year, end_year)
    
    fig, axs = plt.subplots(1, 2, squeeze = False,
                            gridspec_kw = {'width_ratios' : [1, 10]})
    
    # SET TIMESERIES SUBPLOT
    
    df1 = df_in1.loc[df_in1['DELTA'] < 0]
    df2 = df_in1.loc[df_in1['DELTA'] > 0]

    df1 = df1.groupby(['YEAR', 'TECH'])['DELTA'].sum().unstack().fillna(0)
    df2 = df2.groupby(['YEAR', 'TECH'])['DELTA'].sum().unstack().fillna(0)

    for idx in years:
        if not df1.empty:
            if not idx in df1.index:
                df1.loc[idx] = 0
                
        if not df2.empty:            
            if not idx in df2.index:
                df2.loc[idx] = 0
            
    df1.sort_index(inplace = True)
    df2.sort_index(inplace = True)

    # Initialize the bottom at zero for the first set of bars.
    bottom1 = np.zeros(len(df1))
    bottom2 = np.zeros(len(df2))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(df1.columns):
      axs[0,1].bar(df1.index, df1[col], bottom=bottom1, 
             label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom1 += np.array(df1[col])
      
    for i, col in enumerate(df2.columns):
      axs[0,1].bar(df2.index, df2[col], bottom=bottom2, 
             label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom2 += np.array(df2[col])
    
    # Axis formatting
    axs[0,1].xaxis.set_major_formatter(FormatStrFormatter('%d'))
    axs[0,1].margins(x=0)
    axs[0,1].set_ylim([min(df1.sum(axis=1), default = 0) * 1.1, 
                       max(df2.sum(axis=1), default = 0) * 1.1])
    
    # SET TOTAL SUBPLOT
    
    df3 = df_in2.loc[df_in2['DELTA'] < 0]
    df4 = df_in2.loc[df_in2['DELTA'] > 0]

    df3 = df3.groupby(['TECH'])['DELTA'].sum().fillna(0)
    df4 = df4.groupby(['TECH'])['DELTA'].sum().fillna(0)
    
    for idx in df_in2.index:
        if not df3.empty:
            if not idx in df3.index:
                df3.loc[idx] = 0
         
        if not df4.empty:
            if not idx in df4.index:
                df4.loc[idx] = 0
    
    df3 = pd.DataFrame(df3.sort_index()).transpose()
    df4 = pd.DataFrame(df4.sort_index()).transpose()

    # Initialize the bottom at zero for the first set of bars.
    bottom3 = np.zeros(len(df3))
    bottom4 = np.zeros(len(df4))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(df3.columns):
      axs[0,0].bar('Total', df3[col], bottom=bottom3, 
             label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom3 += np.array(df3[col])
      
    for i, col in enumerate(df4.columns):
      axs[0,0].bar('Total', df4[col], bottom=bottom4, 
             label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom4 += np.array(df4[col])
    
    # Axis formatting
    axs[0,0].margins(x=1)
    axs[0,0].set_ylim([min(df3.sum(axis=1), default = 0) * 1.1, 
                       max(df4.sum(axis=1), default = 0) * 1.1])
    axs[0,0].set_ylabel(unit)
    
    # CONFIG BOTH SUBPLOTS
    
    # Set legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    by_label = dict(sorted(by_label.items()))
    
    fig.legend(by_label.values(), by_label.keys(), 
               bbox_to_anchor=(1.12, 0.91), frameon = False, 
               reverse = True, title = legend_title)
    
    plt.suptitle(chart_title)
    
    # Add 0 line
    for i, ax in enumerate(fig.axes):
        ax.axhline(y=0, color='black', linestyle='-', linewidth = 0.1)
        
    fig.tight_layout()

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')

def format_stacked_bar_pwr_delta_spatial(df_in1, df_in2, out_dir, 
                                         chart_title, legend_title, 
                                         file_name, color_dict, unit, 
                                         start_year, end_year, spatial):

    years = get_years(start_year, end_year)
    
    spatial_list = list(df_in1.index.get_level_values(spatial).unique())
    
    rows = math.ceil(len(spatial_list) / 2)
    
    fig, axs = plt.subplots(rows, 4, squeeze = False,
                            figsize = (9, rows * 2.5),
                            gridspec_kw = {
                                'width_ratios' : [1, 10, 1, 10]})
    
    axs = axs.ravel()

    x, y, z = 0, 1, 1
    
    legend_dict = {}

    for entry in spatial_list:
    
        # SET TIMESERIES SUBPLOT
        df1 = df_in1.loc[(df_in1['DELTA'] < 0) & 
                         (df_in1.index.get_level_values(spatial) == entry)]
        df2 = df_in1.loc[(df_in1['DELTA'] > 0) & 
                         (df_in1.index.get_level_values(spatial) == entry)]
    
        df1 = df1.groupby(['YEAR', 'TECH'])['DELTA'].sum().unstack().fillna(0)
        df2 = df2.groupby(['YEAR', 'TECH'])['DELTA'].sum().unstack().fillna(0)

        for idx in years:
            if not df1.empty:
                if not idx in df1.index:
                    df1.loc[idx] = 0
                    
            if not df2.empty:
                if not idx in df2.index:
                    df2.loc[idx] = 0
                
        df1.sort_index(inplace = True)
        df2.sort_index(inplace = True)

        # Initialize the bottom at zero for the first set of bars.
        bottom1 = np.zeros(len(df1))
        bottom2 = np.zeros(len(df2))
        
        # Plot each layer of the bar, adding each bar to the 'bottom' so
        # the next bar starts higher.

        for i, col in enumerate(df1.columns):
          axs[y].bar(df1.index, df1[col], bottom=bottom1, 
                 label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
          bottom1 += np.array(df1[col])
          
        for i, col in enumerate(df2.columns):
          axs[y].bar(df2.index, df2[col], bottom=bottom2, 
                 label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
          bottom2 += np.array(df2[col])
        
        # Axis formatting
        axs[y].xaxis.set_major_formatter(FormatStrFormatter('%d'))
        axs[y].margins(x=0)
        axs[y].set_ylim([min(df1.sum(axis=1), default = -.1) * 1.1, 
                         max(df2.sum(axis=1), default = .1) * 1.1])
        axs[y].set_title(entry, fontsize = 10)
        
        # Add unique legend entries
        handles, labels = axs[y].get_legend_handles_labels()
        by_label = dict(zip(labels, handles))

        for handle, label in by_label.items():
            legend_dict[handle] = label
        
        # SET TOTAL SUBPLOT  
        df3 = df_in2.loc[(df_in2['DELTA'] < 0) & 
                         (df_in2.index.get_level_values(spatial) == entry)]
        df4 = df_in2.loc[(df_in2['DELTA'] > 0) & 
                         (df_in2.index.get_level_values(spatial) == entry)]
    
        df3 = df3.groupby(['TECH'])['DELTA'].sum().fillna(0)
        df4 = df4.groupby(['TECH'])['DELTA'].sum().fillna(0)

        for idx in df_in2.index.get_level_values("TECH"):
            if not idx in df3.index:
                    df3.loc[idx] = 0
                
            if not idx in df4.index:    
                    df4.loc[idx] = 0
        
        df3 = pd.DataFrame(df3.sort_index()).transpose()
        df4 = pd.DataFrame(df4.sort_index()).transpose()
    
        # Initialize the bottom at zero for the first set of bars.
        bottom3 = np.zeros(len(df3))
        bottom4 = np.zeros(len(df4))
        
        # Plot each layer of the bar, adding each bar to the 'bottom' so
        # the next bar starts higher.
        for i, col in enumerate(df3.columns):
          axs[x].bar('Total', df3[col], bottom=bottom3, 
                 label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
          bottom3 += np.array(df3[col])
          
        for i, col in enumerate(df4.columns):
          axs[x].bar('Total', df4[col], bottom=bottom4, 
                 label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
          bottom4 += np.array(df4[col])
        
        # Axis formatting
        axs[x].margins(x=1)

        if df3.sum().sum() != 0:
            axs[x].set_ylim(ymin = min(df3.sum(axis=1) * 1.1))
            
        if df4.sum().sum() != 0:
            axs[x].set_ylim(ymax = max(df4.sum(axis=1) * 1.1))
            
        if df3.sum().sum() + df4.sum().sum() == 0:
            axs[x].set_yticks([0])
        
        if z % 2:
            axs[x].set_ylabel(unit)
            
        axs[x].set_title(entry, fontsize = 10)

        # Add unique legend entries
        handles, labels = axs[x].get_legend_handles_labels()
        by_label = dict(zip(labels, handles))

        for handle, label in by_label.items():
            legend_dict[handle] = label
        
        x, y, z = x + 2, y + 2, z + 1
    
    # CONFIG BOTH SUBPLOTS
    # Remove empty subplots
    if len(spatial_list) % 2:
        fig.delaxes(axs[x])
        fig.delaxes(axs[y])
    
    # Set legend
    legend_dict = dict(sorted(legend_dict.items()))

    fig.legend(legend_dict.values(), legend_dict.keys(), 
               bbox_to_anchor=(0.7, (0.018 * rows)), frameon = False, 
               reverse = True, title = legend_title,
               ncols = 4)
    
    # Add plot title
    if chart_title:
        make_space_above(axs, topmargin=0.7) 
        plt.suptitle(chart_title)
    
    # Adjust subplot whitespace
    plt.subplots_adjust(wspace=0.5, hspace=0.3)
    
    # Add 0 line
    for i, ax in enumerate(fig.axes):
        ax.axhline(y=0, color='black', linestyle='-', linewidth = 0.1)

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')

def format_bar_delta_country(df_in1, df_in2, out_dir, 
                             chart_title, legend_title, 
                             file_name, color_dict, 
                             unit):

    countries = list(df_in1["COUNTRY"].unique())
    
    df_years = {}
    df_total = {}
    n = 0

    for country in countries:
        df1 = df_in1.loc[df_in1['COUNTRY'] == country][['YEAR', 'VALUE']
                                                 ].set_index('YEAR')
        df2 = df_in2.loc[df_in2['COUNTRY'] == country][['YEAR', 'VALUE']
                                                 ].set_index('YEAR')

        # Calculate Delta by year
        df = df2 - df1
        
        # Calculate model horizon Delta
        df3 = round(df.sum(), 3)

        if abs(df3.iloc[0]) > 0:
            df_years[country] = df.copy()
            df_total[country] = df3.copy()
            n = n + 1

    rows = math.ceil(n / 2)
    
    fig, axs = plt.subplots(rows, 4, squeeze = False,
                            figsize = (9, rows * 2.5),
                            gridspec_kw = {
                                'width_ratios' : [1, 10, 1, 10]})
    axs = axs.ravel()

    x, y, z = 0, 1, 1
    
    legend_dict = {}
    
    for country in df_years.keys():

        axs[y].bar(df_years[country].index, df_years[country]['VALUE'], 
                   color = color_dict.get(country),
                   label = country, edgecolor = 'black', linewidth = 0.3)
        
        axs[x].bar('Total', df_total[country]['VALUE'],
                   color = color_dict.get(country), edgecolor = 'black', linewidth = 0.3)
        
        axs[y].margins(x=0)
        axs[x].margins(x=1)
        
        axs[x].set_title(country, fontsize = 10)
        
        axs[y].axhline(y=0, color='black', linestyle='-', linewidth = 0.1)
        
        if z % 2:
            axs[x].set_ylabel(unit)
            
        # Add unique legend entries
        handles, labels = axs[y].get_legend_handles_labels()
        by_label = dict(zip(labels, handles))

        for handle, label in by_label.items():
            legend_dict[handle] = label
        
        x, y, z = x + 2, y + 2, z + 1

    # CONFIG BOTH SUBPLOTS
    # Remove empty subplots
    for ax in range(x, (rows * 4)):
        fig.delaxes(axs[ax])
        
    plt.ticklabel_format(style='plain')

    # Adjust subplot whitespace
    plt.subplots_adjust(wspace=0.5, hspace=0.3)
    
    # Set legend
    legend_dict = dict(sorted(legend_dict.items()))

    fig.legend(legend_dict.values(), legend_dict.keys(), 
               bbox_to_anchor=(0.7, (0.02 * rows)), frameon = False, 
               title = legend_title, ncols = 4)
    
    # Add plot title
    if chart_title:
        make_space_above(axs, topmargin=0.7) 
        plt.suptitle(chart_title)

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')

def format_headline_metrics_global(capacity_in, production_in, 
                                   capacity_title, production_title,
                                   capacity_dict, production_dict,
                                   gen_shares_in1, gen_shares_in2, 
                                   gen_shares_title, gen_shares_dict,
                                   emissions_in1, emissions_in2, 
                                   emissions_title, emissions_dict,
                                   costs_in1, costs_in2, 
                                   costs_title, costs_dict,
                                   capacity_trn, max_capacity_trn,
                                   trn_title, trn_dict, out_dir, 
                                   chart_title, file_name, scenario):
    
    # SET PLOT BASE
    fig, axs = plt.subplots(3, 2, squeeze = False, 
                            gridspec_kw = {'height_ratios' : [1, 1, 1], 
                                           'width_ratios' : [1, 1]},
                            figsize = (12, 4)
                            )
    
    # SUBPLOT - CAPACITY
    capacity1 = capacity_in.loc[capacity_in['DELTA'] < 0]
    capacity2 = capacity_in.loc[capacity_in['DELTA'] > 0]

    capacity1 = capacity1.groupby(['TECH'])['DELTA'].sum().fillna(0)
    capacity2 = capacity2.groupby(['TECH'])['DELTA'].sum().fillna(0)
    
    for idx in capacity_in.index:
        if not capacity1.empty:
            if not idx in capacity1.index:
                capacity1.loc[idx] = 0
         
        if not capacity2.empty:
            if not idx in capacity2.index:
                capacity2.loc[idx] = 0
    
    capacity1 = pd.DataFrame(capacity1.sort_index()).transpose()
    capacity2 = pd.DataFrame(capacity2.sort_index()).transpose()

    # Initialize the bottom at zero for the first set of bars.
    capacity_bot1 = 0
    capacity_bot2 = 0
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(capacity1.columns):
      axs[0, 0].barh('Total', capacity1[col], left=capacity_bot1, 
             label=col, color = capacity_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      capacity_bot1 += capacity1[col].iloc[0]
      
    for i, col in enumerate(capacity2.columns):
      axs[0, 0].barh('Total', capacity2[col], left=capacity_bot2, 
             label=col, color = capacity_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      capacity_bot2 += capacity2[col].iloc[0]
    
    # Axis formatting
    axs[0, 0].set_xlim([min(capacity1.sum(axis=1), default = 0) * 1.1, 
                       max(capacity2.sum(axis=1), default = 0) * 1.1])
    axs[0, 0].title.set_text(capacity_title)
    
    # SUBPLOT - Generation
    production1 = production_in.loc[production_in['DELTA'] < 0]
    production2 = production_in.loc[production_in['DELTA'] > 0]

    production1 = production1.groupby(['TECH'])['DELTA'].sum().fillna(0)
    production2 = production2.groupby(['TECH'])['DELTA'].sum().fillna(0)
    
    for idx in production_in.index:
        if not production1.empty:
            if not idx in production1.index:
                production1.loc[idx] = 0
         
        if not production2.empty:
            if not idx in production2.index:
                production2.loc[idx] = 0
    
    production1 = pd.DataFrame(production1.sort_index()).transpose()
    production2 = pd.DataFrame(production2.sort_index()).transpose()

    # Initialize the bottom at zero for the first set of bars.
    production_bot1 = 0
    production_bot2 = 0
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(production1.columns):
      axs[0, 1].barh('Total', production1[col], left=production_bot1, 
             label=col, color = production_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      production_bot1 += production1[col].iloc[0]
      
    for i, col in enumerate(production2.columns):
      axs[0, 1].barh('Total', production2[col], left=production_bot2, 
             label=col, color = production_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      production_bot2 += production2[col].iloc[0]
    
    # Axis formatting
    axs[0, 1].set_xlim([min(production1.sum(axis=1), default = 0) * 1.1, 
                       max(production2.sum(axis=1), default = 0) * 1.1])
    axs[0, 1].title.set_text(production_title)    
    
    # Set combined legend for capacity & production subplots
    legend = []
    for key, value in capacity_dict.items():
        legend.append(Patch(facecolor = value, label = key))
        
    axs[0, 0].legend(handles = legend, bbox_to_anchor=(1.75, -0.55), 
                     frameon = False, ncols = 7)

    # SUBPLOT - GENERATION SHARES
    # Calculate Delta's for horizon (hz)
    for df in [gen_shares_in1, gen_shares_in2]:
        df['Metric'] = df['Metric'].replace({'Renewable energy share' : 'RENEWABLE',
                          'Fossil energy share' : 'FOSSIL'})

        df.set_index('Metric', inplace = True)
        df.drop(columns = ['Unit'], inplace = True)
        df.loc['OTHER'] = 100 - df.loc[df.index == 'RENEWABLE'
                                       ].iloc[0] - df.loc[df.index == 'FOSSIL'
                                                          ].iloc[0]
                                                          
    df_hz_in = gen_shares_in2 - gen_shares_in1
    df_hz_in = df_hz_in.transpose()[['RENEWABLE', 'FOSSIL', 'OTHER']]

    gen_shares1 = df_hz_in.clip(upper = 0)
    gen_shares2 = df_hz_in.clip(lower = 0)

    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    gen_shares_bot1 = 0
    gen_shares_bot2 = 0
    
    for i, col in enumerate(gen_shares1.columns):           
      axs[1, 0].barh('Total', gen_shares1[col], left = gen_shares_bot1,
                    color = gen_shares_dict.get(col), label = col
                    , edgecolor = 'black', linewidth = 0.3)
      gen_shares_bot1 += np.array(gen_shares1[col])
      
    for i, col in enumerate(gen_shares2.columns):
      axs[1, 0].barh('Total', gen_shares2[col], left = gen_shares_bot2,
                    color = gen_shares_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      gen_shares_bot2 += np.array(gen_shares2[col])
      
    # Subplot formatting
    axs[1, 0].xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    axs[1, 0].set_xlim([min(gen_shares1.sum(axis=1), default = 0) * 1.1, 
                       max(gen_shares2.sum(axis=1), default = 0) * 1.1])
    axs[1, 0].title.set_text(gen_shares_title)
    axs[1, 0].legend(bbox_to_anchor=(0.95, -0.7), frameon = False, 
              reverse = True, ncols = 3)
    
    # SUBPLOTS - Emissions and Costs
    for df in [emissions_in1, emissions_in2, costs_in1, costs_in2]:
        df.set_index('YEAR', inplace = True)

    # Calculate and set Emissions subplot
    emissions = emissions_in2['VALUE'] - emissions_in1['VALUE']
    emissions = emissions.sum()
    
    costs = costs_in2['VALUE'] - costs_in1['VALUE']
    costs = costs.sum()
    
    axs[1, 1].barh('Total', emissions,
                 color = emissions_dict.get('bar'), edgecolor = 'black', linewidth = 0.3)
    
    axs[2, 0].barh('Total', costs,
                 color = costs_dict.get('bar'), edgecolor = 'black', linewidth = 0.3)
    
    # Subplot formatting
    axs[1, 1].title.set_text(emissions_title)
    axs[2, 0].xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    axs[2, 0].title.set_text(costs_title)
    
    if emissions < 0:
        emissions = emissions * -1
        
    if costs < 0:
        costs = costs * -1
       
    axs[1, 1].set_xlim(emissions * -1.1, emissions * 1.1)
    axs[2, 0].set_xlim(costs * -1.1, costs * 1.1)
    
    #SUBPLOT - Transmission Capacity 
    capacity_trn = capacity_trn.loc[capacity_trn['TECHNOLOGY'
                                                 ] == f'TRN{scenario}'
                                    ].reset_index(drop = True)
    
    max_capacity_trn = max_capacity_trn.loc[(max_capacity_trn['TECHNOLOGY'
                                                 ] == f'TRN{scenario}') & 
                                            (max_capacity_trn['VALUE'] != 
                                             0)
                                            ].reset_index(drop = True)

    axs[2, 1].barh('Total', capacity_trn['VALUE'].iloc[0],
                 color = trn_dict.get('new'), label = 'Capacity Built'
                 , edgecolor = 'black', linewidth = 0.3)
    
    axs[2, 1].barh('Total', max_capacity_trn['VALUE'].iloc[0], 
                   height = 0.1, color = trn_dict.get('max'), 
                   label = 'Max Capacity', edgecolor = 'black', linewidth = 0.3)
    
    # Subplot formatting
    axs[2, 1].title.set_text(trn_title)
    axs[2, 1].set_xlim(0, max_capacity_trn['VALUE'].iloc[0] * 1.1)
    axs[2, 1].legend(bbox_to_anchor=(0.85, 2.77), frameon = False, 
              ncols = 2)
    
    # FIGURE ADJUSTMENTS
    # Make changes to all subplots
    for ax in axs.ravel():
        ax.set_yticks([])
        ax.axvline(x=0, color='black', linestyle='-', linewidth = 0.1)
        ax.margins(x = 0, y = 0.8)
    
    # Subplot spacing
   # fig.tight_layout()
    plt.subplots_adjust(hspace=2.5, wspace = 0.05)
    
    # Add plot title
    if chart_title:
        make_space_above(axs, topmargin=0.3) 
        plt.suptitle(chart_title)

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')

def format_bar_delta_multi_scenario(df1, df2_dict, out_dir, 
                                    chart_title, file_name, 
                                    color_dict, unit, 
                                    delta_sort, axis_sort):
    
    if isinstance(df1, Dict):
        for key in df1:
            df1[key].set_index('YEAR', inplace = True)
    
    else:
        df1.set_index('YEAR', inplace = True)
    
    plot_df = pd.DataFrame(columns = ['VALUE'])
    
    fig, ax = plt.subplots()
    
    for key in df2_dict:
        
        df2_dict[key].set_index('YEAR', inplace = True)
        if isinstance(df1, Dict):
            df = df2_dict[key][['VALUE']] - df1[key][['VALUE']]
            
        else:
            df = df2_dict[key][['VALUE']] - df1[['VALUE']]
        
        # Calculate model horizon Delta
        df3 = df.sum().fillna(0)
        plot_df.loc[key] = df3

    if axis_sort == True:
        plot_df = plot_df.sort_values(by = ['VALUE'])
    else:
        plot_df = plot_df.sort_index()
    
    ax.bar(plot_df.index, plot_df['VALUE'],
            color = color_dict.get('bar'), edgecolor = 'black', linewidth = 0.3)
    
    plt.xticks(rotation = 75)
    ax.margins(x=0)
    ax.axhline(y=0, color='black', linestyle='-', linewidth = 0.1)
    ax.set_ylabel(unit)
    ax.set_title(chart_title)

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')

def format_stacked_bar_gen_shares_delta_multi_scenario(df1, df2_dict, out_dir, 
                                                       chart_title, file_name, 
                                                       color_dict, unit, axis_sort):

    df1['Metric'] = df1['Metric'].replace({'Renewable energy share' : 'RENEWABLE',
                      'Fossil energy share' : 'FOSSIL'})

    df1.set_index('Metric', inplace = True)
    df1.drop(columns = ['Unit'], inplace = True)
    df1.loc['OTHER'] = 100 - df1.loc[df1.index == 'RENEWABLE'
                                   ].iloc[0] - df1.loc[df1.index == 'FOSSIL'
                                                      ].iloc[0]
    
    plot_df1 = pd.DataFrame(columns = ['RENEWABLE', 'FOSSIL', 'OTHER'])
    plot_df2 = pd.DataFrame(columns = ['RENEWABLE', 'FOSSIL', 'OTHER'])
    
    for key, value in df2_dict.items():
        
        value['Metric'] = value['Metric'].replace({'Renewable energy share' : 'RENEWABLE',
                          'Fossil energy share' : 'FOSSIL'})
    
        value.set_index('Metric', inplace = True)
        value.drop(columns = ['Unit'], inplace = True)
        value.loc['OTHER'] = 100 - value.loc[value.index == 'RENEWABLE'
                                       ].iloc[0] - value.loc[value.index == 'FOSSIL'
                                                          ].iloc[0]
                                                          
        value = (value - df1)
        value = value.transpose()[['RENEWABLE', 'FOSSIL', 'OTHER']
                                  ].rename(index={'Value': key})
        
        gen_shares1 = value.clip(upper = 0)
        gen_shares2 = value.clip(lower = 0)
        
        if plot_df1.empty:
            plot_df1 = gen_shares1
            plot_df2 = gen_shares2
        else:
            plot_df1 = pd.concat([plot_df1, gen_shares1])
            plot_df2 = pd.concat([plot_df2, gen_shares2])
            
    if axis_sort == True:
        plot_df1['sum'] = plot_df1.sum(axis=1)
        plot_df1 = plot_df1.sort_values(by = ['sum']).drop(columns = ['sum'])
    else:
        plot_df1 = plot_df1.sort_index()
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    gen_shares_bot1 = 0
    gen_shares_bot2 = 0
    
    fig, ax = plt.subplots()
    
    for i, col in enumerate(plot_df1.columns):           
      ax.bar(plot_df1.index, plot_df1[col], bottom = gen_shares_bot1,
              color = color_dict.get(col), label = col, edgecolor = 'black', linewidth = 0.3)
      gen_shares_bot1 += np.array(plot_df1[col])
      
    for i, col in enumerate(plot_df2.columns):
      ax.bar(plot_df2.index, plot_df2[col], bottom = gen_shares_bot2,
             color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      gen_shares_bot2 += np.array(plot_df2[col])
      
    # Subplot formatting
    ax.set_ylim([min(plot_df1.sum(axis=1), default = 0) * 1.1, 
                 max(plot_df2.sum(axis=1), default = 0) * 1.1])
    ax.legend(frameon = False, reverse = True, ncols = 1)
    
    plt.xticks(rotation = 75)
    ax.margins(x=0)
    ax.axhline(y=0, color='black', linestyle='-', linewidth = 0.1)
    ax.set_ylabel(unit)
    ax.set_title(chart_title)
    

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')

def format_stacked_bar_pwr_delta_multi_scenario(df_dict, out_dir, 
                                                chart_title, file_name, 
                                                color_dict, unit, axis_sort):
    
    plot_df1 = None
    
    for key, value in df_dict.items():

        capacity1 = value.loc[value['DELTA'] < 0]
        capacity2 = value.loc[value['DELTA'] > 0]
       
        capacity1 = capacity1.groupby(['TECH'])['DELTA'].sum().fillna(0)
        capacity2 = capacity2.groupby(['TECH'])['DELTA'].sum().fillna(0)
        
        for idx in value.index:
            if not capacity1.empty:
                if not idx in capacity1.index:
                    capacity1.loc[idx] = 0
             
            if not capacity2.empty:
                if not idx in capacity2.index:
                    capacity2.loc[idx] = 0
        
        capacity1 = pd.DataFrame(capacity1).transpose()
        capacity2 = pd.DataFrame(capacity2).transpose()
        
        capacity1.rename(index = {'DELTA' : key}, inplace = True)
        capacity2.rename(index = {'DELTA' : key}, inplace = True)

        if plot_df1 is None:
            plot_df1 = capacity1.copy()
            plot_df2 = capacity2.copy()
        else:
            plot_df1 = pd.concat([plot_df1, capacity1])
            plot_df2 = pd.concat([plot_df2, capacity2])
        
    plot_df1 = plot_df1.fillna(0)
    plot_df2 = plot_df2.fillna(0)
    
    if axis_sort == True:
        plot_sum = (plot_df1.sum(axis=1) * -1 + plot_df2.sum(axis=1)
                    ).sort_values(ascending = False)
        
    else:
        plot_sum = (plot_df1.sum(axis=1) * -1 + plot_df2.sum(axis=1)
                    ).sort_index()

    plot_df1 = plot_df1.reindex(plot_sum.index
                                ).reindex(sorted(plot_df1.columns), axis=1)
    plot_df2 = plot_df2.reindex(plot_sum.index
                                ).reindex(sorted(plot_df2.columns), axis=1)
    
    # Initialize the bottom at zero for the first set of bars.
    capacity_bot1 = 0
    capacity_bot2 = 0
    
    fig, ax = plt.subplots()
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(plot_df1.columns):
      ax.bar(plot_df1.index, plot_df1[col], bottom=capacity_bot1, 
             label=col, color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      capacity_bot1 += np.array(plot_df1[col])
      
    for i, col in enumerate(plot_df2.columns):
      ax.bar(plot_df2.index, plot_df2[col], bottom=capacity_bot2, 
             color = color_dict.get(col), edgecolor = 'black', linewidth = 0.3)
      capacity_bot2 += np.array(plot_df2[col])
      
    ax.legend(frameon = False, ncols = 1, bbox_to_anchor=(1, 1.03),
              reverse = True)

    plt.xticks(rotation = 75)
    ax.margins(x=0)
    ax.axhline(y=0, color='black', linestyle='-', linewidth = 0.3)
    ax.set_ylabel(unit)
    ax.set_title(chart_title)
    ax.set_ylim([min(plot_df1.sum(axis=1), default = 0) * 1.1, 
                 max(plot_df2.sum(axis=1), default = 0) * 1.1])
    
      
    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')

def format_spatial_map_ZIZABONA(df, nodes, base_path, 
                                chart_title, file_name, 
                                color_dict, label):

    df = df.loc[df['region'].isin(nodes)].sort_values(by = ['region']
                                                      ).reset_index(drop = True)
    
    df.insert(0, 'COUNTRY', df['region'].str[:3])

    country_shp = shpreader.natural_earth(resolution='10m',
                                          category='cultural',
                                          name='admin_0_countries')
    
    fig = plt.figure()

    axs1 = plt.axes(projection = ccrs.PlateCarree(), zorder = 1)

    axs1.coastlines()
    axs1.set_extent([5, 45, -35, 10])

        
    for acountry in shpreader.Reader(country_shp).records():
        search = acountry.attributes['ISO_A3'].rstrip('\x00')

        if search in list(df['COUNTRY'].unique()):
            col = color_dict.get(search)
        else:
            col = 'lightgrey'

        axs1.add_geometries([acountry.geometry], ccrs.PlateCarree(),
                           facecolor= col, alpha = 0.5)

    label_adjust = {'AGOXX' : [0.3, 0.6], 'BWAXX' : [0.3, 0.6], 'CODXX' : [0.3, 0.6], 
                    'LSOXX' : [-4.2, -1.5], 'MOZXX' : [1, -0.5], 'MWIXX' : [0.3, 0.6], 
                    'NAMXX' : [0.3, 0.6], 'SWZXX' : [-2, -2], 'TZAXX' : [-4.2, -1.5], 
                    'ZAFXX' : [-4.2, -1.5], 'ZMBXX' : [0.3, 0.6], 'ZWEXX' : [0.3, 0.6]}


    for index, row in df.iterrows():
        axs1.scatter(row['long'], row['lat'], transform=ccrs.Geodetic(),
                     facecolor = 'red', zorder=2, s = 5)
        
        adjust = label_adjust.get(row['region'])
        
        
        axs1.text(row['long'] + adjust[0], row['lat'] + adjust[1], row['region'], 
                  name = 'Calibri', fontsize = 7, zorder=3, weight = 'bold')
        
    axs1.text(5.5, -36, label, name = 'Calibri', fontsize = 11, weight = 'bold')
 
    plt.show()

    return fig.savefig(os.path.join(base_path, file_name), bbox_inches = 'tight')

def format_multi_plot_cap_gen_genshares_emissions(df1, df2, df3, df4, df5, 
                                                   unit1, unit2, unit3, unit4, unit5,
                                                   base_path, file_name, color_dict1,
                                                   color_dict2, color_dict3):
    
    # SET PLOT BASE
    fig, axs = plt.subplots(2, 2, squeeze = False, 
                            gridspec_kw = {'height_ratios' : [1, 1], 
                                           'width_ratios' : [1, 1]},
                            figsize = (10, 6)
                            )
    
    # SET CAPACITY AND GENERATION GRAPHS
    df1 = df1.groupby(['YEAR', 'TECH'])['VALUE'].sum().unstack().fillna(0)
    df2 = df2.groupby(['YEAR', 'TECH'])['VALUE'].sum().unstack().fillna(0)
    
    # Initialize the bottom at zero for the first set of bars.
    bottom1 = np.zeros(len(df1))
    bottom2 = np.zeros(len(df2))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(df1.columns):
      axs[0, 0].bar(df1.index, df1[col], bottom=bottom1, 
             label=col, color = color_dict1.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom1 += np.array(df1[col])
      
    for i, col in enumerate(df2.columns):
      axs[0, 1].bar(df2.index, df2[col], bottom=bottom2, 
                    color = color_dict1.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom2 += np.array(df2[col])
    
    axs[0, 0].set_ylabel(unit1)
    axs[0, 1].set_ylabel(unit2)
    axs[0, 0].legend(bbox_to_anchor=(2.23, -0.1), frameon = False, 
              ncols = 8)

    # SET GEN SHARES GRAPH
    
    df3['OTHER'] = 100 - df3['RENEWABLE'] - df3['FOSSIL']
    df3 = df3[['YEAR', 'RENEWABLE', 'FOSSIL', 'OTHER']].groupby(['YEAR']).sum()

    # Initialize the bottom at zero for the first set of bars.
    bottom3 = np.zeros(len(df3))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(df3.columns):
      axs[1, 0].bar(df3.index, df3[col], bottom=bottom3, 
             label=col, color = color_dict2.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom3 += np.array(df3[col])

    axs[1, 0].set_ylabel(unit3)
    axs[1, 0].legend(bbox_to_anchor=(1.05, -0.1), frameon = False, 
              ncols = 3)

    # SET EMISSIONS GRAPH
    
    df4 = df4.groupby(['YEAR', 'COUNTRY'])['VALUE'].sum().unstack().fillna(0)
    df5.set_index('YEAR', inplace = True)

    # Initialize the bottom at zero for the first set of bars.
    bottom4 = np.zeros(len(df4))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(df4.columns):
      axs[1, 1].bar(df4.index, df4[col], bottom=bottom4, 
             label=col, color = color_dict3.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom4 += np.array(df4[col])
      
    ax2 = axs[1, 1].twinx()
    
    ax2.plot(df5.index, df5['VALUE'], label= unit5, 
             color = 'red')
    
    axs[1, 1].set_ylabel(unit4)
    ax2.set_ylabel(unit5)
    axs[1, 1].legend(bbox_to_anchor=(1.06, -0.1), frameon = False, 
               ncols = 4)
    
    ax2.legend(bbox_to_anchor=(1, 1), frameon = False)

    # PLT ADJUSTMENTS
    for ax in axs.ravel():
        ax.margins(x = 0)
        

    axs[0, 0].text(-0.16, 0, 'a', transform=axs[0, 0].transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
    
    axs[0, 1].text(1.05, 0, 'b', transform=axs[0, 0].transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
    
    axs[1, 0].text(-0.16, -1.43, 'c', transform=axs[0, 0].transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
    
    axs[1, 1].text(1.05, -1.43, 'd', transform=axs[0, 0].transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
       
    plt.subplots_adjust(wspace=0.22, hspace = 0.42)

    
    return fig.savefig(os.path.join(base_path, file_name), bbox_inches = 'tight')
    
def format_multi_plot_country_charts(df1, df2, df3, df4, df5, 
                                     unit1, unit2, unit3, unit4, unit5,
                                     base_path, file_name, color_dict1,
                                     color_dict2, color_dict3, country):
    
    # SET PLOT BASE
    fig, axs = plt.subplots(2, 2, squeeze = False, 
                            gridspec_kw = {'height_ratios' : [1, 1], 
                                           'width_ratios' : [1, 1]},
                            figsize = (10, 6)
                            )
    
    base_path = os.path.join(base_path, country)
    
    # SET CAPACITY AND GENERATION GRAPHS
    df1 = df1.loc[df1['COUNTRY'] == country]
    df2 = df2.loc[df2['COUNTRY'] == country]
    
    df1 = df1.groupby(['YEAR', 'TECH'])['VALUE'].sum().unstack().fillna(0)
    df2 = df2.groupby(['YEAR', 'TECH'])['VALUE'].sum().unstack().fillna(0)
    
    # Initialize the bottom at zero for the first set of bars.
    bottom1 = np.zeros(len(df1))
    bottom2 = np.zeros(len(df2))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(df1.columns):
      axs[0, 0].bar(df1.index, df1[col], bottom=bottom1, 
             label=col, color = color_dict1.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom1 += np.array(df1[col])
      
    for i, col in enumerate(df2.columns):
      axs[0, 1].bar(df2.index, df2[col], bottom=bottom2, 
                    color = color_dict1.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom2 += np.array(df2[col])
    
    axs[0, 0].set_ylabel(unit1)
    axs[0, 1].set_ylabel(unit2)
    axs[0, 0].legend(bbox_to_anchor=(2.23, -0.1), frameon = False, 
              ncols = 8)

    # SET GEN SHARES GRAPH
    df3 = df3.loc[df3['COUNTRY'] == country].reset_index()
    
    df3['OTHER'] = 100 - df3['RENEWABLE'] - df3['FOSSIL']
    df3 = df3[['YEAR', 'RENEWABLE', 'FOSSIL', 'OTHER']].groupby(['YEAR']).sum()

    # Initialize the bottom at zero for the first set of bars.
    bottom3 = np.zeros(len(df3))
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(df3.columns):
      axs[1, 0].bar(df3.index, df3[col], bottom=bottom3, 
             label=col, color = color_dict2.get(col), edgecolor = 'black', linewidth = 0.3)
      bottom3 += np.array(df3[col])

    axs[1, 0].set_ylabel(unit3)
    axs[1, 0].legend(bbox_to_anchor=(1.05, -0.1), frameon = False, 
              ncols = 3)

    # SET EMISSIONS GRAPH
    df4 = df4.loc[df4['COUNTRY'] == country][['YEAR', 'VALUE']]
    df5 = df5.loc[df5['COUNTRY'] == country][['YEAR', 'VALUE']]
    
    df4.set_index('YEAR', inplace = True)
    df5.set_index('YEAR', inplace = True)
    
    axs[1, 1].bar(df4.index, df4['VALUE'], label= unit4, 
                  color = color_dict3.get('bar'), edgecolor = 'black', linewidth = 0.3)
      
    ax2 = axs[1, 1].twinx()
    
    ax2.plot(df5.index, df5['VALUE'], label= unit5, 
             color = color_dict3.get('line'))
    
    axs[1, 1].set_ylabel(unit4)
    ax2.set_ylabel(unit5)
    axs[1, 1].legend(bbox_to_anchor=(0.5, -0.1), frameon = False)
    
    ax2.legend(bbox_to_anchor=(0.9, -0.1), frameon = False)

    # PLT ADJUSTMENTS
    for ax in axs.ravel():
        ax.margins(x = 0)
        

    axs[0, 0].text(-0.16, 0, 'a', transform=axs[0, 0].transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
    
    axs[0, 1].text(1.05, 0, 'b', transform=axs[0, 0].transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
    
    axs[1, 0].text(-0.16, -1.43, 'c', transform=axs[0, 0].transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
    
    axs[1, 1].text(1.05, -1.43, 'd', transform=axs[0, 0].transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
       
    plt.subplots_adjust(wspace=0.22, hspace = 0.42)
    
    make_space_above(axs, topmargin=0.45) 
    plt.suptitle(country, weight = 'bold')

    return fig.savefig(os.path.join(base_path, file_name), bbox_inches = 'tight')

def format_multi_plot_scen_comparison(df1_dict, df2_dict, df3, df3_dict, 
                                      df4, df4_dict, unit1, unit2, unit3, unit4,
                                      color_dict1, color_dict2, color_dict3,
                                      base_path, file_name, axis_sort):
    
    # SET PLOT BASE
    fig, axs = plt.subplots(2, 2, squeeze = False, 
                            gridspec_kw = {'height_ratios' : [1, 1], 
                                           'width_ratios' : [1, 1]},
                            figsize = (10, 8)
                            )
    
    # SET CAPACITY AND GENERATION CHARTS
    plot_df1a = None
    plot_df2a = None
    
    for key, value in df1_dict.items():

        capacity1 = value.loc[value['DELTA'] < 0]
        capacity2 = value.loc[value['DELTA'] > 0]
       
        capacity1 = capacity1.groupby(['TECH'])['DELTA'].sum().fillna(0)
        capacity2 = capacity2.groupby(['TECH'])['DELTA'].sum().fillna(0)
        
        for idx in value.index:
            if not capacity1.empty:
                if not idx in capacity1.index:
                    capacity1.loc[idx] = 0
             
            if not capacity2.empty:
                if not idx in capacity2.index:
                    capacity2.loc[idx] = 0
        
        capacity1 = pd.DataFrame(capacity1).transpose()
        capacity2 = pd.DataFrame(capacity2).transpose()
        
        capacity1.rename(index = {'DELTA' : key}, inplace = True)
        capacity2.rename(index = {'DELTA' : key}, inplace = True)

        if plot_df1a is None:
            plot_df1a = capacity1.copy()
            plot_df1b = capacity2.copy()
        else:
            plot_df1a = pd.concat([plot_df1a, capacity1])
            plot_df1b  = pd.concat([plot_df1b, capacity2])
            
    for key, value in df2_dict.items():

        generation1 = value.loc[value['DELTA'] < 0]
        generation2 = value.loc[value['DELTA'] > 0]
       
        generation1 = generation1.groupby(['TECH'])['DELTA'].sum().fillna(0)
        generation2 = generation2.groupby(['TECH'])['DELTA'].sum().fillna(0)
        
        for idx in value.index:
            if not generation1.empty:
                if not idx in generation1.index:
                    generation1.loc[idx] = 0
             
            if not generation2.empty:
                if not idx in generation2.index:
                    generation2.loc[idx] = 0
        
        generation1 = pd.DataFrame(generation1).transpose()
        generation2 = pd.DataFrame(generation2).transpose()
        
        generation1.rename(index = {'DELTA' : key}, inplace = True)
        generation2.rename(index = {'DELTA' : key}, inplace = True)

        if plot_df2a is None:
            plot_df2a = generation1.copy()
            plot_df2b = generation2.copy()
        else:
            plot_df2a = pd.concat([plot_df2a, generation1])
            plot_df2b  = pd.concat([plot_df2b, generation2])

    plot_df1a = plot_df1a.fillna(0)
    plot_df1b = plot_df1b.fillna(0)
    plot_df2a = plot_df2a.fillna(0)
    plot_df2b = plot_df2b.fillna(0)     
                
    if axis_sort == True:
        plot_sum1 = (plot_df1a.sum(axis=1) * -1 + plot_df1b.sum(axis=1)
                    ).sort_values(ascending = False)
        plot_sum2 = (plot_df2a.sum(axis=1) * -1 + plot_df2b.sum(axis=1)
                    ).sort_values(ascending = False)
        
    else:
        plot_sum1 = (plot_df1a.sum(axis=1) * -1 + plot_df1b.sum(axis=1)
                    ).sort_index()
        plot_sum2 = (plot_df2a.sum(axis=1) * -1 + plot_df2b.sum(axis=1)
                    ).sort_index()

    plot_df1a =  plot_df1a.reindex(plot_sum1.index).reindex(sorted(plot_df1a.columns), axis=1)
    plot_df1b =  plot_df1b.reindex(plot_sum1.index).reindex(sorted(plot_df1b.columns), axis=1)
    plot_df2a =  plot_df2a.reindex(plot_sum2.index).reindex(sorted(plot_df2a.columns), axis=1)
    plot_df2b =  plot_df2b.reindex(plot_sum2.index).reindex(sorted(plot_df2b.columns), axis=1)
        
    # Initialize the bottom at zero for the first set of bars.
    capacity_bot1 = 0
    capacity_bot2 = 0
    generation_bot1 = 0
    generation_bot2 = 0
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(plot_df1a.columns):
      axs[0, 0].bar(plot_df1a.index, plot_df1a[col], bottom=capacity_bot1, 
                    label=col, color = color_dict1.get(col), edgecolor = 'black', 
                    linewidth = 0.3)
      capacity_bot1 += np.array(plot_df1a[col])
      
    for i, col in enumerate(plot_df1b.columns):
      axs[0, 0].bar(plot_df1b.index, plot_df1b[col], bottom=capacity_bot2, 
             color = color_dict1.get(col), edgecolor = 'black', 
             linewidth = 0.3)
      capacity_bot2 += np.array(plot_df1b[col])
      
    for i, col in enumerate(plot_df2a.columns):
      axs[0, 1].bar(plot_df2a.index, plot_df2a[col], bottom=generation_bot1, 
                    label=col, color = color_dict1.get(col), edgecolor = 'black', 
                    linewidth = 0.3)
      generation_bot1 += np.array(plot_df2a[col])
      
    for i, col in enumerate(plot_df2b.columns):
      axs[0, 1].bar(plot_df2b.index, plot_df2b[col], bottom=generation_bot2, 
             color = color_dict1.get(col), edgecolor = 'black', 
             linewidth = 0.3)
      generation_bot2 += np.array(plot_df2b[col])   
      
    axs[0, 1].legend(bbox_to_anchor=(0.85, -0.47), frameon = False, 
                     ncols = 7)

    axs[0, 0].set_ylabel(unit1)
    axs[0, 1].set_ylabel(unit2)
    
    axs[0, 0].set_ylim([min(plot_df1a.sum(axis=1), default = 0) * 1.1, 
                        max(plot_df1b.sum(axis=1), default = 0) * 1.1])

    axs[0, 1].set_ylim([min(plot_df2a.sum(axis=1), default = 0) * 1.1, 
                        max(plot_df2b.sum(axis=1), default = 0) * 1.1])
    
    # SET GEN SHARES CHART
    

    df3['Metric'] = df3['Metric'].replace({'Renewable energy share' : 'RENEWABLE',
                      'Fossil energy share' : 'FOSSIL'})

    df3.set_index('Metric', inplace = True)
    df3.drop(columns = ['Unit'], inplace = True)
    df3.loc['OTHER'] = 100 - df3.loc[df3.index == 'RENEWABLE'
                                   ].iloc[0] - df3.loc[df3.index == 'FOSSIL'
                                                      ].iloc[0]
    
    plot_df3a = pd.DataFrame(columns = ['RENEWABLE', 'FOSSIL', 'OTHER'])
    plot_df3b = pd.DataFrame(columns = ['RENEWABLE', 'FOSSIL', 'OTHER'])
    
    for key, value in df3_dict.items():
        
        value['Metric'] = value['Metric'].replace({'Renewable energy share' : 'RENEWABLE',
                          'Fossil energy share' : 'FOSSIL'})
    
        value.set_index('Metric', inplace = True)
        value.drop(columns = ['Unit'], inplace = True)
        value.loc['OTHER'] = 100 - value.loc[value.index == 'RENEWABLE'
                                       ].iloc[0] - value.loc[value.index == 'FOSSIL'
                                                          ].iloc[0]
                                                          
        value = (value - df3)
        value = value.transpose()[['RENEWABLE', 'FOSSIL', 'OTHER']
                                  ].rename(index={'Value': key})
        
        gen_shares1 = value.clip(upper = 0)
        gen_shares2 = value.clip(lower = 0)
        
        if plot_df3a.empty:
            plot_df3a = gen_shares1
            plot_df3b = gen_shares2
        else:
            plot_df3a = pd.concat([plot_df3a, gen_shares1])
            plot_df3b = pd.concat([plot_df3b, gen_shares2])
            
    if axis_sort == True:
        plot_df3a['sum'] = plot_df3a.sum(axis=1)
        plot_df3a = plot_df3a.sort_values(by = ['sum']).drop(columns = ['sum'])
    else:
        plot_df3a = plot_df3a.sort_index()
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    gen_shares_bot1 = 0
    gen_shares_bot2 = 0
    
    for i, col in enumerate(plot_df3a.columns):           
      axs[1, 0].bar(plot_df3a.index, plot_df3a[col], bottom = gen_shares_bot1,
              color = color_dict2.get(col), label = col, edgecolor = 'black',
              linewidth = 0.3)
      gen_shares_bot1 += np.array(plot_df3a[col])
      
    for i, col in enumerate(plot_df3b.columns):
      axs[1, 0].bar(plot_df3b.index, plot_df3b[col], bottom = gen_shares_bot2,
             color = color_dict2.get(col), edgecolor = 'black', linewidth = 0.3)
      gen_shares_bot2 += np.array(plot_df3b[col])
      
    # Subplot formatting
    axs[1, 0].set_ylim([min(plot_df3a.sum(axis=1), default = 0) * 1.1, 
                        max(plot_df3b.sum(axis=1), default = 0) * 1.1])
    axs[1, 0].legend(frameon = False, reverse = True, ncols = 1)

    axs[1, 0].set_ylabel(unit3)
    
    axs[1, 0].legend(bbox_to_anchor=(1.05, -0.47), frameon = False, 
              ncols = 3)
    
    # SET EMISSIONS CHART
    
    df4.set_index('YEAR', inplace = True)
    plot_df4 = pd.DataFrame(columns = ['VALUE'])

    for key in df4_dict:

        df4_dict[key].set_index('YEAR', inplace = True)
           
        # Calculate Delta by year
        data = df4_dict[key][['VALUE']] - df4[['VALUE']]
        
        # Calculate model horizon Delta
        data = data.sum().fillna(0)
        plot_df4.loc[key] = data
    
    if axis_sort == True:
        plot_df4 = plot_df4.sort_values(by = ['VALUE'])
    else:
        plot_df4 = plot_df4.sort_index()
    
    axs[1, 1].bar(plot_df4.index, plot_df4['VALUE'],
                  color = color_dict3.get('bar'))
    
    axs[1, 1].set_ylabel(unit4)

    # PLT ADJUSTMENTS
    for ax in axs.ravel():
        ax.margins(x = 0)
        ax.axhline(y=0, color='black', linestyle='-', linewidth = 0.3)
        ax.tick_params(axis = 'x', labelrotation = 75)
        
    axs[0, 0].text(-0.16, 0, 'a', transform=axs[0, 0].transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
    
    axs[0, 1].text(1.05, 0, 'b', transform=axs[0, 0].transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
    
    axs[1, 0].text(-0.16, -1.72, 'c', transform=axs[0, 0].transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
    
    axs[1, 1].text(1.05, -1.72, 'd', transform=axs[0, 0].transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
       
    plt.subplots_adjust(wspace=0.24, hspace = 0.72)

    
    return fig.savefig(os.path.join(base_path, file_name), bbox_inches = 'tight')

def format_multi_plot_scen_comparison_costs(df1_dict, df2_dict, df3, df3_dict, 
                                            df4, df4_dict, df5, df5_dict, 
                                            unit1, unit2, unit3, unit4, unit5,
                                            color_dict1, color_dict2, color_dict3,
                                            color_dict4, base_path, file_name, 
                                            scenarios):
    
    fig = plt.figure(figsize = (10, 8))

    gs = GridSpec(2, 40, figure=fig)
    ax1 = fig.add_subplot(gs[1, 0:12])
    ax2 = fig.add_subplot(gs[1, 14:18])
    ax3 = fig.add_subplot(gs[1, 21:34])
    ax4 = fig.add_subplot(gs[1, 36:])

    ax5 = fig.add_subplot(gs[0, 0:14])
    ax6 = fig.add_subplot(gs[0, 17:])
    # SET CAPACITY AND GENERATION CHARTS
    plot_df1a = None
    plot_df2a = None
    
    for key, value in df1_dict.items():

        capacity1 = value.loc[value['DELTA'] < 0]
        capacity2 = value.loc[value['DELTA'] > 0]
       
        capacity1 = capacity1.groupby(['TECH'])['DELTA'].sum().fillna(0)
        capacity2 = capacity2.groupby(['TECH'])['DELTA'].sum().fillna(0)
        
        for idx in value.index:
            if not capacity1.empty:
                if not idx in capacity1.index:
                    capacity1.loc[idx] = 0
             
            if not capacity2.empty:
                if not idx in capacity2.index:
                    capacity2.loc[idx] = 0
        
        capacity1 = pd.DataFrame(capacity1).transpose()
        capacity2 = pd.DataFrame(capacity2).transpose()
        
        capacity1.rename(index = {'DELTA' : key}, inplace = True)
        capacity2.rename(index = {'DELTA' : key}, inplace = True)

        if plot_df1a is None:
            plot_df1a = capacity1.copy()
            plot_df1b = capacity2.copy()
        else:
            plot_df1a = pd.concat([plot_df1a, capacity1])
            plot_df1b  = pd.concat([plot_df1b, capacity2])
            
    for key, value in df2_dict.items():

        generation1 = value.loc[value['DELTA'] < 0]
        generation2 = value.loc[value['DELTA'] > 0]
       
        generation1 = generation1.groupby(['TECH'])['DELTA'].sum().fillna(0)
        generation2 = generation2.groupby(['TECH'])['DELTA'].sum().fillna(0)
        
        for idx in value.index:
            if not generation1.empty:
                if not idx in generation1.index:
                    generation1.loc[idx] = 0
             
            if not generation2.empty:
                if not idx in generation2.index:
                    generation2.loc[idx] = 0
        
        generation1 = pd.DataFrame(generation1).transpose()
        generation2 = pd.DataFrame(generation2).transpose()
        
        generation1.rename(index = {'DELTA' : key}, inplace = True)
        generation2.rename(index = {'DELTA' : key}, inplace = True)

        if plot_df2a is None:
            plot_df2a = generation1.copy()
            plot_df2b = generation2.copy()
        else:
            plot_df2a = pd.concat([plot_df2a, generation1])
            plot_df2b  = pd.concat([plot_df2b, generation2])

    plot_df1a = plot_df1a.fillna(0)
    plot_df1b = plot_df1b.fillna(0)
    plot_df2a = plot_df2a.fillna(0)
    plot_df2b = plot_df2b.fillna(0)     


    filter_list = list(scenarios.values())[0:4]
    data1 =  plot_df1a.loc[filter_list]
    data2 =  plot_df1b.loc[filter_list]
    data3 =  plot_df2a.loc[filter_list]
    data4 =  plot_df2b.loc[filter_list]
    
    # Initialize the bottom at zero for the first set of bars.
    capacity_bot1 = 0
    capacity_bot2 = 0
    generation_bot1 = 0
    generation_bot2 = 0
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(data1.columns):
      ax1.bar(filter_list, data1[col], bottom=capacity_bot1, 
                    label=col, color = color_dict1.get(col), edgecolor = 'black', 
                    linewidth = 0.3)
      capacity_bot1 += np.array(data1[col])
      
    for i, col in enumerate(data2.columns):
      ax1.bar(filter_list, data2[col], bottom=capacity_bot2, 
             color = color_dict1.get(col), edgecolor = 'black', 
             linewidth = 0.3)
      capacity_bot2 += np.array(data2[col])
      
    for i, col in enumerate(data3.columns):
      ax3.bar(filter_list, data3[col], bottom=generation_bot1, 
                    label=col, color = color_dict1.get(col), edgecolor = 'black', 
                    linewidth = 0.3)
      generation_bot1 += np.array(data3[col])
      
    for i, col in enumerate(data4.columns):
      ax3.bar(filter_list, data4[col], bottom=generation_bot2, 
             color = color_dict1.get(col), edgecolor = 'black', 
             linewidth = 0.3)
      generation_bot2 += np.array(data4[col])   
      
    ax3.legend(bbox_to_anchor=(1.25, -0.52), frameon = False, 
                     ncols = 7)

    ax1.set_ylabel(unit1)
    ax3.set_ylabel(unit2)
    
    ax1.set_ylim([min(data1.sum(axis=1), default = 0) * 1.1, 
                        max(data2.sum(axis=1), default = 0) * 1.1])

    ax3.set_ylim([min(data3.sum(axis=1), default = 0) * 1.1, 
                        max(data4.sum(axis=1), default = 0) * 1.1])
    
    ax1.set_frame_on(False)
    ax3.set_frame_on(False)
    
    filter_list = list(scenarios.values())[4:]
    data1 =  plot_df1a.loc[filter_list]
    data2 =  plot_df1b.loc[filter_list]
    data3 =  plot_df2a.loc[filter_list]
    data4 =  plot_df2b.loc[filter_list]
    
    # Initialize the bottom at zero for the first set of bars.
    capacity_bot1 = 0
    capacity_bot2 = 0
    generation_bot1 = 0
    generation_bot2 = 0
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    for i, col in enumerate(data1.columns):
      ax2.bar(filter_list, data1[col], bottom=capacity_bot1, 
                    label=col, color = color_dict1.get(col), edgecolor = 'black', 
                    linewidth = 0.3)
      capacity_bot1 += np.array(data1[col])
      
    for i, col in enumerate(data2.columns):
      ax2.bar(filter_list, data2[col], bottom=capacity_bot2, 
             color = color_dict1.get(col), edgecolor = 'black', 
             linewidth = 0.3)
      capacity_bot2 += np.array(data2[col])
      
    for i, col in enumerate(data3.columns):
      ax4.bar(filter_list, data3[col], bottom=generation_bot1, 
                    label=col, color = color_dict1.get(col), edgecolor = 'black', 
                    linewidth = 0.3)
      generation_bot1 += np.array(data3[col])
      
    for i, col in enumerate(data4.columns):
      ax4.bar(filter_list, data4[col], bottom=generation_bot2, 
             color = color_dict1.get(col), edgecolor = 'black', 
             linewidth = 0.3)
      generation_bot2 += np.array(data4[col])   
      

  #  ax2.set_ylabel(unit1)
   # ax4.set_ylabel(unit2)
   
    ax2.set_frame_on(False)
    ax4.set_frame_on(False)
    
    ax2.set_ylim([min(data1.sum(axis=1), default = 0) * 1.1, 
                        max(data2.sum(axis=1), default = 0) * 1.1])

    ax4.set_ylim([min(data3.sum(axis=1), default = 0) * 1.1, 
                        max(data4.sum(axis=1), default = 0) * 1.1])
    
    # SET GEN SHARES CHART
    

    df3['Metric'] = df3['Metric'].replace({'Renewable energy share' : 'RENEWABLE',
                      'Fossil energy share' : 'FOSSIL'})

    df3.set_index('Metric', inplace = True)
    df3.drop(columns = ['Unit'], inplace = True)
    df3.loc['OTHER'] = 100 - df3.loc[df3.index == 'RENEWABLE'
                                   ].iloc[0] - df3.loc[df3.index == 'FOSSIL'
                                                      ].iloc[0]
    
    plot_df3a = pd.DataFrame(columns = ['RENEWABLE', 'FOSSIL', 'OTHER'])
    plot_df3b = pd.DataFrame(columns = ['RENEWABLE', 'FOSSIL', 'OTHER'])
    
    for key, value in df3_dict.items():
        
        value['Metric'] = value['Metric'].replace({'Renewable energy share' : 'RENEWABLE',
                          'Fossil energy share' : 'FOSSIL'})
    
        value.set_index('Metric', inplace = True)
        value.drop(columns = ['Unit'], inplace = True)
        value.loc['OTHER'] = 100 - value.loc[value.index == 'RENEWABLE'
                                       ].iloc[0] - value.loc[value.index == 'FOSSIL'
                                                          ].iloc[0]
                                                          
        value = (value - df3)
        value = value.transpose()[['RENEWABLE', 'FOSSIL', 'OTHER']
                                  ].rename(index={'Value': key})
        
        gen_shares1 = value.clip(upper = 0)
        gen_shares2 = value.clip(lower = 0)
        
        if plot_df3a.empty:
            plot_df3a = gen_shares1
            plot_df3b = gen_shares2
        else:
            plot_df3a = pd.concat([plot_df3a, gen_shares1])
            plot_df3b = pd.concat([plot_df3b, gen_shares2])
            
    plot_df3a =  plot_df3a.loc[list(scenarios.values())]
    
    # Plot each layer of the bar, adding each bar to the 'bottom' so
    # the next bar starts higher.
    gen_shares_bot1 = 0
    gen_shares_bot2 = 0
    
    for i, col in enumerate(plot_df3a.columns):           
      ax5.bar(plot_df3a.index, plot_df3a[col], bottom = gen_shares_bot1,
              color = color_dict2.get(col), label = col, edgecolor = 'black',
              linewidth = 0.3)
      gen_shares_bot1 += np.array(plot_df3a[col])
      
    for i, col in enumerate(plot_df3b.columns):
      ax5.bar(plot_df3b.index, plot_df3b[col], bottom = gen_shares_bot2,
             color = color_dict2.get(col), edgecolor = 'black', linewidth = 0.3)
      gen_shares_bot2 += np.array(plot_df3b[col])
      
    # Subplot formatting
    ax5.set_ylim([min(plot_df3a.sum(axis=1), default = 0) * 1.1, 
                        max(plot_df3b.sum(axis=1), default = 0) * 1.1])
    ax5.legend(frameon = False, reverse = True, ncols = 1)

    ax5.set_ylabel(unit3)
    
    ax5.legend(bbox_to_anchor=(1.2, -0.52), frameon = False, 
              ncols = 3)
    
    # SET DUAL EMISSIONS AND COSTS CHART
    
    df4.set_index('YEAR', inplace = True)
    df5.set_index('YEAR', inplace = True)
    plot_df4 = pd.DataFrame(columns = ['VALUE'])
    plot_df5 = pd.DataFrame(columns = ['VALUE'])

    for key in df4_dict:

        df4_dict[key].set_index('YEAR', inplace = True)
           
        # Calculate Delta by year
        data = df4_dict[key][['VALUE']] - df4[['VALUE']]
        
        # Calculate model horizon Delta
        data = data.sum().fillna(0)
        plot_df4.loc[key] = data
        
    for key in df5_dict:

        df5_dict[key].set_index('YEAR', inplace = True)
           
        # Calculate Delta by year
        data = df5_dict[key][['VALUE']] - df5[['VALUE']]
        
        # Calculate model horizon Delta
        data = data.sum().fillna(0)
        plot_df5.loc[key] = data
        
    plot_df4 = pd.merge(plot_df4, plot_df5, left_index = True, right_index = True
                        ).rename(columns = {'VALUE_x' : 'emissions', 
                                            'VALUE_y' : 'costs'})

    plot_df4 = plot_df4.loc[list(scenarios.values())]
 
    plot_df4.emissions.plot(kind='bar', color= color_dict3.get('bar'), 
                            ax=ax6, position=1, width = 0.3, label = unit4)
    
    ax6.set_ylabel(unit4)
    
    ax7 = ax6.twinx()
    
    plot_df4.costs.plot(kind='bar', color= color_dict4.get('bar'), 
                        ax=ax7, position=0, width = 0.3, label = unit5)
    
    ax7.set_ylabel(unit5)
    
    ax6.legend(bbox_to_anchor=(0.53, -0.52), frameon = False)
    ax7.legend(bbox_to_anchor=(0.83, -0.52), frameon = False)
    
    ax1_ylims = ax6.axes.get_ylim()           # Find y-axis limits set by the plotter
    ax1_yratio = ax1_ylims[0] / ax1_ylims[1]  # Calculate ratio of lowest limit to highest limit
    
    ax2_ylims = ax7.axes.get_ylim()           # Find y-axis limits set by the plotter
    ax2_yratio = ax2_ylims[0] / ax2_ylims[1]  # Calculate ratio of lowest limit to highest limit

    if ax1_yratio < ax2_yratio: 
        ax7.set_ylim(bottom = ax2_ylims[1]*ax1_yratio)
    else:
        ax6.set_ylim(bottom = ax1_ylims[1]*ax2_yratio)    

    # PLT ADJUSTMENTS
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
        ax.margins(x = 0)
        ax.axhline(y=0, color='black', linestyle='-', linewidth = 0.3)
        ax.tick_params(axis = 'x', labelrotation = 75)
        
    ax1.text(-0.1, -0.07, 'c', transform=ax1.transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
    
    #ax2.text(-0.7, -0.07, 'd', transform=ax2.transAxes, 
   #           name = 'Calibri', fontsize = 15, weight = 'bold')
    
    ax3.text(-0.1, -0.07, 'd', transform=ax3.transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
    
   # ax4.text(-0.7, -0.07, 'f', transform=ax4.transAxes, 
   #           name = 'Calibri', fontsize = 15, weight = 'bold')
    
    ax5.text(-0.1, -0.07, 'a', transform=ax5.transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
    
    ax6.text(-0.05, -0.07, 'b', transform=ax6.transAxes, 
              name = 'Calibri', fontsize = 15, weight = 'bold')
       
    plt.subplots_adjust(wspace=2, 
                        hspace = 0.7
                        )

    
    return fig.savefig(os.path.join(base_path, file_name), bbox_inches = 'tight')
'''Functions as input to visualisations'''
import os
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import pandas as pd
import math

from utils import (
    convert_million_to_billion,
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
             label=col, color = color_dict.get(col))
      bottom1 += np.array(df1[col])
      
    for i, col in enumerate(df2.columns):
      axs[0,1].bar(df2.index, df2[col], bottom=bottom2, 
             label=col, color = color_dict.get(col))
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
             label=col, color = color_dict.get(col))
      bottom3 += np.array(df3[col])
      
    for i, col in enumerate(df4.columns):
      axs[0,0].bar('Total', df4[col], bottom=bottom4, 
             label=col, color = color_dict.get(col))
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

def format_stacked_bar_pwr_delta_country(df_in1, df_in2, out_dir, 
                                         chart_title, legend_title, 
                                         file_name, color_dict, unit, 
                                         start_year, end_year):
    
    years = get_years(start_year, end_year)
    
    countries = list(df_in1.index.get_level_values("COUNTRY").unique())
    
    rows = math.ceil(len(countries) / 2)
    
    fig, axs = plt.subplots(rows, 4, squeeze = False,
                            figsize = (9, rows * 2.5),
                            gridspec_kw = {
                                'width_ratios' : [1, 10, 1, 10]})
    
    axs = axs.ravel()

    x, y, z = 0, 1, 1
    
    legend_dict = {}

    for country in countries:
    
        # SET TIMESERIES SUBPLOT
        df1 = df_in1.loc[(df_in1['DELTA'] < 0) & 
                         (df_in1.index.get_level_values("COUNTRY") == country)]
        df2 = df_in1.loc[(df_in1['DELTA'] > 0) & 
                         (df_in1.index.get_level_values("COUNTRY") == country)]
    
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
                 label=col, color = color_dict.get(col))
          bottom1 += np.array(df1[col])
          
        for i, col in enumerate(df2.columns):
          axs[y].bar(df2.index, df2[col], bottom=bottom2, 
                 label=col, color = color_dict.get(col))
          bottom2 += np.array(df2[col])
        
        # Axis formatting
        axs[y].xaxis.set_major_formatter(FormatStrFormatter('%d'))
        axs[y].margins(x=0)
        axs[y].set_ylim([min(df1.sum(axis=1), default = -.1) * 1.1, 
                         max(df2.sum(axis=1), default = .1) * 1.1])
        axs[y].set_title(country, fontsize = 10)
        
        # Add unique legend entries
        handles, labels = axs[y].get_legend_handles_labels()
        by_label = dict(zip(labels, handles))

        for handle, label in by_label.items():
            legend_dict[handle] = label
        
        # SET TOTAL SUBPLOT  
        df3 = df_in2.loc[(df_in2['DELTA'] < 0) & 
                         (df_in2.index.get_level_values("COUNTRY") == country)]
        df4 = df_in2.loc[(df_in2['DELTA'] > 0) & 
                         (df_in2.index.get_level_values("COUNTRY") == country)]
    
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
                 label=col, color = color_dict.get(col))
          bottom3 += np.array(df3[col])
          
        for i, col in enumerate(df4.columns):
          axs[x].bar('Total', df4[col], bottom=bottom4, 
                 label=col, color = color_dict.get(col))
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
            
        axs[x].set_title(country, fontsize = 10)

        # Add unique legend entries
        handles, labels = axs[x].get_legend_handles_labels()
        by_label = dict(zip(labels, handles))

        for handle, label in by_label.items():
            legend_dict[handle] = label
        
        x, y, z = x + 2, y + 2, z + 1
    
    # CONFIG BOTH SUBPLOTS
    # Remove empty subplots
    if len(countries) % 2:
        fig.delaxes(axs[x])
        fig.delaxes(axs[y])
    
    # Set legend
    legend_dict = dict(sorted(legend_dict.items()))

    fig.legend(legend_dict.values(), legend_dict.keys(), 
               bbox_to_anchor=(0.7, (0.025 * rows)), frameon = False, 
               reverse = True, title = legend_title,
               ncols = 4)
    
    # Add plot title
    if chart_title:
        make_space_above(axs, topmargin=0.6) 
        plt.suptitle(chart_title)
    
    # Adjust subplot whitespace
    plt.subplots_adjust(wspace=0.5, hspace=0.3)
    
    # Add 0 line
    for i, ax in enumerate(fig.axes):
        ax.axhline(y=0, color='black', linestyle='-', linewidth = 0.1)

    return fig.savefig(os.path.join(out_dir, file_name), bbox_inches = 'tight')
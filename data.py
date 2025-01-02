'''Functions as input to visualisations'''
import os
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import pandas as pd
import math

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
             label=col, color = color_dict.get(col))
      bottom1 += np.array(df1[col])
      
    for i, col in enumerate(df2.columns):
      axs[0, 1].bar(df2.index, df2[col], bottom=bottom2, 
                   color = color_dict.get(col))
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
                    color = color_dict.get(col))
      bottom3 += np.array(df3[col])
      
    for i, col in enumerate(df4.columns):
      axs[0, 0].bar('Total', df4[col], bottom=bottom4, 
                    color = color_dict.get(col))
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
           color = color_dict.get('bar'))
    
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
    df = df2 - df1
    
    # Calculate model horizon Delta
    df3 = df.sum().fillna(0)
    
    fig, axs = plt.subplots(1, 2, squeeze = False,
                            gridspec_kw = {'width_ratios' : [1, 10]})
    
    axs[0, 1].bar(df.index, df['VALUE'], 
           color = color_dict.get('bar'))
    
    axs[0, 0].bar('Total', df3['VALUE'],
                 color = color_dict.get('bar'))
    
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
                   label = country)
        
        axs[x].bar('Total', df_total[country]['VALUE'],
                   color = color_dict.get(country))
        
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
               bbox_to_anchor=(0.7, (0.025 * rows)), frameon = False, 
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
                                   trn_title, out_dir, chart_title, 
                                   file_name, scenario):
    
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
             label=col, color = capacity_dict.get(col))
      capacity_bot1 += capacity1[col].iloc[0]
      
    for i, col in enumerate(capacity2.columns):
      axs[0, 0].barh('Total', capacity2[col], left=capacity_bot2, 
             label=col, color = capacity_dict.get(col))
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
             label=col, color = production_dict.get(col))
      production_bot1 += production1[col].iloc[0]
      
    for i, col in enumerate(production2.columns):
      axs[0, 1].barh('Total', production2[col], left=production_bot2, 
             label=col, color = production_dict.get(col))
      production_bot2 += production2[col].iloc[0]
    
    # Axis formatting
    axs[0, 1].set_xlim([min(production1.sum(axis=1), default = 0) * 1.1, 
                       max(production2.sum(axis=1), default = 0) * 1.1])
    axs[0, 1].title.set_text(production_title)    
    
    # Set combined legend for capacity & production subplots
    legend_dict = {}
    
    for ax in [axs[0, 0], axs[0, 1]]:
        # Add unique legend entries
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
    
        for handle, label in by_label.items():
            legend_dict[handle] = label

    legend_dict = dict(sorted(legend_dict.items()))
    axs[0, 0].legend(legend_dict.values(), legend_dict.keys(), 
               bbox_to_anchor=(1.5, -0.55), frameon = False, 
               ncols = math.ceil(len(legend_dict.keys()) / 2))

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
                    color = gen_shares_dict.get(col), label = col)
      gen_shares_bot1 += np.array(gen_shares1[col])
      
    for i, col in enumerate(gen_shares2.columns):
      axs[1, 0].barh('Total', gen_shares2[col], left = gen_shares_bot2,
                    color = gen_shares_dict.get(col))
      gen_shares_bot2 += np.array(gen_shares2[col])
      
    # Subplot formatting
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
                 color = emissions_dict.get('bar'))
    
    axs[2, 0].barh('Total', costs,
                 color = costs_dict.get('bar'))
    
    # Subplot formatting
    axs[1, 1].title.set_text(emissions_title)
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
                 color = 'maroon', label = 'Capacity Built')
    
    axs[2, 1].barh('Total', max_capacity_trn['VALUE'].iloc[0], 
                   height = 0.1, color = 'aqua', label = 'Max Capacity')
    
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
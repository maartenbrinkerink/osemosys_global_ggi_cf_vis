'''This script creates a set of charts relevant for the OSeMOSYS Global - GGI
Climate Finance project. It creates a set of charts for a base model run, 
followed by a set of charts for scenarios where specific transmission expansion
objects are assessed in terms of their climate finance impacts. For the
script to function, the user is required to set paths to the model 
result folders in 'config.py' as well as to set the geographical scope. In 
'config.py' the user can also set which charts to generate. In 'constants.py',
the user can change the color mapping as used in different charts. Generated
charts are saved to file.'''

import os

from config import(
    base_dir_results,
    base_dir_results_summaries,
    base_model,
    base_run_dict,
    countries,
    scenarios
    )

from constants import(
    bar_tech_color_dict,
    bar_gen_shares_color_dict,
    dual_costs_color_dict,
    dual_emissions_color_dict,
    country_color_dict
    )

from data import(
    convert_pj_to_twh,
    format_technology_col,
    format_annual_emissions,
    format_stacked_bar_pwr,
    format_stacked_bar_gen_shares,
    format_bar_line_costs,
    format_line_multi_country,
    format_bar_line_emissions,
    format_stacked_bar_line_emissions
    )

from read import (
    read_capacity_country,
    read_technology_annual_activity,
    read_generation_shares_country,
    read_generation_shares_global,
    read_pwr_cost_country,
    read_total_cost_country,
    read_pwr_cost_global,
    read_total_cost_global,
    read_annual_emissions,
    read_annual_emission_intensity_country,
    read_annual_emission_intensity_global
    )

base_path = f'Figures/{base_model}/Base'

'''Check for and create output paths'''
for country in countries:
    try:
        os.makedirs(os.path.join(base_path, country))
    except FileExistsError:
        pass
    
for scenario in scenarios:
    scen_path = f'Figures/{base_model}/{scenario}'
    for country in countries:
        try:
            os.makedirs(os.path.join(scen_path, country))
        except FileExistsError:
            pass
    
'''Create charts for base model run.'''
if base_run_dict.get('pwr_cap_bar_global') == 'yes':
    df = read_capacity_country(base_dir_results_summaries)
    
    chart_title = 'Installed Capacity'
    legend_title = ''
    file_name = 'pwr_cap_bar'
    unit = 'GW'
    
    format_stacked_bar_pwr(df, base_path, chart_title, 
                           legend_title, file_name, 
                           bar_tech_color_dict, unit, 
                           country = None)

if base_run_dict.get('pwr_cap_bar_country') == 'yes':
    df = read_capacity_country(base_dir_results_summaries)
    
    chart_title = 'Installed Capacity'
    legend_title = ''
    file_name = 'pwr_cap_bar'
    unit = 'GW'    
    
    for country in countries:
   
        format_stacked_bar_pwr(df, base_path, chart_title, 
                               legend_title, file_name, 
                               bar_tech_color_dict, unit, 
                               country = country)
        
if base_run_dict.get('pwr_gen_bar_global') == 'yes':
    df = read_technology_annual_activity(base_dir_results)
    df = format_technology_col(df)
    df = convert_pj_to_twh(df)
    
    chart_title = 'Generation'
    legend_title = ''
    file_name = 'pwr_gen_bar'
    unit = 'TWh'    
    
    format_stacked_bar_pwr(df, base_path, chart_title, 
                           legend_title, file_name, 
                           bar_tech_color_dict, unit, 
                           country = None)
    
if base_run_dict.get('pwr_gen_bar_country') == 'yes':
    df = read_technology_annual_activity(base_dir_results)
    df = format_technology_col(df)
    df = convert_pj_to_twh(df)
    
    chart_title = 'Generation'
    legend_title = ''
    file_name = 'pwr_gen_bar'
    unit = 'TWh'    
    
    for country in countries:
        format_stacked_bar_pwr(df, base_path, chart_title, 
                               legend_title, file_name, 
                               bar_tech_color_dict, unit, 
                               country = country)

if base_run_dict.get('pwr_gen_shares_global') == 'yes':
    df = read_generation_shares_global(base_dir_results_summaries)
    
    chart_title = 'Generation Shares'
    legend_title = ''
    file_name = 'pwr_gen_shares'
    unit = '%'    
    
    format_stacked_bar_gen_shares(df, base_path, chart_title, 
                                  legend_title, file_name, 
                                  bar_gen_shares_color_dict, unit, 
                                  country = None)
    
if base_run_dict.get('pwr_gen_shares_country') == 'yes':
    df = read_generation_shares_country(base_dir_results_summaries)
    
    chart_title = 'Generation Shares'
    legend_title = ''
    file_name = 'pwr_gen_shares'
    unit = '%'    
    
    for country in countries:
        format_stacked_bar_gen_shares(df, base_path, chart_title, 
                                      legend_title, file_name, 
                                      bar_gen_shares_color_dict, unit, 
                                      country = country)
        
if base_run_dict.get('dual_costs_global') == 'yes':
    df1 = read_total_cost_global(base_dir_results_summaries)
    df2 = read_pwr_cost_global(base_dir_results_summaries)
    
    chart_title = 'System Costs'
    legend_title = ''
    file_name = 'dual_costs'
    unit1 = 'Billion $/Year'
    unit2 = '$/MWh'
    
    format_bar_line_costs(df1, df2, base_path, chart_title, 
                          legend_title, file_name, 
                          dual_costs_color_dict, unit1, 
                          unit2, country = None)
    
if base_run_dict.get('dual_costs_country') == 'yes':
    df1 = read_total_cost_country(base_dir_results_summaries)
    df2 = read_pwr_cost_country(base_dir_results_summaries)
    
    chart_title = 'System Costs'
    legend_title = ''
    file_name = 'dual_costs'
    unit1 = 'Billion $/Year'
    unit2 = '$/MWh'
    
    for country in countries:
        format_bar_line_costs(df1, df2, base_path, chart_title, 
                              legend_title, file_name, 
                              dual_costs_color_dict, unit1, 
                              unit2, country = country)
        
if base_run_dict.get('pwr_costs_multi_country') == 'yes':
    df = read_pwr_cost_country(base_dir_results_summaries)
    
    chart_title = 'Normalized Costs'
    legend_title = ''
    file_name = 'multi_country_costs'
    unit = '$/MWh'
    
    format_line_multi_country(df, base_path, chart_title, 
                              legend_title, file_name, 
                              country_color_dict, unit)
    
if base_run_dict.get('dual_emissions_global') == 'yes':
    df1 = format_annual_emissions(read_annual_emissions(base_dir_results), 
                                  country = False)
    
    df2 = read_annual_emission_intensity_global(base_dir_results_summaries)
    
    chart_title = 'Annual Emissions'
    legend_title = ''
    file_name = 'dual_emissions'
    unit1 = 'Mt CO2'
    unit2 = 'gCO2/kWh'
    
    format_bar_line_emissions(df1, df2, base_path, chart_title, 
                              legend_title, file_name, 
                              dual_emissions_color_dict, unit1, 
                              unit2, country = None)
    
if base_run_dict.get('dual_emissions_country') == 'yes':
    df1 = format_annual_emissions(read_annual_emissions(base_dir_results), 
                                  country = True)
    
    df2 = format_annual_emissions(read_annual_emission_intensity_country(
        base_dir_results_summaries), country = True)
    
    chart_title = 'Annual Emissions'
    legend_title = ''
    file_name = 'dual_emissions'
    unit1 = 'Mt CO2'
    unit2 = 'gCO2/kWh'
    
    for country in countries:
        format_bar_line_emissions(df1, df2, base_path, chart_title, 
                                  legend_title, file_name, 
                                  dual_emissions_color_dict, unit1, 
                                  unit2, country = country)
        
if base_run_dict.get('dual_emissions_stacked') == 'yes':
    df1 = format_annual_emissions(read_annual_emissions(base_dir_results), 
                                  country = True)
    
    df2 = read_annual_emission_intensity_global(base_dir_results_summaries)
    
    chart_title = 'Annual Emissions'
    legend_title = ''
    file_name = 'dual_emissions_stacked'
    unit1 = 'Mt CO2'
    unit2 = 'gCO2/kWh (system)'
    
    format_stacked_bar_line_emissions(df1, df2, base_path, chart_title, 
                                      legend_title, file_name, 
                                      country_color_dict, unit1, 
                                      unit2)
    
'''Create charts for single scenario comparison to base.'''


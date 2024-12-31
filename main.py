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
    scen_dir_results,
    scen_dir_results_summaries,
    base_model,
    base_run_dict,
    scen_comparison_dict,
    countries,
    scenarios,
    start_year,
    end_year
    )

from constants import(
    BAR_TECH_COLOR_DICT,
    BAR_GEN_SHARES_COLOR_DICT,
    DUAL_COSTS_COLOR_DICT,
    DUAL_EMISSIONS_COLOR_DICT,
    COUNTRY_COLOR_DICT
    )

from data import(
    format_stacked_bar_pwr,
    format_stacked_bar_gen_shares,
    format_stacked_bar_gen_shares_delta,
    format_bar_line,
    format_bar_delta,
    format_line_multi_country,
    format_stacked_bar_line_emissions,
    format_stacked_bar_pwr_delta,
    format_stacked_bar_pwr_delta_country,
    format_bar_delta_country
    )

from utils import(
    convert_pj_to_twh,
    format_technology_col,
    format_annual_emissions,
    calculate_results_delta,
    convert_million_to_billion
    )

from read import (
    read_capacity_country,
    read_new_capacity_country,
    read_technology_annual_activity,
    read_generation_shares_country,
    read_generation_shares_global,
    read_pwr_cost_country,
    read_total_cost_country,
    read_pwr_cost_global,
    read_total_cost_global,
    read_annual_emissions,
    read_annual_emission_intensity_country,
    read_annual_emission_intensity_global,
    read_headline_metrics
    )

base_path = f'Figures/{base_model}/Base'

'''Check for and create output paths'''
for country in countries:
    try:
        os.makedirs(os.path.join(base_path, country))
    except FileExistsError:
        pass

scen_path = {}
for scenario in scenarios:
    scen_path[scenario] = f'Figures/{base_model}/{scenario}'
    
    try:
        os.makedirs(scen_path[scenario])
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
                           BAR_TECH_COLOR_DICT, unit, 
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
                               BAR_TECH_COLOR_DICT, unit, 
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
                           BAR_TECH_COLOR_DICT, unit, 
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
                               BAR_TECH_COLOR_DICT, unit, 
                               country = country)

if base_run_dict.get('pwr_gen_shares_global') == 'yes':
    df = read_generation_shares_global(base_dir_results_summaries)
    
    chart_title = 'Generation Shares'
    legend_title = ''
    file_name = 'pwr_gen_shares'
    unit = '%'    
    
    format_stacked_bar_gen_shares(df, base_path, chart_title, 
                                  legend_title, file_name, 
                                  BAR_GEN_SHARES_COLOR_DICT, unit, 
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
                                      BAR_GEN_SHARES_COLOR_DICT, unit, 
                                      country = country)
        
if base_run_dict.get('dual_costs_global') == 'yes':
    df1 = read_total_cost_global(base_dir_results_summaries)
    df2 = read_pwr_cost_global(base_dir_results_summaries)
    
    convert_million_to_billion(df1)
    
    chart_title = 'System Costs'
    legend_title = ''
    file_name = 'dual_costs'
    unit1 = 'Billion $/Year'
    unit2 = '$/MWh'
    
    format_bar_line(df1, df2, base_path, chart_title, 
                    legend_title, file_name, 
                    DUAL_COSTS_COLOR_DICT, unit1, 
                    unit2, country = None)
    
if base_run_dict.get('dual_costs_country') == 'yes':
    df1 = read_total_cost_country(base_dir_results_summaries)
    df2 = read_pwr_cost_country(base_dir_results_summaries)
    
    convert_million_to_billion(df1)
    
    chart_title = 'System Costs'
    legend_title = ''
    file_name = 'dual_costs'
    unit1 = 'Billion $/Year'
    unit2 = '$/MWh'
    
    for country in countries:
        format_bar_line(df1, df2, base_path, chart_title, 
                        legend_title, file_name, 
                        DUAL_COSTS_COLOR_DICT, unit1, 
                        unit2, country = country)
        
if base_run_dict.get('pwr_costs_multi_country') == 'yes':
    df = read_pwr_cost_country(base_dir_results_summaries)
    
    chart_title = 'Normalized Costs'
    legend_title = ''
    file_name = 'multi_country_costs'
    unit = '$/MWh'
    
    format_line_multi_country(df, base_path, chart_title, 
                              legend_title, file_name, 
                              COUNTRY_COLOR_DICT, unit)
    
if base_run_dict.get('dual_emissions_global') == 'yes':
    df1 = format_annual_emissions(read_annual_emissions(base_dir_results), 
                                  country = False)
    
    df2 = read_annual_emission_intensity_global(base_dir_results_summaries)
    
    chart_title = 'Annual Emissions'
    legend_title = ''
    file_name = 'dual_emissions'
    unit1 = 'Mt CO2'
    unit2 = 'gCO2/kWh'
    
    format_bar_line(df1, df2, base_path, chart_title, 
                    legend_title, file_name, 
                    DUAL_EMISSIONS_COLOR_DICT, unit1, 
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
        format_bar_line(df1, df2, base_path, chart_title, 
                        legend_title, file_name, 
                        DUAL_EMISSIONS_COLOR_DICT, unit1, 
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
                                      COUNTRY_COLOR_DICT, unit1, 
                                      unit2)
    
'''Create charts for single scenario comparison to base.'''
for scenario in scenarios:

    if scen_comparison_dict.get('pwr_cap_bar_dif_global') == 'yes':
        df1 = read_new_capacity_country(base_dir_results)
        df1 = format_technology_col(df1)
        
        df2 = read_new_capacity_country(scen_dir_results.get(scenario))
        df2 = format_technology_col(df2)
        
        df3 = calculate_results_delta(df1, df2, ['TECH', 'YEAR'],
                                      scenario)
        
        df4 = calculate_results_delta(df1, df2, ['TECH'],
                                      scenario)

        chart_title = f'{scenario} New Capacity - Delta'
        legend_title = ''
        file_name = 'pwr_new_cap_bar_delta'
        unit = 'GW'
        
        format_stacked_bar_pwr_delta(df3, df4, scen_path[scenario], 
                                     chart_title, legend_title, file_name, 
                                     BAR_TECH_COLOR_DICT, unit, start_year,
                                     end_year)
        

    if scen_comparison_dict.get('pwr_cap_bar_dif_country') == 'yes':
        df1 = read_new_capacity_country(base_dir_results)
        df1 = format_technology_col(df1)
        
        df2 = read_new_capacity_country(scen_dir_results.get(scenario))
        df2 = format_technology_col(df2)
        
        df3 = calculate_results_delta(df1, df2, ['COUNTRY', 'TECH', 'YEAR'],
                                      scenario)
        
        df4 = calculate_results_delta(df1, df2, ['COUNTRY', 'TECH'],
                                      scenario)

        chart_title = f'{scenario} New Capacity - Delta'
        legend_title = ''
        file_name = 'pwr_new_cap_bar_delta_country'
        unit = 'GW'
        
        format_stacked_bar_pwr_delta_country(df3, df4, scen_path[scenario], 
                                             chart_title, legend_title, file_name, 
                                             BAR_TECH_COLOR_DICT, unit, start_year,
                                             end_year)
        
    if scen_comparison_dict.get('pwr_gen_bar_dif_global') == 'yes':
        df1 = read_technology_annual_activity(base_dir_results)
        df1 = format_technology_col(df1)
        df1 = convert_pj_to_twh(df1)
        
        df2 = read_technology_annual_activity(scen_dir_results.get(scenario))
        df2 = format_technology_col(df2)
        df2 = convert_pj_to_twh(df2)
        
        df3 = calculate_results_delta(df1, df2, ['TECH', 'YEAR'],
                                      scenario)
        
        df4 = calculate_results_delta(df1, df2, ['TECH'],
                                      scenario)

        chart_title = f'{scenario} Generation - Delta'
        legend_title = ''
        file_name = 'pwr_gen_bar_delta'
        unit = 'TWh'
        
        format_stacked_bar_pwr_delta(df3, df4, scen_path[scenario], 
                                     chart_title, legend_title, file_name, 
                                     BAR_TECH_COLOR_DICT, unit, start_year,
                                     end_year)
        
    if scen_comparison_dict.get('pwr_gen_bar_dif_country') == 'yes':
        df1 = read_technology_annual_activity(base_dir_results)
        df1 = format_technology_col(df1)
        df1 = convert_pj_to_twh(df1)
        
        df2 = read_technology_annual_activity(scen_dir_results.get(scenario))
        df2 = format_technology_col(df2)
        df2 = convert_pj_to_twh(df2)
        
        df3 = calculate_results_delta(df1, df2, ['COUNTRY', 'TECH', 'YEAR'],
                                      scenario)
        
        df4 = calculate_results_delta(df1, df2, ['COUNTRY', 'TECH'],
                                      scenario)

        chart_title = f'{scenario} Generation - Delta'
        legend_title = ''
        file_name = 'pwr_gen_bar_delta_country'
        unit = 'TWh'

        format_stacked_bar_pwr_delta_country(df3, df4, scen_path[scenario], 
                                             chart_title, legend_title, file_name, 
                                             BAR_TECH_COLOR_DICT, unit, start_year,
                                             end_year)

    if scen_comparison_dict.get('costs_dif_global') == 'yes':
        df1 = read_total_cost_global(base_dir_results_summaries)
        df2 = read_total_cost_global(scen_dir_results_summaries.get(scenario))
        convert_million_to_billion(df1)
        convert_million_to_billion(df2)
        
        chart_title = f'{scenario} System Costs - Delta'
        legend_title = ''
        file_name = 'costs_delta_global'
        unit = 'Billion $'

        format_bar_delta(df1, df2, scen_path[scenario], 
                         chart_title, legend_title, 
                         file_name, DUAL_COSTS_COLOR_DICT, 
                         unit, country = None)

    if scen_comparison_dict.get('emissions_dif_global') == 'yes':
        df1 = format_annual_emissions(read_annual_emissions(base_dir_results), 
                                      country = False)
        df2 = format_annual_emissions(read_annual_emissions(
            scen_dir_results.get(scenario)), 
            country = False)
        
        chart_title = f'{scenario} Emissions - Delta'
        legend_title = ''
        file_name = 'emissions_delta_global'
        unit = 'Mt CO2'
        
        format_bar_delta(df1, df2, scen_path[scenario], 
                         chart_title, legend_title, 
                         file_name, DUAL_EMISSIONS_COLOR_DICT, 
                         unit, country = None)
        
    if scen_comparison_dict.get('costs_dif_country') == 'yes':
        df1 = read_total_cost_country(base_dir_results_summaries)
        df2 = read_total_cost_country(scen_dir_results_summaries.get(scenario))
        convert_million_to_billion(df1)
        convert_million_to_billion(df2)
        
        chart_title = f'{scenario} System Costs - Delta'
        legend_title = ''
        file_name = 'costs_delta_country'
        unit = 'Billion $'

        format_bar_delta_country(df1, df2, scen_path[scenario], 
                                 chart_title, legend_title, 
                                 file_name, COUNTRY_COLOR_DICT, 
                                 unit)
        
    if scen_comparison_dict.get('emissions_dif_country') == 'yes':
        df1 = format_annual_emissions(read_annual_emissions(base_dir_results), 
                                      country = True)
        df2 = format_annual_emissions(read_annual_emissions(
            scen_dir_results.get(scenario)), 
            country = True)
        
        chart_title = f'{scenario} Emissions - Delta'
        legend_title = ''
        file_name = 'emissions_delta_country'
        unit = 'Mt CO2'
        
        format_bar_delta_country(df1, df2, scen_path[scenario], 
                                 chart_title, legend_title, 
                                 file_name, COUNTRY_COLOR_DICT, 
                                 unit)
        
        
    if scen_comparison_dict.get('pwr_gen_shares_dif_global') == 'yes':
        df1 = read_generation_shares_global(base_dir_results_summaries)
        df2 = read_generation_shares_global(scen_dir_results_summaries.get(scenario))
        
        df3 = read_headline_metrics(base_dir_results_summaries)
        df4 = read_headline_metrics(scen_dir_results_summaries.get(scenario))
        
        chart_title = 'Generation Shares - Delta'
        legend_title = ''
        file_name = 'pwr_gen_shares_delta'
        unit = '%'    
        
        format_stacked_bar_gen_shares_delta(df1, df2, df3, df4, scen_path[scenario], 
                                            chart_title, legend_title, file_name, 
                                            BAR_GEN_SHARES_COLOR_DICT, unit)
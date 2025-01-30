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
os.chdir(r'C:\Users\mbrinkerink\GitHub\osemosys_global_ggi_cf_vis')

from user_config import(
    BASE,
    runs,
    base_dir_results,
    base_dir_results_summaries,
    base_dir_data,
    resources_data,
    custom_nodes_data,
    scen_dir_data,
    scen_dir_results,
    scen_dir_results_summaries,
    base_model,
    base_run_dict,
    base_scen_comparison_dict,
    multi_scen_comparison_dict,
    sensitivity_dict,
    nodal_results,
    countries,
    zizabona_countries,
    scenarios,
    start_year,
    end_year,
    axis_sort_delta,
    )

from constants import(
    BAR_TECH_COLOR_DICT,
    BAR_GEN_SHARES_COLOR_DICT,
    DUAL_COSTS_COLOR_DICT,
    DUAL_EMISSIONS_COLOR_DICT,
    DUAL_TRANSMISSION_COLOR_DICT,
    COUNTRY_COLOR_DICT,
    SENSITIVTIES_COLOR_DICT,
    STORAGE_LIST
    )

from data import(
    format_stacked_bar_pwr,
    format_stacked_bar_gen_shares,
    format_stacked_bar_gen_shares_delta,
    format_bar_line,
    format_bar_delta,
    format_line_multi_country,
    format_line_emission_limit,
    format_spatial_map_ASEAN,
    format_spatial_map_ZIZABONA,    
    format_stacked_bar_line_emissions,
    format_stacked_bar_pwr_delta,
    format_stacked_bar_pwr_delta_spatial,
    format_bar_delta_country,
    format_headline_metrics_global,
    format_bar_delta_multi_scenario,
    format_stacked_bar_gen_shares_delta_multi_scenario,
    format_transmission_capacity_multi_scenario,
    format_stacked_bar_pwr_delta_multi_scenario,
    format_multi_plot_cap_gen_genshares_emissions,
    format_multi_plot_country_charts,
    format_multi_plot_scen_comparison,
    format_bar_delta_multi_scenario_sensitivities,
    format_stacked_bar_gen_shares_delta_multi_scenario
    )

from utils import(
    convert_pj_to_twh,
    format_technology_col,
    format_annual_emissions,
    calculate_power_costs,
    calculate_results_delta,
    convert_million_to_billion,
    get_node_list,
    )

from read import (
    read_capacity_country,
    read_new_capacity,
    read_technology_annual_activity,
    read_generation_shares_country,
    read_generation_shares_global,
    read_pwr_cost_country,
    read_total_cost_country,
    read_pwr_cost_global,
    read_total_cost_global,
    read_total_discounted_cost,
    read_annual_emissions,
    read_annual_emission_limit,
    read_annual_emission_intensity_country,
    read_annual_emission_intensity_global,
    read_headline_metrics,
    read_max_capacity_investment,
    read_centerpoints
    )

base_path = f'Figures/{base_model}/Base'
multi_scenario_path = f'Figures/{base_model}/Comparison'
sensitivities_path = f'Figures/{base_model}/Sensitivities'

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
    
try:
    os.makedirs(multi_scenario_path)
except FileExistsError:
    pass

try:
    os.makedirs(sensitivities_path)
except FileExistsError:
    pass

'''Create charts for base model run.'''
if base_run_dict.get('pwr_cap_bar_global') == 'yes':
    df = read_capacity_country(base_dir_results_summaries[BASE])
    
    chart_title = 'Installed Capacity'
    legend_title = ''
    file_name = 'pwr_cap_bar'
    unit = 'GW'
    
    format_stacked_bar_pwr(df, base_path, chart_title, 
                           legend_title, file_name, 
                           BAR_TECH_COLOR_DICT, unit, 
                           country = None)

if base_run_dict.get('pwr_cap_bar_country') == 'yes':
    df = read_capacity_country(base_dir_results_summaries[BASE])
    
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
    df = read_technology_annual_activity(base_dir_results[BASE])
    df = format_technology_col(df, node = None)
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
    df = read_technology_annual_activity(base_dir_results[BASE])
    df = format_technology_col(df, node = None)
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
    df = read_generation_shares_global(base_dir_results_summaries[BASE])
    
    chart_title = 'Generation Shares'
    legend_title = ''
    file_name = 'pwr_gen_shares'
    unit = '%'    
    
    format_stacked_bar_gen_shares(df, base_path, chart_title, 
                                  legend_title, file_name, 
                                  BAR_GEN_SHARES_COLOR_DICT, unit, 
                                  country = None)
    
if base_run_dict.get('pwr_gen_shares_country') == 'yes':
    df = read_generation_shares_country(base_dir_results_summaries[BASE])
    
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
    df1 = read_total_discounted_cost(base_dir_results[BASE])
    
    df2 = read_technology_annual_activity(base_dir_results[BASE])
    df2 = format_technology_col(df2, node = None)
    df2 = convert_pj_to_twh(df2)
    df2 = calculate_power_costs(df1, df2, STORAGE_LIST)
    
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
    df1 = read_total_cost_country(base_dir_results_summaries[BASE])
    df2 = read_pwr_cost_country(base_dir_results_summaries[BASE])
    
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
    df = read_pwr_cost_country(base_dir_results_summaries[BASE])
    
    chart_title = 'Normalized Costs'
    legend_title = ''
    file_name = 'multi_country_costs'
    unit = '$/MWh'
    
    format_line_multi_country(df, base_path, chart_title, 
                              legend_title, file_name, 
                              COUNTRY_COLOR_DICT, unit)
    
if base_run_dict.get('dual_emissions_global') == 'yes':
    df1 = format_annual_emissions(read_annual_emissions(base_dir_results[BASE]), 
                                  country = False)
    
    df2 = read_annual_emission_intensity_global(base_dir_results_summaries[BASE])
    
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
    df1 = format_annual_emissions(read_annual_emissions(base_dir_results[BASE]), 
                                  country = True)
    
    df2 = format_annual_emissions(read_annual_emission_intensity_country(
        base_dir_results_summaries[BASE]), country = True)
    
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
    df1 = format_annual_emissions(read_annual_emissions(base_dir_results[BASE]), 
                                  country = True)

    df2 = read_annual_emission_intensity_global(base_dir_results_summaries[BASE])
    
    chart_title = 'Annual Emissions'
    legend_title = ''
    file_name = 'dual_emissions_stacked'
    unit1 = 'Mt CO2'
    unit2 = 'gCO2/kWh'
    
    format_stacked_bar_line_emissions(df1, df2, base_path, chart_title, 
                                      legend_title, file_name, 
                                      COUNTRY_COLOR_DICT, unit1, 
                                      unit2)
    
if base_run_dict.get('emissions_limit') == 'yes':
    df = read_annual_emission_limit(base_dir_data[BASE])
    
    chart_title = 'Emission Limit'
    legend_title = ''
    file_name = 'emission_limit'
    unit = 'Mt CO2'
    
    format_line_emission_limit(df, base_path, chart_title, 
                           legend_title, file_name, 
                           COUNTRY_COLOR_DICT, unit)
    
if base_run_dict.get('spatial_map_ASEAN') == 'yes':
    df1 = read_centerpoints(resources_data)
    df2 = read_centerpoints(custom_nodes_data)
    nodes = get_node_list(read_technology_annual_activity(base_dir_results[BASE]))

    chart_title = 'System Map'
    file_name = 'system_map_ASEAN'
    label = 'a'
    
    format_spatial_map_ASEAN(df1, df2, nodes, base_path, 
                                    chart_title, file_name, 
                                    COUNTRY_COLOR_DICT, label)
    
if base_run_dict.get('spatial_map_ZIZABONA') == 'yes':
    df1 = read_centerpoints(resources_data)
    nodes = [x + 'XX' for x in zizabona_countries]

    chart_title = 'System Map'
    file_name = 'system_map_ZIZABONA'
    label = 'b'
    
    format_spatial_map_ZIZABONA(df1, nodes, base_path, 
                                chart_title, file_name, 
                                COUNTRY_COLOR_DICT, label)
    
if base_run_dict.get('multi_plot_cap_gen_genshares_emisssions') == 'yes':
    
    df1 = read_capacity_country(base_dir_results_summaries[BASE])
    unit1 = 'GW'

    df2 = read_technology_annual_activity(base_dir_results[BASE])
    df2 = format_technology_col(df2, node = None)
    df2 = convert_pj_to_twh(df2)
    unit2 = 'TWh'    
    
    df3 = read_generation_shares_global(base_dir_results_summaries[BASE])
    unit3 = '%'    
    
    df4 = format_annual_emissions(read_annual_emissions(base_dir_results[BASE]), 
                                  country = True)
    unit4 = 'Mt CO2'

    df5 = read_annual_emission_intensity_global(base_dir_results_summaries[BASE])
    unit5 = 'gCO2/kWh'
    file_name = 'multi_plot_cap_gen_genshares_emissions'
    
    format_multi_plot_cap_gen_genshares_emissions(df1, df2, df3, df4, df5,
                                                   unit1, unit2, unit3, unit4, unit5,
                                                   base_path, file_name, 
                                                   BAR_TECH_COLOR_DICT,
                                                   BAR_GEN_SHARES_COLOR_DICT, 
                                                   COUNTRY_COLOR_DICT)
    
if base_run_dict.get('multi_plot_country_charts') == 'yes':
    
    df1 = read_capacity_country(base_dir_results_summaries[BASE])
    unit1 = 'GW'
    
    df2 = read_technology_annual_activity(base_dir_results[BASE])
    df2 = format_technology_col(df2, node = None)
    df2 = convert_pj_to_twh(df2)
    unit2 = 'TWh'
    
    df3 = read_generation_shares_country(base_dir_results_summaries[BASE])
    unit3 = '%'
    
    df4 = format_annual_emissions(read_annual_emissions(base_dir_results[BASE]), 
                              country = True)
    unit4 = 'Mt CO2'

    df5 = format_annual_emissions(read_annual_emission_intensity_country(
    base_dir_results_summaries[BASE]), country = True)
    unit5 = 'gCO2/kWh'
    
    file_name = 'multi_plot_country_charts'
    
    for country in countries:

        format_multi_plot_country_charts(df1, df2, df3, df4, df5,
                                         unit1, unit2, unit3, unit4, unit5,
                                         base_path, file_name, 
                                         BAR_TECH_COLOR_DICT,
                                         BAR_GEN_SHARES_COLOR_DICT, 
                                         DUAL_EMISSIONS_COLOR_DICT, country)
        
    
'''Create charts for single scenario comparison to base.'''
for scenario in scenarios:
    capacity_trn = read_new_capacity(scen_dir_results[BASE].get(scenario))
    if not capacity_trn.loc[capacity_trn['TECHNOLOGY'] == f'TRN{scenario}'].empty:

        if base_scen_comparison_dict.get('pwr_cap_bar_dif_global') == 'yes':
            df1 = read_new_capacity(base_dir_results[BASE])
            df1 = format_technology_col(df1, node = None)
            
            df2 = read_new_capacity(scen_dir_results[BASE].get(scenario))
            df2 = format_technology_col(df2, node = None)
            
            df3 = calculate_results_delta(df1, df2, ['TECH', 'YEAR'],
                                          scenario, nodal_results, node = None)
            
            df4 = calculate_results_delta(df1, df2, ['TECH'],
                                          scenario, nodal_results, node = None)
    
            chart_title = f'{scenario} New Capacity - Delta'
            legend_title = ''
            file_name = 'pwr_new_cap_bar_delta'
            unit = 'GW'
            
            format_stacked_bar_pwr_delta(df3, df4, scen_path[scenario], 
                                         chart_title, legend_title, file_name, 
                                         BAR_TECH_COLOR_DICT, unit, start_year,
                                         end_year)
            
    
        if base_scen_comparison_dict.get('pwr_cap_bar_dif_country') == 'yes':
            df1 = read_new_capacity(base_dir_results[BASE])
            df1 = format_technology_col(df1, node = None)
            
            df2 = read_new_capacity(scen_dir_results[BASE].get(scenario))
            df2 = format_technology_col(df2, node = None)
            
            df3 = calculate_results_delta(df1, df2, ['COUNTRY', 'TECH', 'YEAR'],
                                          scenario, nodal_results, node = None)
            
            df4 = calculate_results_delta(df1, df2, ['COUNTRY', 'TECH'],
                                          scenario, nodal_results, node = None)
    
            chart_title = f'{scenario} New Capacity - Delta'
            legend_title = ''
            file_name = 'pwr_new_cap_bar_delta_country'
            unit = 'GW'
            
            format_stacked_bar_pwr_delta_spatial(df3, df4, scen_path[scenario], 
                                                 chart_title, legend_title, file_name, 
                                                 BAR_TECH_COLOR_DICT, unit, start_year,
                                                 end_year, 'COUNTRY')
        
        if scenario in nodal_results.keys():
        
            if base_scen_comparison_dict.get('pwr_cap_bar_dif_node') == 'yes':
                df1 = read_new_capacity(base_dir_results[BASE])
                df1 = format_technology_col(df1, node = True)
                
                df2 = read_new_capacity(scen_dir_results[BASE].get(scenario))
                df2 = format_technology_col(df2, node = True)
                
                df3 = calculate_results_delta(df1, df2, ['NODE', 'TECH', 'YEAR'],
                                              scenario, nodal_results, node = True)
                
                df4 = calculate_results_delta(df1, df2, ['NODE', 'TECH'],
                                              scenario, nodal_results, node = True)
        
                chart_title = f'{scenario} New Capacity - Delta'
                legend_title = ''
                file_name = 'pwr_new_cap_bar_delta_node'
                unit = 'GW'
                
                format_stacked_bar_pwr_delta_spatial(df3, df4, scen_path[scenario], 
                                                     chart_title, legend_title, file_name, 
                                                     BAR_TECH_COLOR_DICT, unit, start_year,
                                                     end_year, 'NODE')
            
        if base_scen_comparison_dict.get('pwr_gen_bar_dif_global') == 'yes':
            df1 = read_technology_annual_activity(base_dir_results[BASE])
            df1 = format_technology_col(df1, node = None)
            df1 = convert_pj_to_twh(df1)
            
            df2 = read_technology_annual_activity(scen_dir_results[BASE].get(scenario))
            df2 = format_technology_col(df2, node = None)
            df2 = convert_pj_to_twh(df2)
            
            df3 = calculate_results_delta(df1, df2, ['TECH', 'YEAR'],
                                          scenario, nodal_results, node = None)
            
            df4 = calculate_results_delta(df1, df2, ['TECH'],
                                          scenario, nodal_results, node = None)
    
            chart_title = f'{scenario} Generation - Delta'
            legend_title = ''
            file_name = 'pwr_gen_bar_delta'
            unit = 'TWh'
            
            format_stacked_bar_pwr_delta(df3, df4, scen_path[scenario], 
                                         chart_title, legend_title, file_name, 
                                         BAR_TECH_COLOR_DICT, unit, start_year,
                                         end_year)
            
        if base_scen_comparison_dict.get('pwr_gen_bar_dif_country') == 'yes':
            df1 = read_technology_annual_activity(base_dir_results[BASE])
            df1 = format_technology_col(df1, node = None)
            df1 = convert_pj_to_twh(df1)
            
            df2 = read_technology_annual_activity(scen_dir_results[BASE].get(scenario))
            df2 = format_technology_col(df2, node = None)
            df2 = convert_pj_to_twh(df2)
            
            df3 = calculate_results_delta(df1, df2, ['COUNTRY', 'TECH', 'YEAR'],
                                          scenario, nodal_results, node = None)
            
            df4 = calculate_results_delta(df1, df2, ['COUNTRY', 'TECH'],
                                          scenario, nodal_results, node = None)
    
            chart_title = f'{scenario} Generation - Delta'
            legend_title = ''
            file_name = 'pwr_gen_bar_delta_country'
            unit = 'TWh'
    
            format_stacked_bar_pwr_delta_spatial(df3, df4, scen_path[scenario], 
                                                 chart_title, legend_title, file_name, 
                                                 BAR_TECH_COLOR_DICT, unit, start_year,
                                                 end_year, 'COUNTRY')
            
        if scenario in nodal_results.keys():
            
            if base_scen_comparison_dict.get('pwr_gen_bar_dif_node') == 'yes':
                df1 = read_technology_annual_activity(base_dir_results[BASE])
                df1 = format_technology_col(df1, node = True)
                df1 = convert_pj_to_twh(df1)
                
                df2 = read_technology_annual_activity(scen_dir_results[BASE].get(scenario))
                df2 = format_technology_col(df2, node = True)
                df2 = convert_pj_to_twh(df2)
                
                df3 = calculate_results_delta(df1, df2, ['NODE', 'TECH', 'YEAR'],
                                              scenario, nodal_results, node = True)
                
                df4 = calculate_results_delta(df1, df2, ['NODE', 'TECH'],
                                              scenario, nodal_results, node = True)
        
                chart_title = f'{scenario} Generation - Delta'
                legend_title = ''
                file_name = 'pwr_gen_bar_delta_node'
                unit = 'TWh'
        
                format_stacked_bar_pwr_delta_spatial(df3, df4, scen_path[scenario], 
                                                     chart_title, legend_title, file_name, 
                                                     BAR_TECH_COLOR_DICT, unit, start_year,
                                                     end_year, 'NODE')
    
        if base_scen_comparison_dict.get('costs_dif_global') == 'yes':
            df1 = read_total_discounted_cost(base_dir_results[BASE])
            df2 = read_total_discounted_cost(scen_dir_results[BASE].get(scenario))
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

        if base_scen_comparison_dict.get('emissions_dif_global') == 'yes':
            df1 = format_annual_emissions(read_annual_emissions(base_dir_results[BASE]), 
                                          country = False)
            df2 = format_annual_emissions(read_annual_emissions(
                scen_dir_results[BASE].get(scenario)), 
                country = False)
            
            chart_title = f'{scenario} Emissions - Delta'
            legend_title = ''
            file_name = 'emissions_delta_global'
            unit = 'Mt CO2'
            
            format_bar_delta(df1, df2, scen_path[scenario], 
                             chart_title, legend_title, 
                             file_name, DUAL_EMISSIONS_COLOR_DICT, 
                             unit, country = None)
            
        if base_scen_comparison_dict.get('costs_dif_country') == 'yes':
            df1 = read_total_cost_country(base_dir_results_summaries[BASE])
            df2 = read_total_cost_country(scen_dir_results_summaries[BASE].get(scenario))
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
            
        if base_scen_comparison_dict.get('emissions_dif_country') == 'yes':
            df1 = format_annual_emissions(read_annual_emissions(base_dir_results[BASE]), 
                                          country = True)
            df2 = format_annual_emissions(read_annual_emissions(
                scen_dir_results[BASE].get(scenario)), 
                country = True)
            
            chart_title = f'{scenario} Emissions - Delta'
            legend_title = ''
            file_name = 'emissions_delta_country'
            unit = 'Mt CO2'
            
            format_bar_delta_country(df1, df2, scen_path[scenario], 
                                     chart_title, legend_title, 
                                     file_name, COUNTRY_COLOR_DICT, 
                                     unit)           
            
        if base_scen_comparison_dict.get('pwr_gen_shares_dif_global') == 'yes':
            df1 = read_generation_shares_global(base_dir_results_summaries[BASE])
            df2 = read_generation_shares_global(scen_dir_results_summaries[BASE].get(scenario))
            
            df3 = read_headline_metrics(base_dir_results_summaries[BASE])
            df4 = read_headline_metrics(scen_dir_results_summaries[BASE].get(scenario))
            
            chart_title = 'Generation Shares - Delta'
            legend_title = ''
            file_name = 'pwr_gen_shares_delta'
            unit = '%'    
            
            format_stacked_bar_gen_shares_delta(df1, df2, df3, df4, scen_path[scenario], 
                                                chart_title, legend_title, file_name, 
                                                BAR_GEN_SHARES_COLOR_DICT, unit)
            
        if base_scen_comparison_dict.get('headline_metrics_dif_global') == 'yes':
    
            # Set inputs for capacity subplot
            capacity_base = read_new_capacity(base_dir_results[BASE])
            capacity_base = format_technology_col(capacity_base, node = None)
            
            capacity_scen = read_new_capacity(scen_dir_results[BASE].get(scenario))
            capacity_scen = format_technology_col(capacity_scen, node = None)
            
            capacity = calculate_results_delta(capacity_base, capacity_scen, ['TECH'],
                                               scenario, nodal_results,  node = None)
            capacity_title = 'Capacity (GW)'
    
            # Set inputs for generation subplot
            production_base = read_technology_annual_activity(base_dir_results[BASE])
            production_base = format_technology_col(production_base, node = None)
            production_base = convert_pj_to_twh(production_base)
            
            production_scen = read_technology_annual_activity(scen_dir_results[BASE].get(scenario))
            production_scen = format_technology_col(production_scen, node = None)
            production_scen = convert_pj_to_twh(production_scen)
    
            production = calculate_results_delta(production_base, production_scen, ['TECH'],
                                                 scenario, nodal_results,  node = None)
            production_title = 'Generation (TWh)'
             
            # Set inputs for generation shares subplot
            gen_shares_base = read_headline_metrics(base_dir_results_summaries[BASE])
            gen_shares_scen = read_headline_metrics(scen_dir_results_summaries[BASE].get(scenario))
            gen_shares_title = 'Generation Share (%)'
            
            # Set inputs for emissions subplot
            emissions_base = format_annual_emissions(read_annual_emissions(base_dir_results[BASE]), 
                                          country = True)
            emissions_scen = format_annual_emissions(read_annual_emissions(
                scen_dir_results[BASE].get(scenario)), 
                country = True)
            emissions_title = 'Emissions (Mt CO2)'
            
            # Set inputs for costs subplot
            costs_base = read_total_discounted_cost(base_dir_results[BASE])
            costs_scen = read_total_discounted_cost(scen_dir_results[BASE].get(scenario))           
            convert_million_to_billion(costs_base)
            convert_million_to_billion(costs_scen)
            costs_title = 'Total Costs (Billion $)'
            
            # Set inputs for transmission capacity subplot
            capacity_trn = read_new_capacity(scen_dir_results[BASE].get(scenario))
            max_capacity_trn = read_max_capacity_investment(scen_dir_data[BASE].get(scenario))
            trn_title = f'{scenario} Capacity (GW)'
    
            # Set chart inputs
            chart_title = ''
            file_name = 'headline_metrics_delta'
    
            # Create chart
            format_headline_metrics_global(capacity, production,
                                           capacity_title, production_title, 
                                           BAR_TECH_COLOR_DICT, BAR_TECH_COLOR_DICT,
                                           gen_shares_base, gen_shares_scen, 
                                           gen_shares_title, BAR_GEN_SHARES_COLOR_DICT,
                                           emissions_base, emissions_scen,
                                           emissions_title, DUAL_EMISSIONS_COLOR_DICT,
                                           costs_base, costs_scen,
                                           costs_title, DUAL_COSTS_COLOR_DICT,
                                           capacity_trn, max_capacity_trn,
                                           trn_title, DUAL_TRANSMISSION_COLOR_DICT,
                                           scen_path[scenario], chart_title, 
                                           file_name, scenario
                                           )
            
'''Create charts for multi scenario comparison.'''
if multi_scen_comparison_dict.get('emissions_dif') == 'yes':
    df1 = format_annual_emissions(read_annual_emissions(base_dir_results[BASE]), 
                                  country = False)
    df2_dict = {}
    
    for scenario in scenarios:
        capacity_trn = read_new_capacity(scen_dir_results[BASE].get(scenario))
        if not capacity_trn.loc[capacity_trn['TECHNOLOGY'] == f'TRN{scenario}'].empty:
            df2_dict[scenario] = format_annual_emissions(read_annual_emissions(
                scen_dir_results[BASE].get(scenario)), 
                country = False)

    chart_title = 'Emissions - Delta'
    file_name = 'emissions_delta_global'
    unit = 'Mt CO2'
            
    format_bar_delta_multi_scenario(df1, df2_dict, multi_scenario_path, 
                                    chart_title, file_name, 
                                    DUAL_EMISSIONS_COLOR_DICT, unit, axis_sort_delta)
    
if multi_scen_comparison_dict.get('costs_dif') == 'yes':
    df1 = read_total_discounted_cost(base_dir_results[BASE])
    convert_million_to_billion(df1)    
    df2_dict = {}
    
    for scenario in scenarios:
        capacity_trn = read_new_capacity(scen_dir_results[BASE].get(scenario))
        if not capacity_trn.loc[capacity_trn['TECHNOLOGY'] == f'TRN{scenario}'].empty:
            df2_dict[scenario] = read_total_discounted_cost(
                scen_dir_results[BASE].get(scenario))
            convert_million_to_billion(df2_dict[scenario])

    chart_title = 'System Costs - Delta'
    file_name = 'costs_delta_global'
    unit = 'Billion $'

    format_bar_delta_multi_scenario(df1, df2_dict, multi_scenario_path, 
                                    chart_title, file_name, 
                                    DUAL_COSTS_COLOR_DICT, unit, axis_sort_delta)
    
if multi_scen_comparison_dict.get('gen_shares_dif') == 'yes':
    df1 = read_headline_metrics(base_dir_results_summaries[BASE]) 
    df2_dict = {}
    
    for scenario in scenarios:
        capacity_trn = read_new_capacity(scen_dir_results[BASE].get(scenario))
        if not capacity_trn.loc[capacity_trn['TECHNOLOGY'] == f'TRN{scenario}'].empty:
            df2_dict[scenario] = read_headline_metrics(scen_dir_results_summaries[BASE].get(scenario))

    chart_title = 'Generation Shares - Delta'
    file_name = 'gen_shares_delta_global'
    unit = '%'
    
    format_stacked_bar_gen_shares_delta_multi_scenario(df1, df2_dict, multi_scenario_path, 
                                                       chart_title, file_name, 
                                                       BAR_GEN_SHARES_COLOR_DICT, unit,
                                                       axis_sort_delta)
    
if multi_scen_comparison_dict.get('trn_cap_dif') == 'yes':
    df1_dict = {}
    df2_dict = {}
    
    for scenario in scenarios:
        df1_dict[scenario] = read_new_capacity(scen_dir_results[BASE].get(scenario))
        df2_dict[scenario] = read_max_capacity_investment(scen_dir_data[BASE].get(scenario))

    chart_title = 'Transmission Capacity'
    file_name = 'transmission_capacity_delta_global'
    unit = 'GW'
    
    format_transmission_capacity_multi_scenario(df1_dict, df2_dict, multi_scenario_path, 
                                                chart_title, file_name, 
                                                DUAL_TRANSMISSION_COLOR_DICT, unit,
                                                axis_sort_delta)
    
if multi_scen_comparison_dict.get('capacity_dif') == 'yes':
    df1 = read_new_capacity(base_dir_results[BASE])
    df1 = format_technology_col(df1, node = None)
    df2_dict = {}
    
    for scenario in scenarios:
        capacity_trn = read_new_capacity(scen_dir_results[BASE].get(scenario))
        if not capacity_trn.loc[capacity_trn['TECHNOLOGY'] == f'TRN{scenario}'].empty:
            df2 = read_new_capacity(scen_dir_results[BASE].get(scenario))
            df2 = format_technology_col(df2, node = None)
            
            df2_dict[scenario] = calculate_results_delta(df1, df2, ['TECH'],
                                                         scenario, nodal_results,
                                                         node = None)
            
    chart_title = 'Capacity - Delta'
    file_name = 'capacity_delta_global'
    unit = 'GW'
    
    format_stacked_bar_pwr_delta_multi_scenario(df2_dict, multi_scenario_path, 
                                                chart_title, file_name, 
                                                BAR_TECH_COLOR_DICT, unit, 
                                                axis_sort_delta)
    
if multi_scen_comparison_dict.get('generation_dif') == 'yes':
    df1 = read_technology_annual_activity(base_dir_results[BASE])
    df1 = format_technology_col(df1, node = None)
    df1 = convert_pj_to_twh(df1)
    df2_dict = {}
    
    for scenario in scenarios:
        capacity_trn = read_new_capacity(scen_dir_results[BASE].get(scenario))
        if not capacity_trn.loc[capacity_trn['TECHNOLOGY'] == f'TRN{scenario}'].empty:
            df2 = read_technology_annual_activity(scen_dir_results[BASE].get(scenario))
            df2 = format_technology_col(df2, node = None)
            df2 = convert_pj_to_twh(df2)
            
            df2_dict[scenario] = calculate_results_delta(df1, df2, ['TECH'],
                                                         scenario, nodal_results,
                                                         node = None)
            
    chart_title = 'Generation - Delta'
    file_name = 'generation_delta_global'
    unit = 'TWh'
    
    format_stacked_bar_pwr_delta_multi_scenario(df2_dict, multi_scenario_path, 
                                                chart_title, file_name, 
                                                BAR_TECH_COLOR_DICT, unit,
                                                axis_sort_delta)
    
if multi_scen_comparison_dict.get('multi_plot_scen_comparison') == 'yes':
    df1a = read_new_capacity(base_dir_results[BASE])
    df1a = format_technology_col(df1a, node = None)
    
    df2a = read_technology_annual_activity(base_dir_results[BASE])
    df2a = format_technology_col(df2a, node = None)
    df2a = convert_pj_to_twh(df2a)
    
    df3 = read_headline_metrics(base_dir_results_summaries[BASE]) 
    df4 = format_annual_emissions(read_annual_emissions(base_dir_results[BASE]), 
                                  country = False)
    
    df1_dict = {}
    df2_dict = {}
    df3_dict = {}
    df4_dict = {}
    
    unit1 = 'GW'
    unit2 = 'TWh'
    unit3 = '%'
    unit4 = 'Mt CO2'
    
    file_name = 'multi_plot_scen_comparison'

    for scenario in scenarios:
        capacity_trn = read_new_capacity(scen_dir_results[BASE].get(scenario))
        if not capacity_trn.loc[capacity_trn['TECHNOLOGY'] == f'TRN{scenario}'].empty:
            df1b = read_new_capacity(scen_dir_results[BASE].get(scenario))
            df1b = format_technology_col(df1b, node = None)
            
            df2b = read_technology_annual_activity(scen_dir_results[BASE].get(scenario))
            df2b = format_technology_col(df2b, node = None)
            df2b = convert_pj_to_twh(df2b)
            
            df1_dict[scenario] = calculate_results_delta(df1a, df1b, ['TECH'],
                                                         scenario, nodal_results,
                                                         node = None)
            
            df2_dict[scenario] = calculate_results_delta(df2a, df2b, ['TECH'],
                                                         scenario, nodal_results,
                                                         node = None)
            
            df3_dict[scenario] = read_headline_metrics(scen_dir_results_summaries[BASE].get(scenario))
            
            df4_dict[scenario] = format_annual_emissions(read_annual_emissions(
                scen_dir_results[BASE].get(scenario)), country = False)

    format_multi_plot_scen_comparison(df1_dict, df2_dict, df3, df3_dict, 
                                      df4, df4_dict, unit1, unit2, unit3, 
                                      unit4, BAR_TECH_COLOR_DICT,
                                      BAR_GEN_SHARES_COLOR_DICT,
                                      DUAL_EMISSIONS_COLOR_DICT,
                                      multi_scenario_path, file_name, 
                                      axis_sort_delta)
    
'''Create charts for sensitivities.'''
if sensitivity_dict.get('emissions_dif') == 'yes':

    df1_dict = {}
    df2_dict = {}
    for run in runs:
        df1_dict[run] = format_annual_emissions(read_annual_emissions(base_dir_results[run]), 
                                                country = False)
        df2_dict[run] = {}
        for scenario in scenarios:

            capacity_trn = read_new_capacity(scen_dir_results[run].get(scenario))
            if not capacity_trn.loc[capacity_trn['TECHNOLOGY'] == f'TRN{scenario}'].empty:
                df2_dict[run][scenario] = format_annual_emissions(read_annual_emissions(
                    scen_dir_results[run].get(scenario)), 
                    country = False)
    
        chart_title = ''
        file_name = 'emissions_delta_global'
        unit = 'Mt CO2'
            
    format_bar_delta_multi_scenario_sensitivities(df1_dict, df2_dict, sensitivities_path, 
                                                  chart_title, file_name, 
                                                  SENSITIVTIES_COLOR_DICT, unit, axis_sort_delta,
                                                  runs, BASE)
    
if sensitivity_dict.get('gen_shares_dif') == 'yes':
    
    df1_dict = {}
    df2_dict = {}
    
    for run in runs:
        df1_dict[run] = read_headline_metrics(base_dir_results_summaries[run]) 
        df2_dict[run] = {}
        
        for scenario in scenarios:
            capacity_trn = read_new_capacity(scen_dir_results[BASE].get(scenario))
            if not capacity_trn.loc[capacity_trn['TECHNOLOGY'] == f'TRN{scenario}'].empty:
                df2_dict[run][scenario] = read_headline_metrics(scen_dir_results_summaries[run].get(scenario))

    chart_title = ''
    file_name = 'gen_shares_delta_global'
    unit = '%'
    
    a, b = format_stacked_bar_gen_shares_delta_multi_scenario(df1_dict, df2_dict, sensitivities_path, 
                                                       chart_title, file_name, 
                                                       BAR_GEN_SHARES_COLOR_DICT, unit,
                                                       axis_sort_delta, runs, BASE)
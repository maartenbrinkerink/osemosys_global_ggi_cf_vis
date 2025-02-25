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
os.chdir(r'C:\Users\maart\Github\osemosys_global_ggi_cf_vis')

from user_config import(
    figures_folder,
    base_dir_results,
    base_dir_results_summaries,
    base_dir_data,
    resources_data,
    custom_nodes_data,
    scen_dir_data,
    scen_dir_results,
    scen_dir_results_summaries,
    base_run_dict,
    base_scen_comparison_dict,
    multi_scen_comparison_dict,
    nodal_results,
    countries,
    scenarios,
    start_year,
    end_year,
    system_delta,
    axis_sort_delta
    )

from constants import(
    BAR_TECH_COLOR_DICT,
    BAR_GEN_SHARES_COLOR_DICT,
    DUAL_COSTS_COLOR_DICT,
    DUAL_EMISSIONS_COLOR_DICT,
    COUNTRY_COLOR_DICT,
    STORAGE_LIST
    )

from data import(
    format_stacked_bar_pwr,
    format_stacked_bar_demand,
    format_stacked_bar_gen_shares,
    format_stacked_bar_gen_shares_delta,
    format_bar_line,
    format_bar_delta,
    format_line_multi_country,
    format_line_emission_limit,
    format_spatial_map_ZIZABONA,    
    format_stacked_bar_line_emissions,
    format_stacked_bar_pwr_delta,
    format_stacked_bar_pwr_delta_spatial,
    format_bar_delta_country,
    format_bar_delta_multi_scenario,
    format_stacked_bar_gen_shares_delta_multi_scenario,
    format_stacked_bar_pwr_delta_multi_scenario,
    format_multi_plot_cap_gen_genshares_emissions,
    format_multi_plot_country_charts,
    format_multi_plot_scen_comparison,
    )

from utils import(
    convert_pj_to_twh,
    format_technology_col,
    format_annual_emissions,
    calculate_power_costs,
    calculate_results_delta,
    convert_million_to_billion,
    get_node_list
    )

from read import (
    read_capacity_country,
    read_new_capacity,
    read_specified_annual_demand,
    read_technology_annual_activity,
    read_generation_shares_country,
    read_generation_shares_global,
    read_pwr_cost_country,
    read_total_cost_country,
    read_pwr_cost_global,
    read_total_cost_global,
    read_total_discounted_cost,
    read_annual_emissions,
    read_annual_technology_emission,
    read_annual_emission_limit,
    read_annual_emission_intensity_country,
    read_annual_emission_intensity_global,
    read_headline_metrics,
    read_max_capacity_investment,
    read_centerpoints
    )

base_path = f'Figures/{figures_folder}/Base'
multi_scenario_path = f'Figures/{figures_folder}/Comparison'

'''Check for and create output paths'''
for country in countries:
    try:
        os.makedirs(os.path.join(base_path, country))
    except FileExistsError:
        pass

scen_path = {}
for scenario in scenarios.keys():
    scen_path[scenario] = f'Figures/{figures_folder}/{scenario}'
    
    try:
        os.makedirs(scen_path[scenario])
    except FileExistsError:
        pass
    
try:
    os.makedirs(multi_scenario_path)
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
    df = format_technology_col(df, node = None)
    df = convert_pj_to_twh(df)
    
    chart_title = 'Generation'
    legend_title = ''
    file_name = 'pwr_gen_bar'
    unit = 'PJ'    
    
    format_stacked_bar_pwr(df, base_path, chart_title, 
                           legend_title, file_name, 
                           BAR_TECH_COLOR_DICT, unit, 
                           country = None)
    
if base_run_dict.get('pwr_gen_bar_country') == 'yes':
    df = read_technology_annual_activity(base_dir_results)
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
    df1 = read_total_discounted_cost(base_dir_results)
    
    df2 = read_technology_annual_activity(base_dir_results)
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
    unit2 = 'gCO2/kWh'
    
    format_stacked_bar_line_emissions(df1, df2, base_path, chart_title, 
                                      legend_title, file_name, 
                                      COUNTRY_COLOR_DICT, unit1, 
                                      unit2)
    
if base_run_dict.get('demand_stacked') == 'yes':
    df1 = read_specified_annual_demand(base_dir_data)
    df1 = convert_pj_to_twh(df1)
    
    chart_title = 'Electricity Demand'
    legend_title = ''
    file_name = 'demand_stacked'
    unit = 'PJ'

    format_stacked_bar_demand(df1, base_path, chart_title, 
                              legend_title, file_name, 
                              COUNTRY_COLOR_DICT, unit)
    
if base_run_dict.get('emissions_limit') == 'yes':
    df = read_annual_emission_limit(base_dir_data)
    
    chart_title = 'Emission Limit'
    legend_title = ''
    file_name = 'emission_limit'
    unit = 'Mt CO2'
    
    format_line_emission_limit(df, base_path, chart_title, 
                           legend_title, file_name, 
                           COUNTRY_COLOR_DICT, unit)
    
if base_run_dict.get('spatial_map_ZIZABONA') == 'yes':
    df1 = read_centerpoints(resources_data)
    nodes = [x + 'XX' for x in countries]

    chart_title = 'System Map'
    file_name = 'system_map_ZIZABONA'
    label = 'b'
    
    format_spatial_map_ZIZABONA(df1, nodes, base_path, 
                                chart_title, file_name, 
                                COUNTRY_COLOR_DICT, label)
    
if base_run_dict.get('multi_plot_cap_gen_genshares_emisssions') == 'yes':
    
    df1 = read_capacity_country(base_dir_results_summaries)
    unit1 = 'GW'

    df2 = read_technology_annual_activity(base_dir_results)
    df2 = format_technology_col(df2, node = None)
    df2 = convert_pj_to_twh(df2)
    unit2 = 'TWh'    
    
    df3 = read_generation_shares_global(base_dir_results_summaries)
    unit3 = '%'    
    
    df4 = format_annual_emissions(read_annual_emissions(base_dir_results), 
                                  country = True)
    unit4 = 'Mt CO2'

    df5 = read_annual_emission_intensity_global(base_dir_results_summaries)
    unit5 = 'gCO2/kWh'
    file_name = 'multi_plot_cap_gen_genshares_emissions'
    
    format_multi_plot_cap_gen_genshares_emissions(df1, df2, df3, df4, df5,
                                                   unit1, unit2, unit3, unit4, unit5,
                                                   base_path, file_name, 
                                                   BAR_TECH_COLOR_DICT,
                                                   BAR_GEN_SHARES_COLOR_DICT, 
                                                   COUNTRY_COLOR_DICT)
    
if base_run_dict.get('multi_plot_country_charts') == 'yes':
    
    df1 = read_capacity_country(base_dir_results_summaries)
    unit1 = 'GW'
    
    df2 = read_technology_annual_activity(base_dir_results)
    df2 = format_technology_col(df2, node = None)
    df2 = convert_pj_to_twh(df2)
    unit2 = 'TWh'
    
    df3 = read_generation_shares_country(base_dir_results_summaries)
    unit3 = '%'
    
    df4 = format_annual_emissions(read_annual_emissions(base_dir_results), 
                              country = True)
    unit4 = 'Mt CO2'

    df5 = format_annual_emissions(read_annual_emission_intensity_country(
    base_dir_results_summaries), country = True)
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
for scenario, trn in scenarios.items():
    capacity_trn = read_new_capacity(scen_dir_results.get(scenario))
    if not capacity_trn.loc[capacity_trn['TECHNOLOGY'].isin(trn)].empty:

        if base_scen_comparison_dict.get('pwr_cap_bar_dif_global') == 'yes':
            df1 = read_new_capacity(base_dir_results)
            df1 = format_technology_col(df1, node = None)
            
            df2 = read_new_capacity(scen_dir_results.get(scenario))
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
            df1 = read_new_capacity(base_dir_results)
            df1 = format_technology_col(df1, node = None)
            
            df2 = read_new_capacity(scen_dir_results.get(scenario))
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
                df1 = read_new_capacity(base_dir_results)
                df1 = format_technology_col(df1, node = True)
                
                df2 = read_new_capacity(scen_dir_results.get(scenario))
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
            df1 = read_technology_annual_activity(base_dir_results)
            df1 = format_technology_col(df1, node = None)
            df1 = convert_pj_to_twh(df1)
            
            df2 = read_technology_annual_activity(scen_dir_results.get(scenario))
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
            df1 = read_technology_annual_activity(base_dir_results)
            df1 = format_technology_col(df1, node = None)
            df1 = convert_pj_to_twh(df1)
            
            df2 = read_technology_annual_activity(scen_dir_results.get(scenario))
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
                df1 = read_technology_annual_activity(base_dir_results)
                df1 = format_technology_col(df1, node = True)
                df1 = convert_pj_to_twh(df1)
                
                df2 = read_technology_annual_activity(scen_dir_results.get(scenario))
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
            df1 = read_total_discounted_cost(base_dir_results)
            df2 = read_total_discounted_cost(scen_dir_results.get(scenario))
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
            
        if base_scen_comparison_dict.get('costs_dif_country') == 'yes':
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
            
        if base_scen_comparison_dict.get('emissions_dif_country') == 'yes':
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
            
        if base_scen_comparison_dict.get('pwr_gen_shares_dif_global') == 'yes':
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

'''Create charts for multi scenario comparison.'''
if multi_scen_comparison_dict.get('emissions_dif') == 'yes':
    df1 = format_annual_emissions(read_annual_emissions(base_dir_results), 
                                  country = False)
    df2_dict = {}
    
    for scenario, trn in scenarios.items():
        capacity_trn = read_new_capacity(scen_dir_results.get(scenario))
        if not capacity_trn.loc[capacity_trn['TECHNOLOGY'].isin(trn)].empty:
            df2_dict[scenario] = format_annual_emissions(read_annual_emissions(
                scen_dir_results.get(scenario)), 
                country = False)

    chart_title = 'Emissions - Delta'
    file_name = 'emissions_delta_global'
    unit = 'Mt CO2'
            
    format_bar_delta_multi_scenario(df1, df2_dict, multi_scenario_path, 
                                    chart_title, file_name, 
                                    DUAL_EMISSIONS_COLOR_DICT, unit, 
                                    system_delta, axis_sort_delta)

if multi_scen_comparison_dict.get('costs_dif') == 'yes':
    df1 = read_total_discounted_cost(base_dir_results)
    convert_million_to_billion(df1)    
    df2_dict = {}
    
    for scenario, trn in scenarios.items():
        capacity_trn = read_new_capacity(scen_dir_results.get(scenario))
        if not capacity_trn.loc[capacity_trn['TECHNOLOGY'].isin(trn)].empty:
            df2_dict[scenario] = read_total_discounted_cost(
                scen_dir_results.get(scenario))
            convert_million_to_billion(df2_dict[scenario])

    chart_title = 'System Costs - Delta'
    file_name = 'costs_delta_global'
    unit = 'Billion $'

    format_bar_delta_multi_scenario(df1, df2_dict, multi_scenario_path, 
                                    chart_title, file_name, 
                                    DUAL_COSTS_COLOR_DICT, unit, 
                                    system_delta, axis_sort_delta)
    
if multi_scen_comparison_dict.get('gen_shares_dif') == 'yes':
    df1 = read_headline_metrics(base_dir_results_summaries) 
    df2_dict = {}
    
    for scenario, trn in scenarios.items():
        capacity_trn = read_new_capacity(scen_dir_results.get(scenario))
        if not capacity_trn.loc[capacity_trn['TECHNOLOGY'].isin(trn)].empty:
            df2_dict[scenario] = read_headline_metrics(scen_dir_results_summaries.get(scenario))

    chart_title = 'Generation Shares - Delta'
    file_name = 'gen_shares_delta_global'
    unit = '%'
    
    format_stacked_bar_gen_shares_delta_multi_scenario(df1, df2_dict, multi_scenario_path, 
                                                       chart_title, file_name, 
                                                       BAR_GEN_SHARES_COLOR_DICT, unit,
                                                       axis_sort_delta)
    
if multi_scen_comparison_dict.get('capacity_dif') == 'yes':
    df1 = read_new_capacity(base_dir_results)
    df1 = format_technology_col(df1, node = None)
    df2_dict = {}
    
    for scenario, trn in scenarios.items():
        capacity_trn = read_new_capacity(scen_dir_results.get(scenario))
        if not capacity_trn.loc[capacity_trn['TECHNOLOGY'].isin(trn)].empty:
            df2 = read_new_capacity(scen_dir_results.get(scenario))
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
    df1 = read_technology_annual_activity(base_dir_results)
    df1 = format_technology_col(df1, node = None)
    df1 = convert_pj_to_twh(df1)
    df2_dict = {}
    
    for scenario, trn in scenarios.items():
        capacity_trn = read_new_capacity(scen_dir_results.get(scenario))
        if not capacity_trn.loc[capacity_trn['TECHNOLOGY'].isin(trn)].empty:
            df2 = read_technology_annual_activity(scen_dir_results.get(scenario))
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
    df1a = read_new_capacity(base_dir_results)
    df1a = format_technology_col(df1a, node = None)
    
    df2a = read_technology_annual_activity(base_dir_results)
    df2a = format_technology_col(df2a, node = None)
    df2a = convert_pj_to_twh(df2a)
    
    df3 = read_headline_metrics(base_dir_results_summaries) 
    df4 = format_annual_emissions(read_annual_emissions(base_dir_results), 
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

    for scenario, trn in scenarios.items():
        capacity_trn = read_new_capacity(scen_dir_results.get(scenario))
        if not capacity_trn.loc[capacity_trn['TECHNOLOGY'].isin(trn)].empty:
            df1b = read_new_capacity(scen_dir_results.get(scenario))
            df1b = format_technology_col(df1b, node = None)
            
            df2b = read_technology_annual_activity(scen_dir_results.get(scenario))
            df2b = format_technology_col(df2b, node = None)
            df2b = convert_pj_to_twh(df2b)
            
            df1_dict[scenario] = calculate_results_delta(df1a, df1b, ['TECH'],
                                                         scenario, nodal_results,
                                                         node = None)
            
            df2_dict[scenario] = calculate_results_delta(df2a, df2b, ['TECH'],
                                                         scenario, nodal_results,
                                                         node = None)
            
            df3_dict[scenario] = read_headline_metrics(scen_dir_results_summaries.get(scenario))
            
            df4_dict[scenario] = format_annual_emissions(read_annual_emissions(
                scen_dir_results.get(scenario)), country = False)

    format_multi_plot_scen_comparison(df1_dict, df2_dict, df3, df3_dict, 
                                      df4, df4_dict, unit1, unit2, unit3, 
                                      unit4, BAR_TECH_COLOR_DICT,
                                      BAR_GEN_SHARES_COLOR_DICT,
                                      DUAL_EMISSIONS_COLOR_DICT,
                                      multi_scenario_path, file_name, 
                                      axis_sort_delta)
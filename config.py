'''Set paths.'''
base_model = 'ASEAN'
OG_path = 'C:\\Users\\maart\\Github\\osemosys_global'

base_dir_results = f'{OG_path}\\results\\{base_model}\\results'
base_dir_results_summaries = f'{OG_path}\\results\\{base_model}\\result_summaries'

'''Set scenarios that will be compared to the base_model.'''
scenarios = [
    'MYSPESGPXX',
    'MYSPETHASO'
    ]

'''Set start and end year of model horizon.'''
start_year = 2023
end_year = 2050

scen_dir_results = {}
scen_dir_results_summaries = {}

for scenario in scenarios:
    scen_dir_results[scenario] = f'{OG_path}\\results\\{scenario}\\results'
    scen_dir_results_summaries[scenario] = f'{OG_path}\\results\\{scenario}\\result_summaries'

'''Set default model data.'''
countries = ['BRN', 
             'IDN',
             'KHM', 
             'LAO', 
             'MMR', 
             'MYS', 
             'PHL', 
             'SGP', 
             'THA', 
             'VNM']

'''Set which visualisations to run.'''
base_run_dict = {
    'pwr_cap_bar_global' : 'yes',
    'pwr_cap_bar_country' : 'yes',
    'pwr_gen_bar_global' : 'yes',
    'pwr_gen_bar_country' : 'yes',
    'pwr_gen_shares_global' : 'yes',
    'pwr_gen_shares_country' : 'yes',
    'dual_costs_global' : 'yes',
    'dual_costs_country' : 'yes',
    'pwr_costs_multi_country' : 'yes',
    'dual_emissions_global' : 'yes',
    'dual_emissions_country' : 'yes',
    'dual_emissions_stacked' : 'yes',
    }

scen_comparison_dict = {
    'pwr_cap_bar_dif' : 'yes',
    }
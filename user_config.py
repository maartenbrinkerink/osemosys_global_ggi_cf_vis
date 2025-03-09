'''Set paths.'''
# Set name for folder in Figures
figures_folder = 'ZiZaBoNa_1%_ForcedBuilts'

# Set results path
results_folder = r'C:/Users/maart/OneDrive/Documenten/Work/Consulting/CCG/Climate Finance/results/ZiZaBoNa_1%_ForcedBuilts'

# Set OG path
og_path = r'C:/Users/maart/Github/osemosys_global'

# Set name for the baseline scenario
BASE = 'Base'

base_dir_results = f'{results_folder}/{BASE}/results'
base_dir_results_summaries = f'{results_folder}/{BASE}/result_summaries'
base_dir_data = f'{results_folder}/{BASE}/data'

resources_data = f'{og_path}/resources/data'
custom_nodes_data = f'{resources_data}/custom_nodes'

'''Set scenarios that will be compared to the base_model.'''
scenarios = {
    'BWAXXZWEXX' : ['TRNBWAXXZWEXX'],
    'NAMXXZMBXX' : ['TRNNAMXXZMBXX'],
    'ZMBXXZWEXX' : ['TRNZMBXXZWEXX'],
    'ZiZaBoNa' : ['TRNBWAXXZWEXX', 'TRNNAMXXZMBXX', 'TRNZMBXXZWEXX'],
    'SAPP' : ['TRNAGOXXNAMXX', 'TRNAGOXXCODXX', 'TRNAGOXXZMBXX', 
              'TRNCODXXZMBXX', 'TRNMOZXXMWIXX', 'TRNMWIXXTZAXX', 
              'TRNMOZXXZMBXX', 'TRNNAMXXZMBXX', 'TRNZAFXXZWEXX', 
              'TRNTZAXXZMBXX', 'TRNMOZXXTZAXX', 'TRNZMBXXZWEXX', 
              'TRNMOZXXZWEXX', 'TRNBWAXXZWEXX']
    }

'''Set start and end year of model horizon.'''
start_year = 2023
end_year = 2050

scen_dir_data = {}
scen_dir_results = {}
scen_dir_results_summaries = {}

for scenario in scenarios.keys():
    scen_dir_data[scenario] = f'{results_folder}/{scenario}/data'
    scen_dir_results[scenario] = f'{results_folder}/{scenario}/results'
    scen_dir_results_summaries[scenario] = f'{results_folder}/{scenario}/result_summaries'

'''Set default model data.'''
countries = [
    'AGO',
    'BWA',
    'COD',
    'LSO',
    'MOZ',
    'MWI',
    'NAM',
    'SWZ',
    'TZA',
    'ZAF',
    'ZMB',
    'ZWE',
    ]

'''Set which visualisations to run.'''
base_run_dict = {
    'pwr_cap_bar_global' : 'no',
    'pwr_cap_bar_country' : 'no',
    'pwr_gen_bar_global' : 'no',
    'pwr_gen_bar_country' : 'no',
    'pwr_gen_shares_global' : 'no',
    'pwr_gen_shares_country' : 'no',
    'dual_costs_global' : 'no',
    'dual_emissions_global' : 'no',
    'dual_emissions_country' : 'no',
    'dual_emissions_stacked' : 'no',
    'demand_stacked' : 'no',
    'emissions_limit' : 'no',
    'spatial_map_ZIZABONA' : 'no',    
    'multi_plot_cap_gen_genshares_emisssions' : 'no',
    'multi_plot_country_charts' : 'yes',
    }

base_scen_comparison_dict = {
    'pwr_cap_bar_dif_global' : 'no',
    'pwr_gen_bar_dif_global' : 'no',
    'pwr_cap_bar_dif_country' : 'no',
    'pwr_gen_bar_dif_country' : 'no',
    'pwr_cap_bar_dif_node' : 'no',
    'pwr_gen_bar_dif_node' : 'no',
    'costs_dif_global' : 'no',
    'emissions_dif_global' : 'no',
    'emissions_dif_country' : 'no',
    'pwr_gen_shares_dif_global' : 'no',
    }

multi_scen_comparison_dict = {
    'emissions_dif' : 'no',
    'costs_dif' : 'no',
    'gen_shares_dif' : 'no',
    'capacity_dif' : 'no',
    'generation_dif' : 'no',
    'multi_plot_scen_comparison' : 'no',
    'multi_plot_scen_comparison_costs' : 'no',
    }

'''Set for which scenarios nodal level results to show and list which 
countries require nodal level results.'''
nodal_results = {
    }

'''Set to True if the scenario deltas are to be calculated at the system level. If set
to False the delta will be calculated solely for the geographies connected to the transmission
project.'''
system_delta = True

'''Set to True if the axis labels need to be ordered by absolute size of the Delta.
Set to False if the labels need to be ordered alphabetically.'''
axis_sort_delta = False
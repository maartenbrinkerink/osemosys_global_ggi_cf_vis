'''Set paths.'''
base_model = 'ASEAN'
results_extension = ''
results_folder = r'C:\Users\maart\OneDrive\Documenten\Work\Consulting\CCG\Climate Finance\results\ASEAN'
og_path = r'C:\Users\maart\Github\osemosys_global'

BASE = 'Baseline'

runs = ['Baseline', 
        'LowTransmissionCosts',
        'NoNuclear',
        'PointTarget'
                 ]

results_path = {}
base_dir_results = {}
base_dir_results_summaries = {}
base_dir_data = {}

for run in runs:
    results_path[run] = f'{results_folder}\\{results_extension}{run}'
    base_dir_results[run] = f'{results_path[run]}\\{base_model}\\results'
    base_dir_results_summaries[run] = f'{results_path[run]}\\{base_model}\\result_summaries'
    base_dir_data[run] = f'{results_path[run]}\\{base_model}\\data'

resources_data = f'{og_path}\\resources\\data'
custom_nodes_data = f'{resources_data}\\custom_nodes'

'''Set scenarios that will be compared to the base_model.'''
scenarios = [
  'MYSPESGPXX',
  'MYSPETHASO',
  'IDNSMMYSPE',
  'MYSSHPHLLU',
  'BRNXXMYSSK',
  'LAOXXTHANO',
  'LAOXXVNMNO',
  'MMRXXTHANO',
  'KHMXXLAOXX',
  'KHMXXTHACE',
  'IDNKAMYSSH',
  'IDNSMSGPXX',
  'LAOXXMMRXX',
  'SGPXXVNMSO',
  'KHMXXSGPXX',
  'MYSPEMYSSK',
  'MYSSHMYSSK',
  'IDNJWIDNKA',
  'IDNJWIDNSM',
    ]

'''Set start and end year of model horizon.'''
start_year = 2023
end_year = 2050

scen_dir_data = {}
scen_dir_results = {}
scen_dir_results_summaries = {}

for run in runs:
    scen_dir_data[run] = {}
    scen_dir_results[run] = {}
    scen_dir_results_summaries[run] = {}
    for scenario in scenarios:
        scen_dir_data[run][scenario] = f'{results_path[run]}\\{scenario}\\data'
        scen_dir_results[run][scenario] = f'{results_path[run]}\\{scenario}\\results'
        scen_dir_results_summaries[run][scenario] = f'{results_path[run]}\\{scenario}\\result_summaries'

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

zizabona_countries = [
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
   #'dual_costs_country' : 'no', # Sub-global level costs incomplete
   #'pwr_costs_multi_country' : 'no', # Sub-global level costs incomplete
    'dual_emissions_global' : 'no',
    'dual_emissions_country' : 'no',
    'dual_emissions_stacked' : 'no',
    'emissions_limit' : 'no',
    'spatial_map_ASEAN' : 'no',
    'spatial_map_ZIZABONA' : 'no',    
    'multi_plot_cap_gen_genshares_emisssions' : 'no',
    'multi_plot_country_charts' : 'no',
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
    #'costs_dif_country' : 'no', # Sub-global level costs incomplete
    'emissions_dif_country' : 'no',
    'pwr_gen_shares_dif_global' : 'no',
    'headline_metrics_dif_global' : 'no',
    }

multi_scen_comparison_dict = {
    'emissions_dif' : 'no',
    'costs_dif' : 'no',
    'gen_shares_dif' : 'no',
    'trn_cap_dif' : 'no',
    'capacity_dif' : 'no',
    'generation_dif' : 'no',
    'multi_plot_scen_comparison' : 'no',
    }

sensitivity_dict = {
    'emissions_dif' : 'yes',
    'gen_shares_dif' : 'yes',
    }

'''Set for which scenarios nodal level results to show and list which 
countries require nodal level results.'''
nodal_results = {
    'MYSPEMYSSK' : ['MYS'],
    'MYSSHMYSSK' : ['MYS'],
    'IDNJWIDNKA' : ['IDN'],
    'IDNJWIDNSM' : ['IDN'],
    }

'''Set to True if the axis labels need to be ordered by absolute size of the Delta.
Set to False if the labels need to be ordered alphabetically.'''
axis_sort_delta = False
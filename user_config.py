'''Set paths.'''
base_model = 'ASEAN'
results_extension = ''
results_folder = r'C:\Users\maart\OneDrive\Documenten\Work\Consulting\CCG\Climate Finance\results\ASEAN'
og_path = r'C:\Users\maart\Github\osemosys_global'

BASE = 'Base'

runs = ['Base', 
        'CoalPhaseOut',
        #'CoalPhaseOut15%',
        #'LowTransmissionCosts',
        #'LongDurationStorage',
        #'HighGasPrice',
       # 'NoNuclear',
        #'PointTargets',
        #'NoTargets'
                 ]

results_path = {}
base_dir_results = {}
base_dir_results_summaries = {}
base_dir_data = {}

for run in runs:
    results_path[run] = f'{results_folder}/{results_extension}{run}'
    base_dir_results[run] = f'{results_path[run]}/{base_model}/results'
    base_dir_results_summaries[run] = f'{results_path[run]}/{base_model}/result_summaries'
    base_dir_data[run] = f'{results_path[run]}/{base_model}/data'

resources_data = f'{og_path}/resources/data'
custom_nodes_data = f'{resources_data}/custom_nodes'

'''Set scenarios that will be compared to the base_model.'''
scenarios = {
 # 'MYSPESGPXX' : ['TRNMYSPESGPXX'],
  #'MYSPETHASO' : ['TRNMYSPETHASO'],
  #'IDNSMMYSPE' : ['TRNIDNSMMYSPE'],
  #'MYSSHPHLLU' : ['TRNMYSSHPHLLU'],
  #'BRNXXMYSSK' : ['TRNBRNXXMYSSK'],
  #'LAOXXTHANO' : ['TRNLAOXXTHANO'],
  #'LAOXXVNMNO' : ['TRNLAOXXVNMNO'],
  #'MMRXXTHANO' : ['TRNMMRXXTHANO'],
  #'KHMXXLAOXX' : ['TRNKHMXXLAOXX'],
 # 'KHMXXTHACE' : ['TRNKHMXXTHACE'],
 # 'IDNKAMYSSH' : ['TRNIDNKAMYSSH'],
 # 'IDNSMSGPXX' : ['TRNIDNSMSGPXX'],
 # 'LAOXXMMRXX' : ['TRNLAOXXMMRXX'],
 # 'SGPXXVNMSO' : ['TRNSGPXXVNMSO'],
 # 'KHMXXSGPXX' : ['TRNKHMXXSGPXX'],
  'MYSPEMYSSK' : ['TRNMYSPEMYSSK'],
 # 'MYSSHMYSSK' : ['TRNMYSSHMYSSK'],
 # 'IDNJWIDNKA' : ['TRNIDNJWIDNKA'],
  #'IDNJWIDNSM' : ['TRNIDNJWIDNSM'],
    }

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
    for scenario in scenarios.keys():
        scen_dir_data[run][scenario] = f'{results_path[run]}/{scenario}/data'
        scen_dir_results[run][scenario] = f'{results_path[run]}/{scenario}/results'
        scen_dir_results_summaries[run][scenario] = f'{results_path[run]}/{scenario}/result_summaries'

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
    'pwr_cap_bar_global' : 'yes',
    'pwr_cap_bar_country' : 'yes',
    'pwr_gen_bar_global' : 'yes',
    'pwr_gen_bar_country' : 'yes',
    'pwr_gen_shares_global' : 'yes',
    'pwr_gen_shares_country' : 'yes',
    'dual_costs_global' : 'yes',
   #'dual_costs_country' : 'yes', # Sub-global level costs incomplete
   #'pwr_costs_multi_country' : 'yes', # Sub-global level costs incomplete
    'dual_emissions_global' : 'yes',
    'dual_emissions_country' : 'yes',
    'dual_emissions_stacked' : 'yes',
    'demand_stacked' : 'yes',
    'emissions_limit' : 'yes',
    'spatial_map_ASEAN' : 'yes',
    'spatial_map_ZIZABONA' : 'yes',    
    'multi_plot_cap_gen_genshares_emisssions' : 'yes',
    'multi_plot_country_charts' : 'yes',
    }

base_scen_comparison_dict = {
    'pwr_cap_bar_dif_global' : 'yes',
    'pwr_gen_bar_dif_global' : 'yes',
    'pwr_cap_bar_dif_country' : 'yes',
    'pwr_gen_bar_dif_country' : 'yes',
    'pwr_cap_bar_dif_node' : 'yes',
    'pwr_gen_bar_dif_node' : 'yes',
    'costs_dif_global' : 'yes',
    'emissions_dif_global' : 'yes',
    #'costs_dif_country' : 'yes', # Sub-global level costs incomplete
    'emissions_dif_country' : 'yes',
    'pwr_gen_shares_dif_global' : 'yes',
    'headline_metrics_dif_global' : 'yes',
    }

multi_scen_comparison_dict = {
    'emissions_dif' : 'yes',
    'costs_dif' : 'yes',
    'gen_shares_dif' : 'yes',
    'trn_cap_dif' : 'yes',
    'capacity_dif' : 'yes',
    'generation_dif' : 'yes',
    'multi_plot_scen_comparison' : 'yes',
    }

multi_scen_comparison_dict_geo = {
    'emissions_dif' : 'no',
    }

sensitivity_dict = {
    'emissions_dif' : 'yes',
    'emissions_dif_geo' : 'no',
    'costs_dif' : 'yes',
    'gen_shares_dif' : 'yes',
    'trn_cap_dif' : 'yes',
    'multi_plot_sensitivities' : 'yes',
    'multi_plot_cap_gen_genshares_emisssions' : 'yes',
    'multi_plot_scen_comparison' : 'yes',
    }

'''Set for which sensitivity runs scenario specific charts are 
to be generated.'''
sensitivity_scenario_dict_runs = [
            'CoalPhaseOut',
            #'LowTransmissionCosts',
            #'LongDurationStorage',
            #'HighGasPrice',
            #'NoNuclear',
            #'PointTargets',
            #'NoTargets'
    ]

sensitivity_scen_comparison_dict = {
    'pwr_cap_bar_dif_global' : 'yes',
    'pwr_gen_bar_dif_global' : 'yes',
    'pwr_cap_bar_dif_country' : 'yes',
    'pwr_gen_bar_dif_country' : 'yes',
    'pwr_cap_bar_dif_node' : 'yes',
    'pwr_gen_bar_dif_node' : 'yes',
    'costs_dif_global' : 'yes',
    'emissions_dif_global' : 'yes',
    #'costs_dif_country' : 'yes', # Sub-global level costs incomplete
    'emissions_dif_country' : 'yes',
    'pwr_gen_shares_dif_global' : 'yes',
    'headline_metrics_dif_global' : 'yes',
    }

sensitivity_multi_scen_comparison_dict = {
    'emissions_dif' : 'yes',
    'costs_dif' : 'yes',
    'gen_shares_dif' : 'yes',
    'trn_cap_dif' : 'yes',
    'capacity_dif' : 'yes',
    'generation_dif' : 'yes',
    }

'''Set for which scenarios nodal level results to show and list which 
countries require nodal level results.'''
nodal_results = {
    'MYSPEMYSSK' : ['MYS'],
    'MYSSHMYSSK' : ['MYS'],
    'IDNJWIDNKA' : ['IDN'],
    'IDNJWIDNSM' : ['IDN'],
    }

'''Set to True if the scenario deltas are to be calculated at the system level. If set
to False the delta will be calculated solely for the geographies connected to the transmission
project.'''
system_delta = True

'''Set to True if the axis labels need to be ordered by absolute size of the Delta.
Set to False if the labels need to be ordered alphabetically.'''
axis_sort_delta = False
'''Set paths.'''
base_model = 'ASEAN'
OG_path = ''

base_dir_results = f'{OG_path}\\results\\{base_model}\\results'
base_dir_results_summaries = f'{OG_path}\\results\\{base_model}\\result_summaries'

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

for scenario in scenarios:
    scen_dir_data[scenario] = f'{OG_path}\\results\\{scenario}\\data'
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

base_scen_comparison_dict = {
    'pwr_cap_bar_dif_global' : 'yes',
    'pwr_gen_bar_dif_global' : 'yes',
    'pwr_cap_bar_dif_country' : 'yes',
    'pwr_gen_bar_dif_country' : 'yes',
    'costs_dif_global' : 'yes',
    'emissions_dif_global' : 'yes',
    'costs_dif_country' : 'yes',
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
    'generation_dif' : 'yes'
    }
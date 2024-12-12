'''Set paths.'''
base_model = 'ASEAN'
OG_path = ''

base_dir_results = f'{OG_path}\\results\\{base_model}\\results'
base_dir_results_summaries = f'{OG_path}\\results\\{base_model}\\result_summaries'

'''Set which visualisations to run.'''
base_run_dict = {'pwr_cap_bar_global' : 'no',
                 'pwr_cap_bar_country' : 'no',
                 'pwr_gen_bar_global' : 'no',
                 'pwr_gen_bar_country' : 'no',
                 'pwr_gen_shares_global' : 'no',
                 'pwr_gen_shares_country' : 'no',
                 'dual_costs_global' : 'no',
                 'dual_costs_country' : 'no',
                 'pwr_costs_multi_country' : 'no',
                 'dual_emissions_global' : 'no',
                 'dual_emissions_country' : 'no',
                 'dual_emissions_stacked' : 'no',
    }

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

scenarios = [
    'MYSPESGPXX',
    'MYSPETHASO'
    ]
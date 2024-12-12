'''Set paths.'''
base_model = 'ASEAN'
OG_path = ''

base_dir_results = f'{OG_path}\\results\\{base_model}\\results'
base_dir_results_summaries = f'{OG_path}\\results\\{base_model}\\result_summaries'

'''Set which visualisations to run.'''
run_dict = {'pwr_cap_bar_global' : 'yes',
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
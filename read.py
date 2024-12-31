# import packages and paths
import pandas as pd
import os

# Functions to import result files
def read_capacity_country(path):
    df = pd.read_csv(os.path.join(path, 'PowerCapacityCountry.csv'))
    
    return df

def read_new_capacity_country(path):
    df = pd.read_csv(os.path.join(path, 'NewCapacity.csv'))
    
    return df

def read_technology_annual_activity(path):
    df = pd.read_csv(os.path.join(path, 'TotalTechnologyAnnualActivity.csv'))
    
    return df

def read_generation_shares_country(path):
    df = pd.read_csv(os.path.join(path, 'GenerationSharesCountry.csv'))
    
    return df

def read_generation_shares_global(path):
    df = pd.read_csv(os.path.join(path, 'GenerationSharesGlobal.csv'))
    
    return df

def read_pwr_cost_country(path):
    df = pd.read_csv(os.path.join(path, 'PowerCostCountry.csv'))
    
    return df

def read_total_cost_country(path):
    df = pd.read_csv(os.path.join(path, 'TotalCostCountry.csv'))
    
    return df

def read_pwr_cost_global(path):
    df = pd.read_csv(os.path.join(path, 'PowerCostGlobal.csv'))
    
    return df

def read_total_cost_global(path):
    df = pd.read_csv(os.path.join(path, 'TotalCostGlobal.csv'))
    
    return df

def read_annual_emissions(path):
    df = pd.read_csv(os.path.join(path, 'AnnualEmissions.csv'))
    
    return df

def read_annual_emission_intensity_country(path):
    df = pd.read_csv(os.path.join(path, 'AnnualEmissionIntensity.csv'))
    
    return df

def read_annual_emission_intensity_global(path):
    df = pd.read_csv(os.path.join(path, 'AnnualEmissionIntensityGlobal.csv'))
    
    return df

def read_headline_metrics(path):
    df = pd.read_csv(os.path.join(path, 'Metrics.csv'))
    
    return df
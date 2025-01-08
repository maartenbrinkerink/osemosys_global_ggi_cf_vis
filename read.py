# import packages and paths
import pandas as pd
import os

# Functions to import result files
def read_capacity_country(path):
    df = pd.read_csv(os.path.join(path, 'PowerCapacityCountry.csv'))
    
    return df

def read_new_capacity(path):
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

# PowerCostCountry is incomplete, DO NOT USE UNTIL FIXED
def read_pwr_cost_country(path):
    df = pd.read_csv(os.path.join(path, 'PowerCostCountry.csv'))
    
    return df

# TotalCostCountry is incomplete, DO NOT USE UNTIL FIXED
def read_total_cost_country(path):
    df = pd.read_csv(os.path.join(path, 'TotalCostCountry.csv'))
    
    return df

# PowerCostGlobal is incomplete, DO NOT USE UNTIL FIXED
def read_pwr_cost_global(path):
    df = pd.read_csv(os.path.join(path, 'PowerCostGlobal.csv'))
    
    return df

# TotalCostGlobal is incomplete, DO NOT USE UNTIL FIXED
def read_total_cost_global(path):
    df = pd.read_csv(os.path.join(path, 'TotalCostGlobal.csv'))
    
    return df

# TotalCostGlobal is incomplete, DO NOT USE UNTIL FIXED
def read_total_discounted_cost(path):
    df = pd.read_csv(os.path.join(path, 'TotalDiscountedCost.csv'))
    
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

def read_max_capacity_investment(path):
    df = pd.read_csv(os.path.join(path, 'TotalAnnualMaxCapacityInvestment.csv'))
    
    return df
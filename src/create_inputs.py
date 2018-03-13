"""
Code to automatically generate inputs for switch.

Developers:
    Pedro Andres Sanchez Perez
    Sergio Castellanos Rodriguez
    And other I do not know.
"""
import os
import sys
import yaml
import numpy as np
import pandas as pd
from collections import OrderedDict

data_path  = '../data/clean/loads/'
output_path  = '../data/clean/switch_inputs/'

def get_load_data(path=data_path, filename='HighLoads.csv',
        corrections=True, total=False, *args, **kwargs):
    """
        Load consumption data
        TODO:
            * This could be a csv or it could connect to a DB.
    """
    print (os.path.join(path, filename))
    df = pd.read_csv(os.path.join(path, filename))
    # Calculate the sum of loads
    df['total'] = df.sum(axis=1)
    # Convert to datetime if does not exist
    last_year = df['year'].iloc[-1:].values
    if corrections:
        try:
            df.loc[df['hour'] == 24, 'hour'] = 0
            df.loc[df['hour'] == 0, 'hour'] +=  1
            # Fix below code to represent a year regression
            df.loc[df['year'] > last_year] -= pd.DateOffset(day=365)
        except ValueError as e:
            # TODO Add error if data is wrong
            pass
    df.index = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

    if total:
        df = df[['total']].sort_index()
    df = df.sort_index()
    # TODO: Fix to return only total load
    return (df)

def get_peak_day(data, number=4, freq='MS'):
    """ Construc a representative day based on a single timestamp
    # Month start is to avoid getting more timepoints in a even division
    Args:
    data
    dates
    number
    TODO: Write readme
    """
    print (number)
    years = []
    if number & 1:
        raise ValueError('Odd number of timepoints. Use even number')
    for index, group in data.groupby([pd.Grouper(freq='A'),\
        pd.Grouper(freq=freq)]):
        peak_timestamp = group.idxmax()
        mask = peak_timestamp.strftime('%Y-%m-%d')
        years.append(group.loc[mask].iloc[::int((24/number))].reset_index())

    output_data = pd.concat(years)
    output_data.rename(columns={'index':'date', 'total':'peak_day'},\
            inplace=True)

    return (output_data)

def get_median_day(data, number=4, freq='1MS'):
    """ Calculate median day giving a timeseries

    """
    years = []
    for index, group in data.groupby([pd.Grouper(freq='A'),\
        pd.Grouper(freq=freq)]):
        grouper = group.groupby(pd.Grouper(freq='D')).mean()
        if len(grouper) & 1:
            # Odd number of days
            index_median = grouper.loc[grouper==grouper.median()].index[0]
        else:
            # Even number of days
            index_median = (np.abs(grouper-grouper.median())).idxmin()
        years.append(group.loc[index_median.strftime('%Y-%m-%d')].iloc[::int((24/number))].reset_index())
    output_data = pd.concat(years)
    output_data.rename(columns={'index':'date', 'total':'median_day'},\
            inplace=True)

    return ( output_data )

def create_investment_period(data, ext='.tab'):
    """
        Create periods file
    """
    # TODO: implement multiple periods based on the data
    output_file = output_path + 'periods' + ext

    # TODO: Migrate this to a function in utilities

    with open("periods.yaml", "r") as stream:
        try:
            periods = yaml.load(stream)
        except yaml.YAMLError as exc:
            raise (exc)

    d = OrderedDict(periods)
    periods_tab = pd.DataFrame(d)
    periods_tab = periods_tab.set_index('INVESTMENT_PERIOD')
    periods_tab.to_csv(output_file, sep='\t')

    return  (True)

def create_timepoints(data, ext='.tab'):
    """ Create timepoints file
    """
    if isinstance(data, list):
        data = pd.concat(data)
    output_file = output_path + 'timepoints' + ext
    if ext == '.tab': sep='\t'
    # Write test to check if columns exist
    data = data[['timestamp', 'TIMESERIES', 'daysinmonth']]
    data.index.name = 'timepoint_id'
    data = data.reset_index(drop=True)
    data = data.rename(columns={'TIMESERIES':'timeseries'})
    data.index += 1  # To start on 1 instead of 0
    data.index.name = 'timepoint_id'
    data[['timestamp', 'timeseries']].to_csv(output_file, sep=sep)

    return True

def create_strings(data,identifier='P',  ext='.tab'):
    """ Create timestamp file

    """
    strftime = '%Y%M%d%H'
    data['timestamp'] = data['date'].dt.strftime(strftime)
    data['TIMESERIES'] = data['date'].dt.strftime('%Y_%m{}'.format(identifier))
    data['daysinmonth'] = data['date'].dt.daysinmonth

    return (data)

def create_timeseries(data, number=4, ext='.tab'):
    """
        Create timeseries file
    """

    # Filename convention
    output_file = output_path + 'timeseries' + ext
    if ext == '.tab': sep='\t'

    # If multiple timeseries included in data
    if isinstance(data, list):
        data = pd.concat(data)

    size = len(data)

    # Extract unique timeseries_id
    timeseries = data[['TIMESERIES', 'daysinmonth']].drop_duplicates('TIMESERIES')
    timeseries.reset_index(drop=True, inplace=True)

    # TODO: fix this to change investment period 
    timeseries['ts_period'] = 2016

    ts_duration_of_tp = (24/number)
    timeseries['ts_duration_of_tp'] = ts_duration_of_tp

    timeseries['count'] = timeseries.groupby('ts_period')['TIMESERIES'].transform(len)
    timeseries['ts_num_tps'] = data[['timestamp', 'TIMESERIES']].groupby('TIMESERIES').count().values
    # TODO: Change 10 by difference of time between each period.
    scaling = 10*24*(365/timeseries['count'])/(timeseries['ts_duration_of_tp']*timeseries['ts_num_tps'])
    timeseries['ts_scale_to_period'] = scaling

    timeseries.index += 1  # To start on 1 instead of 0
    timeseries.index.name = 'timepoint_id'
    print (timeseries.head())
    del timeseries['daysinmonth']
    del timeseries['count']
    timeseries.to_csv(output_file, index=False, sep=sep)

def create_variablecp(data, ext='.tab'):
    """ Create variable capacity factor file
    """
    if isinstance(data, list):
        data = pd.concat(data)
    periods = set(data.date.dt.year)
    output_file = output_path + 'variable_capacity_factors' + ext
    data_path = '../data/clean/SWITCH/'
    ren_cap_data = pd.read_csv(data_path + 'ren-all2.csv', index_col=0,
                               parse_dates=True)

    filter_dates = pd.DatetimeIndex(data['date'].reset_index(drop=True)).strftime('%m-%d %H:%M:%S')
    #  filter_dates = pd.DatetimeIndex(data['date'].reset_index(drop=True))
    df = pd.DataFrame([])
    ren_tmp = ren_cap_data.copy()
    ren_tmp.index = ren_tmp.index + pd.DateOffset(years=2)
#df = df.append(ren_tmp)
    for year in periods:
        df = df.append(ren_tmp)
        ren_tmp.index = ren_tmp.index + pd.DateOffset(years=1)
    grouped = (df.loc[df['time'].isin(filter_dates)]
                .reset_index(drop=True)
                .groupby('GENERATION_PROJECT', as_index=False))
    tmp = []
    variable_cap = pd.concat([group.reset_index(drop=True) for name, group in grouped])
    if os.path.exists(output_file):
        os.remove(output_file)
    variable_tab = variable_cap.groupby('GENERATION_PROJECT')
    for keys in variable_tab.groups.keys():
        data = variable_tab.get_group(keys).reset_index(drop=True)
        data.index +=1
        data.index.name = 'timepoint'
        data.rename(columns={'capacity_factor': 'gen_max_capacity_factor'},
                   inplace=True)
        data.reset_index()[['GENERATION_PROJECT', 'timepoint',
            'gen_max_capacity_factor']].to_csv(output_file, sep='\t',
                    index=False, mode='a', header=(not
                        os.path.exists(output_file)))

def create_loads(load, data, ext='.tab'):
    """ Create loads file
    """
    if isinstance(data, list):
        data = pd.concat(data)
    output_file = output_path + 'loads' + ext
    loads_tmp = load[load.year <= 2025]
    list_tmp = []
    tmp = (loads_tmp.loc[data['date']]
            .drop(['year', 'month','day','hour', 'total'], axis=1)
            .reset_index()
            .drop_duplicates('index')
            .reset_index(drop=True))
    del tmp['index']
    tmp = tmp.unstack(0)
    for name, group in tmp.groupby(level=0):
        list_tmp.append(group.reset_index())
    loads_tab = pd.concat(list_tmp)
    loads_tab.index += 1
    loads_tab = loads_tab.rename(columns={'level_0':'LOAD_ZONE', 0:'zone_demand_mw'})
    del loads_tab['level_1']
    loads_tab.index.name = 'TIMEPOINT'
    loads_tab = loads_tab.reset_index()[['LOAD_ZONE', 'TIMEPOINT', 'zone_demand_mw']]
    loads_tab.to_csv(output_file, sep='\t', index=False)



def create_inputs(**kwargs):
    """ Create all inputs
    """
    load_data = get_load_data()
    peak_data = get_peak_day(load_data['2016']['total'], freq='1MS', **kwargs)
    median_data = get_median_day(load_data['2016']['total'], freq='1MS', **kwargs)
    peak = create_strings(peak_data)
    median = create_strings(median_data, identifier='M')
    create_investment_period(peak)
    create_timeseries([peak, median], **kwargs)
    create_timepoints([peak, median])
    create_variablecp([peak, median])
    create_loads(load_data, [peak, median])
    return (median)


if __name__ == '__main__':
    df = create_inputs(number=4)
    print (df.head())


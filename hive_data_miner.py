import fire
import time

from datetime import datetime
from enum import Enum
from hive_api_v6 import HiveAPIConnectionV6

# Fire command line entry point. Key arguments:
# - attributes: comma separated list of attributes to retrieve, should be the first part of the
#               channel id, e.g. "temperature", "targetTemperature" etc.
# - time_window: How far back from the current time in minutes to look get data from. Default
#                30 minutes.
def call(username: str,
         password: str,
         attributes: list,   
         time_window: int = 30,
         operation: str = 'AVG',
         output_format: str = 'CONSOLE'):

    api_connection = HiveAPIConnectionV6(username, password)
    channel_ids = []

    for channel in api_connection.get_channel_definitions().get('channels'):
        id = channel.get('id')
        if (id.split('@')[0] in attributes):
            channel_ids.append(id)

    # Hive expects all times in milliseconds from epoch
    end_time = int(time.time() * 1000)
    start_time = end_time - (time_window * 60 * 1000)

    raw_data = api_connection.get_channel_data(
        channel_ids,
        start_time,
        end_time,
        30,
        'MINUTES',
        operation)

    data_set = {}

    for channel in raw_data.get('channels'):
        data_set[channel.get('id')] = channel.get('values')
    
    if (str.upper(output_format) == 'CONSOLE'):
        return console_pretty_print(data_set)
    elif (str.upper(output_format) == 'JSON'):
        return filtered_json(data_set)
    else:
        raise ValueError(f'Invalid value {output_format} for --output_format')

def console_pretty_print(data_set):
    print('')
    for attribute in data_set.items():
        print(attribute[0].split('@')[0])
        print('=' * 30)
        for element in attribute[1].items():
            print('{}\t{}'.format(unix_ts_ms_to_dt(element[0]), str(element[1])))
        print('')

def filtered_json(data_set):
    filtered_data = {}

    for attribute in data_set.items():
        filtered_data[attribute[0].split('@')[0]] = attribute[1]

    return filtered_data

def unix_ts_ms_to_dt(unix_ts):
    return datetime.fromtimestamp(int(unix_ts) / 1000).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    fire.Fire(call)

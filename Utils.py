import pandas as pd
import matplotlib
import re


def load_data():
    file_path = 'Dataset/HealthApp_2k.log_structured.csv'
    df = pd.read_csv(file_path)
    df['Time'] = pd.to_datetime(df['Time'], format='%Y%m%d-%H:%M:%S:%f')
    df['Date'] = df['Time'].dt.date
    df['Hour'] = pd.to_datetime(df['Time'], format='%Y%m%d-%H:%M:%S:%f').dt.hour
    return df

def generateScreenStatusDataAll(data):
    data['statusChange'] = 0

    data.loc[data['EventId'] == 'E41', 'statusChange'] = 1
    data.loc[data['EventId'] == 'E40', 'statusChange'] = -1

    data['screenStatus'] = data['statusChange'].cumsum().clip(lower=0)

    data.drop('statusChange', axis=1, inplace=True)
    data['yVal'] = 'Screen Status'
    data['ScreenStatusCat'] = data['screenStatus'].apply(lambda x: 'Screen On' if x > 0 else 'Screen Off')

    data['timeShifted'] = data['Time'].shift(-1)

    data['duration'] = (data['timeShifted'] - data['Time']).dt.total_seconds() /60

    return data
def generateScreenStatusData(data, date):
    data['statusChange'] = 0

    data.loc[data['EventId'] == 'E41', 'statusChange'] = 1
    data.loc[data['EventId'] == 'E40', 'statusChange'] = -1

    data['screenStatus'] = data['statusChange'].cumsum().clip(lower=0)

    data.drop('statusChange', axis=1, inplace=True)
    data['yVal'] = 'Screen Status'
    data['ScreenStatusCat'] = data['screenStatus'].apply(lambda x: 'Screen On' if x > 0 else 'Screen Off')

    data['timeShifted'] = data['Time'].shift(-1)

    if date:
        data = data[(data['Time'].dt.date == pd.to_datetime(date).date())]

    data['duration'] = (data['timeShifted'] - data['Time']).dt.total_seconds() / 60

    return data


def extract_step_count(content):
    try:
        match = re.search(r'getTodayTotalDetailSteps = \d+##(\d+)', content)
        if match:
            return int(match.group(1))
        else:
            return None
    except Exception as e:
        print(f"Error extracting step count: {e}")
        return None

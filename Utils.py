import pandas
import matplotlib


def generateScreenStatusData(data):
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


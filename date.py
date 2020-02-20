from datetime import datetime
from dateutil.parser import parse


get_date_obj1 = parse("2020-03-05T00:00:00.000-08:00")
get_date_obj2 = parse("2018-02-05T00:00:00.000-08:00")
print(get_date_obj1 - get_date_obj2)

"""
format = '%Y-%m-%dT%H:%M:%S.%f'
minTime = datetime.strptime("2020-03-05T00:00:00.000", format)
"""

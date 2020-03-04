from datetime import datetime, timezone, timedelta
from dateutil.parser import parse


#get_date_obj1 = parse("2020-03-05T00:00:00.000-08:00")
#get_date_obj2 = parse("2018-02-05T00:00:00.000-08:00")
#print(get_date_obj1 - get_date_obj2)


#format = '%Y-%m-%dT%H:%M:%S.%f%Z'
#minTime = datetime.strptime("2020-03-24T00:00:00.000+01:00", format)


#format = '%Y-%m-%d %H:%M:%S'
x = datetime(2020, 3, 8, 0, 0,tzinfo=timezone(timedelta(days=0, seconds=3600)))
#y = x.strftime('%Y-%m-%dT%H:%M:%S.%3f')
print(x)
#print(y)

d = parse('2020-03-08T00:00:00.000+01:00')
print(d)

if d == x:
    print("wow")
else:
    print("neeey")